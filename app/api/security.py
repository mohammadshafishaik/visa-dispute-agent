"""Security middleware and utilities"""
import hmac
import hashlib
import time
from typing import Optional, Dict
from fastapi import Request, HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        """Initialize rate limiter"""
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        
        recent_requests = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]
        
        return max(0, self.requests_per_minute - len(recent_requests))


class WebhookSignatureValidator:
    """Validates webhook signatures using HMAC"""
    
    def __init__(self, secret: str):
        """Initialize validator with secret key"""
        self.secret = secret.encode() if isinstance(secret, str) else secret
    
    def generate_signature(self, payload: bytes, timestamp: str) -> str:
        """Generate HMAC signature for payload"""
        message = f"{timestamp}.{payload.decode()}"
        signature = hmac.new(
            self.secret,
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def verify_signature(
        self,
        payload: bytes,
        signature: str,
        timestamp: str,
        tolerance: int = 300  # 5 minutes
    ) -> bool:
        """Verify webhook signature"""
        # Check timestamp to prevent replay attacks
        try:
            request_time = int(timestamp)
            current_time = int(time.time())
            
            if abs(current_time - request_time) > tolerance:
                return False
        except (ValueError, TypeError):
            return False
        
        # Verify signature
        expected_signature = self.generate_signature(payload, timestamp)
        return hmac.compare_digest(signature, expected_signature)


class APIKeyValidator:
    """Validates API keys"""
    
    def __init__(self, valid_keys: Optional[set] = None):
        """Initialize with valid API keys"""
        self.valid_keys = valid_keys or set()
    
    def is_valid(self, api_key: str) -> bool:
        """Check if API key is valid"""
        return api_key in self.valid_keys
    
    def add_key(self, api_key: str) -> None:
        """Add a valid API key"""
        self.valid_keys.add(api_key)
    
    def remove_key(self, api_key: str) -> None:
        """Remove an API key"""
        self.valid_keys.discard(api_key)


# Global instances
rate_limiter = RateLimiter(requests_per_minute=100)
webhook_validator = WebhookSignatureValidator(secret="your-webhook-secret-key")
api_key_validator = APIKeyValidator()


async def verify_webhook_signature(request: Request) -> None:
    """Middleware to verify webhook signatures"""
    # Get signature from headers
    signature = request.headers.get("X-Webhook-Signature")
    timestamp = request.headers.get("X-Webhook-Timestamp")
    
    if not signature or not timestamp:
        # For development, allow requests without signatures
        # In production, this should raise an exception
        return
    
    # Get request body
    body = await request.body()
    
    # Verify signature
    if not webhook_validator.verify_signature(body, signature, timestamp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )


async def check_rate_limit(request: Request) -> None:
    """Middleware to check rate limits"""
    # Get client identifier (IP address or API key)
    client_id = request.client.host if request.client else "unknown"
    
    # Check API key if provided
    api_key = request.headers.get("X-API-Key")
    if api_key:
        if not api_key_validator.is_valid(api_key):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        client_id = api_key
    
    # Check rate limit
    if not rate_limiter.is_allowed(client_id):
        remaining = rate_limiter.get_remaining(client_id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again later.",
            headers={"X-RateLimit-Remaining": str(remaining)}
        )


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()
