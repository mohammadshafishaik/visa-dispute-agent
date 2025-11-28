"""Human review queue management"""
import json
from datetime import datetime
from typing import Any, Dict, List
from app.db.connection import db_pool
from app.schema.models import DisputeDecision, HumanReviewCase


async def add_to_review_queue(
    dispute_id: str,
    decision: DisputeDecision | Dict[str, Any],
    payload: Dict[str, Any]
) -> None:
    """Add a dispute to the human review queue"""
    # Handle both DisputeDecision object and dict
    if isinstance(decision, dict):
        confidence_score = decision.get("confidence_score", 0.0)
        decision_value = decision.get("decision", "escalate")
        reasoning = decision.get("reasoning", "") or "Requires human review for final determination"
        supporting_rules = decision.get("supporting_rules", [])
    else:
        confidence_score = decision.confidence_score
        decision_value = decision.decision
        reasoning = decision.reasoning
        supporting_rules = decision.supporting_rules
    
    query = """
        INSERT INTO human_review_queue (
            dispute_id, confidence_score, decision, reasoning,
            supporting_rules, status, payload, created_at, updated_at
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (dispute_id) DO UPDATE SET
            confidence_score = EXCLUDED.confidence_score,
            decision = EXCLUDED.decision,
            reasoning = EXCLUDED.reasoning,
            supporting_rules = EXCLUDED.supporting_rules,
            updated_at = EXCLUDED.updated_at
    """
    await db_pool.execute(
        query,
        dispute_id,
        confidence_score,
        decision_value,
        reasoning,
        json.dumps(supporting_rules),
        "pending_review",
        json.dumps(payload),
        datetime.utcnow(),
        datetime.utcnow()
    )


async def get_pending_reviews() -> List[HumanReviewCase]:
    """Retrieve all pending human review cases"""
    query = """
        SELECT dispute_id, confidence_score, decision, reasoning,
               supporting_rules, status, created_at
        FROM human_review_queue
        WHERE status = 'pending_review'
        ORDER BY created_at ASC
    """
    rows = await db_pool.fetch(query)
    
    return [
        HumanReviewCase(
            dispute_id=row["dispute_id"],
            confidence_score=float(row["confidence_score"]),
            decision=row["decision"],
            reasoning=row["reasoning"],
            supporting_rules=json.loads(row["supporting_rules"]) if row["supporting_rules"] else [],
            status=row["status"],
            created_at=row["created_at"]
        )
        for row in rows
    ]


async def update_review_status(
    dispute_id: str,
    status: str,
    reviewed_by: str
) -> None:
    """Update the status of a review case"""
    query = """
        UPDATE human_review_queue
        SET status = $1, reviewed_by = $2, reviewed_at = $3, updated_at = $4
        WHERE dispute_id = $5
    """
    await db_pool.execute(
        query,
        status,
        reviewed_by,
        datetime.utcnow(),
        datetime.utcnow(),
        dispute_id
    )
