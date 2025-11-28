"""Audit logging functionality"""
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from app.db.connection import db_pool
from app.schema.models import DisputeDecision


class AuditLogger:
    """Handles audit trail logging to PostgreSQL"""
    
    async def log_node_entry(
        self,
        dispute_id: str,
        node_name: str,
        state: Dict[str, Any]
    ) -> None:
        """Log entry into a state graph node"""
        query = """
            INSERT INTO audit_log (dispute_id, node_name, event_type, state_data, timestamp)
            VALUES ($1, $2, $3, $4, $5)
        """
        await db_pool.execute(
            query,
            dispute_id,
            node_name,
            "node_entry",
            json.dumps(state),
            datetime.utcnow()
        )
    
    async def log_decision(
        self,
        dispute_id: str,
        decision: DisputeDecision
    ) -> None:
        """Log adjudication decision"""
        query = """
            INSERT INTO audit_log (
                dispute_id, node_name, event_type, reasoning,
                confidence_score, supporting_evidence, timestamp
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """
        await db_pool.execute(
            query,
            dispute_id,
            "adjudication_node",
            "decision_made",
            decision.reasoning,
            decision.confidence_score,
            json.dumps({"supporting_rules": decision.supporting_rules}),
            datetime.utcnow()
        )
    
    async def log_retrieval(
        self,
        dispute_id: str,
        query_text: str,
        documents: List[Dict[str, Any]],
        similarity_scores: List[float]
    ) -> None:
        """Log RAG retrieval operation"""
        query = """
            INSERT INTO audit_log (
                dispute_id, node_name, event_type, state_data, timestamp
            )
            VALUES ($1, $2, $3, $4, $5)
        """
        await db_pool.execute(
            query,
            dispute_id,
            "legal_research_node",
            "rag_retrieval",
            json.dumps({
                "query": query_text,
                "num_documents": len(documents),
                "similarity_scores": similarity_scores,
                "average_similarity": sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
            }),
            datetime.utcnow()
        )
    
    async def log_action(
        self,
        dispute_id: str,
        action_type: str,
        metadata: Dict[str, Any]
    ) -> None:
        """Log action taken (e.g., email sent)"""
        query = """
            INSERT INTO audit_log (
                dispute_id, node_name, event_type, state_data, timestamp
            )
            VALUES ($1, $2, $3, $4, $5)
        """
        await db_pool.execute(
            query,
            dispute_id,
            "action_node",
            action_type,
            json.dumps(metadata),
            datetime.utcnow()
        )
    
    async def log_error(
        self,
        dispute_id: str,
        node_name: str,
        error_message: str,
        state: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log error occurrence"""
        query = """
            INSERT INTO audit_log (
                dispute_id, node_name, event_type, error_message, state_data, timestamp
            )
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        await db_pool.execute(
            query,
            dispute_id,
            node_name,
            "error",
            error_message,
            json.dumps(state) if state else None,
            datetime.utcnow()
        )


# Global audit logger instance
audit_logger = AuditLogger()
