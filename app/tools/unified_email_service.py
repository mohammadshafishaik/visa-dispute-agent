"""Unified email service that tries multiple providers for reliability"""
from typing import Dict, Any
import os


class UnifiedEmailService:
    """Try multiple email providers for maximum reliability"""
    
    def __init__(self):
        self.providers = []
        
        # Try SendGrid first (most reliable)
        try:
            from app.tools.sendgrid_service import sendgrid_service
            if sendgrid_service.enabled:
                self.providers.append(("SendGrid", sendgrid_service))
        except:
            pass
        
        # Fallback to Gmail SMTP
        try:
            from app.tools.email_service import email_service
            if email_service.sender_email and email_service.sender_password:
                self.providers.append(("Gmail SMTP", email_service))
        except:
            pass
    
    def send_dispute_decision(
        self,
        to_email: str,
        dispute_id: str,
        customer_name: str,
        decision: str,
        reasoning: str,
        amount: float,
        currency: str = "INR"
    ) -> Dict[str, Any]:
        """Send email using the first available provider"""
        
        if not self.providers:
            print("⚠️  No email providers configured!")
            return {
                "success": False,
                "error": "No email providers available"
            }
        
        # Try each provider in order
        errors = []
        for provider_name, provider in self.providers:
            try:
                print(f"📧 Attempting to send email via {provider_name}...")
                result = provider.send_dispute_decision(
                    to_email=to_email,
                    dispute_id=dispute_id,
                    customer_name=customer_name,
                    decision=decision,
                    reasoning=reasoning,
                    amount=amount,
                    currency=currency
                )
                
                if result.get('success'):
                    print(f"✅ Email sent successfully via {provider_name}!")
                    return result
                else:
                    error_msg = f"{provider_name} failed: {result.get('error', 'Unknown error')}"
                    print(f"❌ {error_msg}")
                    errors.append(error_msg)
                    
            except Exception as e:
                error_msg = f"{provider_name} exception: {str(e)}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
        
        # All providers failed
        return {
            "success": False,
            "error": f"All email providers failed: {'; '.join(errors)}"
        }


# Global instance
unified_email_service = UnifiedEmailService()
