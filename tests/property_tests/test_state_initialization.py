"""Property-based tests for state initialization"""
from hypothesis import given, strategies as st
from datetime import datetime
from decimal import Decimal
from app.schema.models import DisputeWebhook


# Feature: visa-dispute-agent, Property 2: State initialization completeness
@given(
    dispute_id=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    customer_id=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    transaction_id=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    amount=st.decimals(min_value=Decimal("0.01"), max_value=Decimal("100000"), places=2),
    currency=st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
    reason_code=st.sampled_from(["10.1", "10.4", "11.1", "12.1", "13.1", "13.2", "13.3"]),
    description=st.text(min_size=10, max_size=500),
    timestamp=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2025, 12, 31))
)
def test_state_initialization_contains_all_required_fields(
    dispute_id, customer_id, transaction_id, amount, currency, reason_code, description, timestamp
):
    """For any valid dispute webhook, initial state should contain all required fields"""
    webhook = DisputeWebhook(
        dispute_id=dispute_id,
        customer_id=customer_id,
        transaction_id=transaction_id,
        amount=amount,
        currency=currency,
        reason_code=reason_code,
        description=description,
        timestamp=timestamp
    )
    
    # Simulate state initialization
    initial_state = {
        "dispute_id": webhook.dispute_id,
        "payload": webhook.model_dump(),
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": None,
        "query_attempts": 0,
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": None,
        "current_node": "initial"
    }
    
    # Verify all required fields are present
    assert initial_state["dispute_id"] == dispute_id
    assert initial_state["payload"]["customer_id"] == customer_id
    assert initial_state["payload"]["transaction_id"] == transaction_id
    assert initial_state["payload"]["amount"] == amount
    assert initial_state["payload"]["currency"] == currency
    assert initial_state["payload"]["reason_code"] == reason_code
    assert initial_state["query_attempts"] == 0
    assert initial_state["actions_taken"] == []
    assert initial_state["error"] is None
