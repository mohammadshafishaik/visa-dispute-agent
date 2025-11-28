"""Property-based tests for confidence-based routing"""
from hypothesis import given, strategies as st
from app.schema.models import DisputeDecision
from app.schema.state import DisputeState
from app.agents.dispute_graph import route_by_confidence


# Feature: visa-dispute-agent, Property 12: Confidence-based routing
@given(st.floats(min_value=0.0, max_value=1.0))
def test_confidence_routing_threshold(confidence_score: float):
    """For any confidence score, routing should match threshold logic (0.85)"""
    state: DisputeState = {
        "dispute_id": "test-123",
        "payload": {},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": None,
        "query_attempts": 0,
        "decision": DisputeDecision(
            dispute_id="test-123",
            decision="accept",
            confidence_score=confidence_score,
            reasoning="Test reasoning",
            supporting_rules=["rule1"],
            recommended_action="test"
        ),
        "confidence_score": confidence_score,
        "actions_taken": [],
        "error": None,
        "current_node": "adjudication"
    }
    
    next_node = route_by_confidence(state)
    
    if confidence_score < 0.85:
        assert next_node == "human_review", f"Expected human_review for confidence {confidence_score}, got {next_node}"
    else:
        assert next_node == "action", f"Expected action for confidence {confidence_score}, got {next_node}"


@given(st.floats(min_value=0.85, max_value=1.0))
def test_high_confidence_routes_to_action(confidence_score: float):
    """For any confidence score >= 0.85, should route to action node"""
    state: DisputeState = {
        "dispute_id": "test-high",
        "payload": {},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": None,
        "query_attempts": 0,
        "decision": None,
        "confidence_score": confidence_score,
        "actions_taken": [],
        "error": None,
        "current_node": "adjudication"
    }
    
    result = route_by_confidence(state)
    assert result == "action"


@given(st.floats(min_value=0.0, max_value=0.849))
def test_low_confidence_routes_to_human_review(confidence_score: float):
    """For any confidence score < 0.85, should route to human review"""
    state: DisputeState = {
        "dispute_id": "test-low",
        "payload": {},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": None,
        "query_attempts": 0,
        "decision": None,
        "confidence_score": confidence_score,
        "actions_taken": [],
        "error": None,
        "current_node": "adjudication"
    }
    
    result = route_by_confidence(state)
    assert result == "human_review"
