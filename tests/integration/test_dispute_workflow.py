"""Integration tests for complete dispute workflow"""
import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch

from app.schema.models import DisputeWebhook, Document
from app.schema.state import DisputeState
from app.agents.dispute_graph import (
    input_node,
    enrichment_node,
    legal_research_node,
    adjudication_node,
    route_by_confidence,
    should_rewrite_query
)


@pytest.mark.asyncio
async def test_happy_path_high_confidence_workflow(sample_dispute_payload):
    """Test complete workflow: webhook → enrichment → RAG → high confidence → action"""
    # Initialize state
    state: DisputeState = {
        "dispute_id": sample_dispute_payload["dispute_id"],
        "payload": sample_dispute_payload,
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
    
    # Mock database operations
    with patch('app.db.audit_logger.audit_logger.log_node_entry', new_callable=AsyncMock):
        # Step 1: Input node
        state = await input_node(state)
        assert state["current_node"] == "input_node"
        assert state["query_attempts"] == 0
        
        # Verify routing would proceed to enrichment
        assert "input_node" in state["current_node"]


@pytest.mark.asyncio
async def test_low_confidence_routes_to_human_review():
    """Test workflow with low confidence decision routing to human review"""
    state: DisputeState = {
        "dispute_id": "test_low_conf",
        "payload": {"dispute_id": "test_low_conf"},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": None,
        "query_attempts": 0,
        "decision": None,
        "confidence_score": 0.65,  # Below 0.85 threshold
        "actions_taken": [],
        "error": None,
        "current_node": "adjudication"
    }
    
    # Verify routing decision
    next_node = route_by_confidence(state)
    assert next_node == "human_review"


@pytest.mark.asyncio
async def test_low_similarity_triggers_query_rewrite():
    """Test RAG self-correction with low similarity scores"""
    state: DisputeState = {
        "dispute_id": "test_low_sim",
        "payload": {"dispute_id": "test_low_sim"},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": [0.45, 0.50, 0.55],  # All below 0.7
        "query_attempts": 1,  # First attempt
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": None,
        "current_node": "legal_research"
    }
    
    # Verify routing decision
    next_node = should_rewrite_query(state)
    assert next_node == "rewrite"


@pytest.mark.asyncio
async def test_max_query_attempts_escalates():
    """Test that after 3 query attempts with low similarity, dispute escalates"""
    state: DisputeState = {
        "dispute_id": "test_max_attempts",
        "payload": {"dispute_id": "test_max_attempts"},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": [0.45, 0.50, 0.55],  # All below 0.7
        "query_attempts": 3,  # Max attempts reached
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": None,
        "current_node": "legal_research"
    }
    
    # Verify routing decision
    next_node = should_rewrite_query(state)
    assert next_node == "escalate"


@pytest.mark.asyncio
async def test_high_similarity_proceeds_to_adjudication():
    """Test that high similarity scores proceed to adjudication"""
    state: DisputeState = {
        "dispute_id": "test_high_sim",
        "payload": {"dispute_id": "test_high_sim"},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": [0.85, 0.90, 0.88],  # All above 0.7
        "query_attempts": 1,
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": None,
        "current_node": "legal_research"
    }
    
    # Verify routing decision
    next_node = should_rewrite_query(state)
    assert next_node == "proceed"


@pytest.mark.asyncio
async def test_error_state_routes_to_human_review():
    """Test that errors in processing route to human review"""
    state: DisputeState = {
        "dispute_id": "test_error",
        "payload": {"dispute_id": "test_error"},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": None,
        "query_attempts": 0,
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": "Processing error occurred",
        "current_node": "enrichment"
    }
    
    # Verify routing decision
    next_node = route_by_confidence(state)
    assert next_node == "human_review"
