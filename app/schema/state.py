"""LangGraph state definitions"""
from typing import Any, Dict, List, Optional, TypedDict
from app.schema.models import DisputeDecision, Document, TransactionData


class DisputeState(TypedDict):
    """State definition for LangGraph dispute processing workflow"""
    dispute_id: str
    payload: Dict[str, Any]
    transaction_history: Optional[List[TransactionData]]
    retrieved_rules: Optional[List[Document]]
    similarity_scores: Optional[List[float]]
    query_attempts: int
    decision: Optional[DisputeDecision]
    confidence_score: Optional[float]
    actions_taken: List[str]
    error: Optional[str]
    current_node: str
