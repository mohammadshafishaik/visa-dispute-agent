"""Property-based tests for similarity-based routing"""
from hypothesis import given, strategies as st
from app.schema.state import DisputeState
from app.agents.dispute_graph import should_rewrite_query


# Feature: visa-dispute-agent, Property 9: Self-reflective query rewriting
@given(
    st.lists(st.floats(min_value=0.0, max_value=0.69), min_size=1, max_size=10),
    st.integers(min_value=0, max_value=2)
)
def test_low_similarity_triggers_rewrite(similarity_scores: list, query_attempts: int):
    """For any retrieval with all scores < 0.7 and attempts < 3, query should be rewritten"""
    state: DisputeState = {
        "dispute_id": "test-rewrite",
        "payload": {},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": similarity_scores,
        "query_attempts": query_attempts,
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": None,
        "current_node": "legal_research"
    }
    
    result = should_rewrite_query(state)
    
    if query_attempts < 3:
        assert result == "rewrite", f"Expected rewrite for attempts={query_attempts}, got {result}"
    else:
        assert result == "escalate", f"Expected escalate for attempts={query_attempts}, got {result}"


# Feature: visa-dispute-agent, Property 10: High-quality retrieval progression
@given(
    st.lists(st.floats(min_value=0.7, max_value=1.0), min_size=1, max_size=10)
)
def test_high_similarity_proceeds_to_adjudication(similarity_scores: list):
    """For any retrieval with at least one score >= 0.7, should proceed to adjudication"""
    state: DisputeState = {
        "dispute_id": "test-proceed",
        "payload": {},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": similarity_scores,
        "query_attempts": 1,
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": None,
        "current_node": "legal_research"
    }
    
    result = should_rewrite_query(state)
    assert result == "proceed"


@given(
    st.lists(st.floats(min_value=0.0, max_value=0.69), min_size=1, max_size=10)
)
def test_max_attempts_exhausted_escalates(similarity_scores: list):
    """For any retrieval with low scores after 3 attempts, should escalate"""
    state: DisputeState = {
        "dispute_id": "test-escalate",
        "payload": {},
        "transaction_history": None,
        "retrieved_rules": None,
        "similarity_scores": similarity_scores,
        "query_attempts": 3,
        "decision": None,
        "confidence_score": None,
        "actions_taken": [],
        "error": None,
        "current_node": "legal_research"
    }
    
    result = should_rewrite_query(state)
    assert result == "escalate"
