"""Property-based tests for webhook validation"""
import pytest
from datetime import datetime
from decimal import Decimal
from hypothesis import given, strategies as st
from pydantic import ValidationError

from app.schema.models import DisputeWebhook


# Hypothesis strategies for generating test data
@st.composite
def valid_dispute_webhook(draw):
    """Generate valid DisputeWebhook instances"""
    return DisputeWebhook(
        dispute_id=draw(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        customer_id=draw(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        transaction_id=draw(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        amount=draw(st.decimals(min_value=Decimal("0.01"), max_value=Decimal("100000"), places=2)),
        currency=draw(st.sampled_from(["USD", "EUR", "GBP", "JPY"])),
        reason_code=draw(st.sampled_from(["10.1", "10.4", "11.1", "12.1", "13.1", "13.2", "13.3"])),
        description=draw(st.text(min_size=10, max_size=500)),
        timestamp=draw(st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2025, 12, 31)))
    )


# Feature: visa-dispute-agent, Property 1: Webhook payload validation
@given(valid_dispute_webhook())
def test_valid_webhooks_are_accepted(webhook: DisputeWebhook):
    """For any valid webhook conforming to DisputeWebhook schema, it should be successfully parsed"""
    # If we got here, the webhook was successfully created and validated
    assert webhook.dispute_id is not None
    assert webhook.customer_id is not None
    assert webhook.transaction_id is not None
    assert webhook.amount > 0
    assert webhook.currency in ["USD", "EUR", "GBP", "JPY"]
    assert len(webhook.description) >= 10


@given(
    dispute_id=st.one_of(st.none(), st.just("")),
    customer_id=st.text(min_size=1, max_size=50),
    transaction_id=st.text(min_size=1, max_size=50),
    amount=st.decimals(min_value=Decimal("0.01"), max_value=Decimal("100000"), places=2),
    currency=st.sampled_from(["USD", "EUR", "GBP"]),
    reason_code=st.sampled_from(["10.4", "13.1"]),
    description=st.text(min_size=10, max_size=500),
    timestamp=st.datetimes(min_value=datetime(2020, 1, 1))
)
def test_invalid_dispute_id_raises_validation_error(
    dispute_id, customer_id, transaction_id, amount, currency, reason_code, description, timestamp
):
    """For any webhook with invalid dispute_id, validation should fail"""
    with pytest.raises(ValidationError):
        DisputeWebhook(
            dispute_id=dispute_id,
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            reason_code=reason_code,
            description=description,
            timestamp=timestamp
        )


@given(
    dispute_id=st.text(min_size=1, max_size=50),
    customer_id=st.text(min_size=1, max_size=50),
    transaction_id=st.text(min_size=1, max_size=50),
    amount=st.one_of(st.decimals(max_value=Decimal("-0.01")), st.decimals(min_value=Decimal("0"), max_value=Decimal("0"))),
    currency=st.sampled_from(["USD", "EUR"]),
    reason_code=st.sampled_from(["10.4", "13.1"]),
    description=st.text(min_size=10, max_size=500),
    timestamp=st.datetimes(min_value=datetime(2020, 1, 1))
)
def test_invalid_amount_raises_validation_error(
    dispute_id, customer_id, transaction_id, amount, currency, reason_code, description, timestamp
):
    """For any webhook with non-positive amount, validation should fail"""
    with pytest.raises((ValidationError, ValueError)):
        DisputeWebhook(
            dispute_id=dispute_id,
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            reason_code=reason_code,
            description=description,
            timestamp=timestamp
        )
