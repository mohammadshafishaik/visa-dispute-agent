"""Property-based tests for schema validation"""
from hypothesis import given, strategies as st
from decimal import Decimal
from datetime import datetime
from app.schema.models import DisputeDecision, TransactionData


# Feature: visa-dispute-agent, Property 11: Adjudication decision structure
@given(
    dispute_id=st.text(min_size=1, max_size=50),
    decision=st.sampled_from(["accept", "reject", "escalate"]),
    confidence_score=st.floats(min_value=0.0, max_value=1.0),
    reasoning=st.text(min_size=10, max_size=500),
    supporting_rules=st.lists(st.text(min_size=1, max_size=100), min_size=0, max_size=5),
    recommended_action=st.text(min_size=1, max_size=200)
)
def test_dispute_decision_structure(
    dispute_id, decision, confidence_score, reasoning, supporting_rules, recommended_action
):
    """For any adjudication decision, it should conform to DisputeDecision schema"""
    decision_obj = DisputeDecision(
        dispute_id=dispute_id,
        decision=decision,
        confidence_score=confidence_score,
        reasoning=reasoning,
        supporting_rules=supporting_rules,
        recommended_action=recommended_action
    )
    
    # Verify all required fields are present
    assert decision_obj.dispute_id == dispute_id
    assert decision_obj.decision in ["accept", "reject", "escalate"]
    assert 0.0 <= decision_obj.confidence_score <= 1.0
    assert len(decision_obj.reasoning) >= 10
    assert isinstance(decision_obj.supporting_rules, list)
    assert decision_obj.recommended_action is not None


# Feature: visa-dispute-agent, Property 20: Transaction data schema conformance
@given(
    transaction_id=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    customer_id=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    amount=st.decimals(min_value=Decimal("0.01"), max_value=Decimal("100000"), places=2),
    timestamp=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2025, 12, 31)),
    merchant=st.text(min_size=1, max_size=100),
    status=st.sampled_from(["completed", "pending", "chargeback", "refunded"])
)
def test_transaction_data_schema_conformance(
    transaction_id, customer_id, amount, timestamp, merchant, status
):
    """For any transaction data, it should conform to TransactionData schema"""
    transaction = TransactionData(
        transaction_id=transaction_id,
        customer_id=customer_id,
        amount=amount,
        timestamp=timestamp,
        merchant=merchant,
        status=status
    )
    
    # Verify schema conformance
    assert transaction.transaction_id is not None
    assert transaction.customer_id is not None
    assert transaction.amount > 0
    assert isinstance(transaction.timestamp, datetime)
    assert transaction.merchant is not None
    assert transaction.status in ["completed", "pending", "chargeback", "refunded"]


# Feature: visa-dispute-agent, Property 18: Schema validation enforcement
@given(st.floats(min_value=1.01, max_value=2.0))
def test_confidence_score_out_of_range_fails(invalid_score: float):
    """For any confidence score outside [0.0, 1.0], validation should fail"""
    from pydantic import ValidationError
    import pytest
    
    with pytest.raises(ValidationError):
        DisputeDecision(
            dispute_id="test",
            decision="accept",
            confidence_score=invalid_score,
            reasoning="Test reasoning",
            supporting_rules=[],
            recommended_action="test"
        )


@given(st.floats(min_value=-1.0, max_value=-0.01))
def test_negative_confidence_score_fails(invalid_score: float):
    """For any negative confidence score, validation should fail"""
    from pydantic import ValidationError
    import pytest
    
    with pytest.raises(ValidationError):
        DisputeDecision(
            dispute_id="test",
            decision="accept",
            confidence_score=invalid_score,
            reasoning="Test reasoning",
            supporting_rules=[],
            recommended_action="test"
        )
