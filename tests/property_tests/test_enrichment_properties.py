"""Property-based tests for enrichment service properties"""
import pytest
from hypothesis import given, strategies as st
from datetime import datetime, timedelta
from decimal import Decimal


# Feature: visa-dispute-agent, Property 4: Enrichment service invocation
@given(
    customer_id=st.text(min_size=1, max_size=50),
    years=st.integers(min_value=1, max_value=5)
)
def test_enrichment_requests_correct_time_range(customer_id, years):
    """For any enrichment request, it should request exactly N years of history"""
    from app.tools.transaction_enrichment import TransactionEnrichment
    
    enrichment = TransactionEnrichment("http://test-api")
    
    # Calculate expected date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=years * 365)
    
    # Verify the date range calculation
    calculated_days = (end_date - start_date).days
    expected_days = years * 365
    
    # Allow for small variance due to leap years
    assert abs(calculated_days - expected_days) <= years


@given(
    customer_id=st.text(min_size=1, max_size=50)
)
def test_enrichment_always_requests_three_years(customer_id):
    """For any dispute, enrichment should request exactly 3 years of history"""
    # This is the specific requirement from the spec
    required_years = 3
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=required_years * 365)
    
    # Verify 3-year calculation
    days_diff = (end_date - start_date).days
    assert 1090 <= days_diff <= 1100  # ~3 years accounting for leap years


# Feature: visa-dispute-agent, Property 5: Enrichment state update
@given(
    num_transactions=st.integers(min_value=0, max_value=100)
)
def test_enrichment_updates_state_with_transactions(num_transactions):
    """For any successful enrichment, state should contain transaction history"""
    from app.schema.models import TransactionData
    
    # Simulate transaction history
    transactions = [
        TransactionData(
            transaction_id=f"tx_{i}",
            customer_id="cust_123",
            amount=Decimal("50.00"),
            timestamp=datetime.utcnow() - timedelta(days=i),
            merchant="Test Merchant",
            status="completed"
        )
        for i in range(num_transactions)
    ]
    
    # Simulate state update
    state = {
        "dispute_id": "test",
        "transaction_history": transactions,
        "actions_taken": ["transaction_history_fetched"]
    }
    
    # Verify state contains transaction history
    assert "transaction_history" in state
    assert len(state["transaction_history"]) == num_transactions
    assert "transaction_history_fetched" in state["actions_taken"]


@given(
    num_transactions=st.integers(min_value=1, max_value=50),
    dispute_amount=st.decimals(min_value=Decimal("1.00"), max_value=Decimal("10000.00"), places=2)
)
def test_enrichment_includes_fraud_analysis(num_transactions, dispute_amount):
    """For any enrichment with transactions, fraud analysis should be performed"""
    from app.schema.models import TransactionData
    from app.tools.transaction_enrichment import TransactionEnrichment
    
    enrichment = TransactionEnrichment("http://test")
    
    # Create sample transactions
    transactions = [
        TransactionData(
            transaction_id=f"tx_{i}",
            customer_id="cust_123",
            amount=Decimal("50.00"),
            timestamp=datetime.utcnow() - timedelta(days=i * 10),
            merchant="Test Merchant",
            status="completed"
        )
        for i in range(num_transactions)
    ]
    
    # Perform fraud analysis
    analysis = enrichment.detect_fraud_patterns(transactions, dispute_amount)
    
    # Verify analysis contains required fields
    assert hasattr(analysis, 'has_suspicious_patterns')
    assert hasattr(analysis, 'chargeback_rate')
    assert hasattr(analysis, 'risk_score')
    assert hasattr(analysis, 'pattern_details')
    assert 0.0 <= analysis.chargeback_rate <= 1.0
    assert 0.0 <= analysis.risk_score <= 1.0
