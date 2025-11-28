"""Transaction enrichment tool for fraud pattern detection"""
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List
import httpx
from app.schema.models import TransactionData, FraudAnalysis


class RetriableError(Exception):
    """Exception for errors that should trigger retry logic"""
    pass


class TransactionEnrichment:
    """Fetches and analyzes transaction history for fraud detection"""
    
    def __init__(self, api_url: str, timeout: float = 10.0) -> None:
        self.api_url = api_url
        self.timeout = timeout
        self.max_retries = 3
        self.base_delay = 1.0
    
    async def fetch_history(
        self,
        customer_id: str,
        years: int = 3
    ) -> List[TransactionData]:
        """Fetch customer transaction history with retry logic and circuit breaker"""
        from app.tools.circuit_breaker import enrichment_circuit_breaker
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=years * 365)
        
        async def _fetch() -> List[TransactionData]:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    response = await client.get(
                        f"{self.api_url}/transactions",
                        params={
                            "customer_id": customer_id,
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat()
                        }
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    return [TransactionData(**tx) for tx in data.get("transactions", [])]
                    
                except httpx.TimeoutException as e:
                    raise RetriableError(f"Enrichment API timeout: {e}")
                except httpx.HTTPStatusError as e:
                    if e.response.status_code >= 500:
                        raise RetriableError(f"Enrichment API server error: {e}")
                    raise
        
        # Use circuit breaker for external API call
        try:
            return await enrichment_circuit_breaker.call(
                self._retry_with_backoff, _fetch
            )
        except Exception as e:
            # If circuit breaker is open, return empty list to allow processing to continue
            print(f"Circuit breaker open for enrichment service: {e}")
            return []
    
    async def _retry_with_backoff(self, func):
        """Execute function with exponential backoff retry logic"""
        for attempt in range(self.max_retries):
            try:
                return await func()
            except RetriableError as e:
                if attempt == self.max_retries - 1:
                    raise
                delay = self.base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
        
        raise RuntimeError("Max retries exceeded")
    
    def detect_fraud_patterns(
        self,
        transactions: List[TransactionData],
        current_dispute_amount: Decimal
    ) -> FraudAnalysis:
        """Analyze transaction history for friendly fraud indicators"""
        if not transactions:
            return FraudAnalysis(
                has_suspicious_patterns=False,
                chargeback_rate=0.0,
                pattern_details=[],
                risk_score=0.0
            )
        
        # Calculate chargeback rate
        total_transactions = len(transactions)
        chargebacks = [tx for tx in transactions if tx.status == "chargeback"]
        chargeback_rate = len(chargebacks) / total_transactions if total_transactions > 0 else 0.0
        
        pattern_details = []
        risk_factors = 0
        
        # Pattern 1: High chargeback rate (>1% indicates friendly fraud)
        if chargeback_rate > 0.01:
            pattern_details.append(
                f"High chargeback rate: {chargeback_rate:.2%} (threshold: 1%)"
            )
            risk_factors += 2
        
        # Pattern 2: Multiple recent chargebacks
        recent_chargebacks = [
            tx for tx in chargebacks
            if (datetime.utcnow() - tx.timestamp).days <= 180
        ]
        if len(recent_chargebacks) >= 3:
            pattern_details.append(
                f"Multiple recent chargebacks: {len(recent_chargebacks)} in last 6 months"
            )
            risk_factors += 2
        
        # Pattern 3: High-value dispute relative to transaction history
        avg_transaction = sum(tx.amount for tx in transactions) / len(transactions)
        if current_dispute_amount > avg_transaction * 3:
            pattern_details.append(
                f"Dispute amount (${current_dispute_amount}) significantly exceeds "
                f"average transaction (${avg_transaction:.2f})"
            )
            risk_factors += 1
        
        # Pattern 4: Timing patterns (disputes filed long after delivery)
        # This would require delivery confirmation data - placeholder for now
        
        # Pattern 5: Successful transactions from same merchant
        # This would require merchant matching - placeholder for now
        
        # Calculate overall risk score (0.0 - 1.0)
        risk_score = min(risk_factors / 5.0, 1.0)
        has_suspicious_patterns = risk_score >= 0.4
        
        return FraudAnalysis(
            has_suspicious_patterns=has_suspicious_patterns,
            chargeback_rate=chargeback_rate,
            pattern_details=pattern_details,
            risk_score=risk_score
        )
