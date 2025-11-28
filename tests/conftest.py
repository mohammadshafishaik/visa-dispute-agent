"""Pytest configuration and fixtures"""
import pytest
from hypothesis import settings

# Configure Hypothesis
settings.register_profile("default", max_examples=100, deadline=5000)
settings.load_profile("default")


@pytest.fixture
def sample_dispute_payload():
    """Sample dispute webhook payload"""
    return {
        "dispute_id": "disp_123",
        "customer_id": "cust_456",
        "transaction_id": "txn_789",
        "amount": "150.00",
        "currency": "USD",
        "reason_code": "10.4",
        "description": "Customer claims unauthorized transaction",
        "timestamp": "2024-01-15T10:30:00Z"
    }


@pytest.fixture
def sample_dispute_state():
    """Sample dispute state for testing"""
    return {
        "dispute_id": "disp_123",
        "payload": {
            "dispute_id": "disp_123",
            "customer_id": "cust_456",
            "transaction_id": "txn_789",
            "amount": "150.00",
            "currency": "USD",
            "reason_code": "10.4",
            "description": "Customer claims unauthorized transaction"
        },
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
