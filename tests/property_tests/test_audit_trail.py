"""Property-based tests for audit trail completeness"""
import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from unittest.mock import AsyncMock, patch


# Feature: visa-dispute-agent, Property 3: Audit trail completeness
@given(
    dispute_id=st.text(min_size=1, max_size=50),
    node_name=st.sampled_from(["input_node", "enrichment_node", "legal_research_node", 
                                "adjudication_node", "action_node", "human_review_node"])
)
@pytest.mark.asyncio
async def test_every_node_entry_is_logged(dispute_id, node_name):
    """For any dispute entering any node, an audit log entry should be created"""
    from app.db.audit_logger import audit_logger
    
    # Mock the database execute
    with patch('app.db.connection.db_pool.execute', new_callable=AsyncMock) as mock_execute:
        # Log node entry
        await audit_logger.log_node_entry(
            dispute_id=dispute_id,
            node_name=node_name,
            state={"test": "data"}
        )
        
        # Verify execute was called
        assert mock_execute.called
        call_args = mock_execute.call_args[0]
        
        # Verify the query contains INSERT into audit_log
        assert "INSERT INTO audit_log" in call_args[0]
        # Verify dispute_id and node_name are in the call
        assert dispute_id in call_args
        assert node_name in call_args


# Feature: visa-dispute-agent, Property 3: Audit trail completeness (decisions)
@given(
    dispute_id=st.text(min_size=1, max_size=50),
    confidence_score=st.floats(min_value=0.0, max_value=1.0),
    reasoning=st.text(min_size=20, max_size=500)
)
@pytest.mark.asyncio
async def test_every_decision_is_logged(dispute_id, confidence_score, reasoning):
    """For any decision made, it should be logged with reasoning and confidence"""
    from app.db.audit_logger import audit_logger
    from app.schema.models import DisputeDecision
    
    decision = DisputeDecision(
        dispute_id=dispute_id,
        decision="accept",
        confidence_score=confidence_score,
        reasoning=reasoning,
        supporting_rules=["rule1"],
        recommended_action="test"
    )
    
    with patch('app.db.connection.db_pool.execute', new_callable=AsyncMock) as mock_execute:
        await audit_logger.log_decision(dispute_id, decision)
        
        assert mock_execute.called
        call_args = mock_execute.call_args[0]
        
        # Verify decision details are logged
        assert "INSERT INTO audit_log" in call_args[0]
        assert dispute_id in call_args
        assert reasoning in call_args
        assert confidence_score in call_args


# Feature: visa-dispute-agent, Property 3: Audit trail completeness (actions)
@given(
    dispute_id=st.text(min_size=1, max_size=50),
    action_type=st.sampled_from(["email_sent", "sms_sent", "webhook_called"])
)
@pytest.mark.asyncio
async def test_every_action_is_logged(dispute_id, action_type):
    """For any action taken, it should be logged with metadata"""
    from app.db.audit_logger import audit_logger
    
    metadata = {
        "recipient": "test@example.com",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    with patch('app.db.connection.db_pool.execute', new_callable=AsyncMock) as mock_execute:
        await audit_logger.log_action(dispute_id, action_type, metadata)
        
        assert mock_execute.called
        call_args = mock_execute.call_args[0]
        
        # Verify action is logged
        assert "INSERT INTO audit_log" in call_args[0]
        assert dispute_id in call_args
        assert action_type in call_args
