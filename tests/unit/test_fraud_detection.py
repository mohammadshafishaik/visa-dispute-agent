"""Unit tests for fraud pattern detection"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from app.schema.models import TransactionData
from app.tools.transaction_enrichment import TransactionEnrichment


def test_high_chargeback_rate_detected():
    """Verify high chargeback rate is flagged as suspicious"""
    enrichment = TransactionEnrichment("http://test")
    
    # Create 100 transactions with 5 chargebacks (5% rate)
    transactions = []
    for i in range(95):
        transactions.append(TransactionData(
            transaction_id=f"tx_{i}",
            customer_id="cust_123",
            amount=Decimal("50.00"),
            timestamp=datetime.utcnow() - timedelta(days=i),
            merchant="Test Merchant",
            status="completed"
        ))
    
    for i in range(5):
        transactions.append(TransactionData(
            transaction_id=f"cb_{i}",
            customer_id="cust_123",
            amount=Decimal("50.00"),
            timestamp=datetime.utcnow() - timedelta(days=i),
            merchant="Test Merchant",
            status="chargeback"
        ))
    
    analysis = enrichment.detect_fraud_patterns(transactions, Decimal("50.00"))
    
    assert analysis.chargeback_rate == 0.05
    assert analysis.has_suspicious_patterns is True
    assert analysis.risk_score > 0.4


def test_low_chargeback_rate_not_suspicious():
    """Verify low chargeback rate is not flagged"""
    enrichment = TransactionEnrichment("http://test")
    
    # Create 100 transactions with 0 chargebacks
    transactions = [
        TransactionData(
            transaction_id=f"tx_{i}",
            customer_id="cust_123",
            amount=Decimal("50.00"),
            timestamp=datetime.utcnow() - timedelta(days=i),
            merchant="Test Merchant",
            status="completed"
        )
        for i in range(100)
    ]
    
    analysis = enrichment.detect_fraud_patterns(transactions, Decimal("50.00"))
    
    assert analysis.chargeback_rate == 0.0
    assert analysis.has_suspicious_patterns is False
    assert analysis.risk_score < 0.4


def test_high_value_dispute_flagged():
    """Verify disputes significantly above average are flagged"""
    enrichment = TransactionEnrichment("http://test")
    
    # Create transactions with average $50
    transactions = [
        TransactionData(
            transaction_id=f"tx_{i}",
            customer_id="cust_123",
            amount=Decimal("50.00"),
            timestamp=datetime.utcnow() - timedelta(days=i),
            merchant="Test Merchant",
            status="completed"
        )
        for i in range(50)
    ]
    
    # Dispute for $500 (10x average)
    analysis = enrichment.detect_fraud_patterns(transactions, Decimal("500.00"))
    
    assert "significantly exceeds" in " ".join(analysis.pattern_details)
    assert analysis.risk_score > 0.0


def test_empty_transaction_history():
    """Verify empty history returns safe defaults"""
    enrichment = TransactionEnrichment("http://test")
    
    analysis = enrichment.detect_fraud_patterns([], Decimal("100.00"))
    
    assert analysis.chargeback_rate == 0.0
    assert analysis.has_suspicious_patterns is False
    assert analysis.risk_score == 0.0
    assert len(analysis.pattern_details) == 0
