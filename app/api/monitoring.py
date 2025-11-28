"""Monitoring and observability endpoints"""
from fastapi import APIRouter
from typing import Dict, List
from datetime import datetime, timedelta
from app.db.connection import db_pool
from app.tools.circuit_breaker import (
    enrichment_circuit_breaker,
    gmail_circuit_breaker,
    llm_circuit_breaker
)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/metrics")
async def get_metrics() -> Dict:
    """Get system metrics"""
    # Query database for metrics
    query = """
        SELECT 
            COUNT(*) as total_disputes,
            COUNT(CASE WHEN event_type = 'decision_made' THEN 1 END) as decisions_made,
            AVG(CASE WHEN event_type = 'decision_made' THEN confidence_score END) as avg_confidence,
            COUNT(CASE WHEN node_name = 'human_review_node' THEN 1 END) as human_reviews
        FROM audit_log
        WHERE timestamp > NOW() - INTERVAL '24 hours'
    """
    
    try:
        row = await db_pool.fetchrow(query)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "period": "24_hours",
            "disputes": {
                "total": row["total_disputes"] if row else 0,
                "decisions_made": row["decisions_made"] if row else 0,
                "human_reviews": row["human_reviews"] if row else 0,
                "avg_confidence": float(row["avg_confidence"]) if row and row["avg_confidence"] else 0.0
            }
        }
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/circuit-breakers")
async def get_circuit_breakers() -> Dict:
    """Get circuit breaker states"""
    return {
        "enrichment_service": enrichment_circuit_breaker.get_state(),
        "gmail_api": gmail_circuit_breaker.get_state(),
        "llm_api": llm_circuit_breaker.get_state()
    }


@router.get("/review-queue/stats")
async def get_review_queue_stats() -> Dict:
    """Get human review queue statistics"""
    query = """
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN status = 'pending_review' THEN 1 END) as pending,
            COUNT(CASE WHEN status = 'in_review' THEN 1 END) as in_review,
            COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved,
            AVG(confidence_score) as avg_confidence,
            MIN(created_at) as oldest_pending
        FROM human_review_queue
    """
    
    try:
        row = await db_pool.fetchrow(query)
        
        return {
            "total": row["total"] if row else 0,
            "pending": row["pending"] if row else 0,
            "in_review": row["in_review"] if row else 0,
            "resolved": row["resolved"] if row else 0,
            "avg_confidence": float(row["avg_confidence"]) if row and row["avg_confidence"] else 0.0,
            "oldest_pending": row["oldest_pending"].isoformat() if row and row["oldest_pending"] else None
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/rag/quality")
async def get_rag_quality_metrics() -> Dict:
    """Get RAG retrieval quality metrics"""
    query = """
        SELECT 
            AVG((state_data->>'average_similarity')::float) as avg_similarity,
            COUNT(*) as total_retrievals,
            COUNT(CASE WHEN (state_data->>'average_similarity')::float < 0.7 THEN 1 END) as low_quality,
            COUNT(CASE WHEN (state_data->>'average_similarity')::float >= 0.7 THEN 1 END) as high_quality
        FROM audit_log
        WHERE event_type = 'rag_retrieval'
        AND timestamp > NOW() - INTERVAL '24 hours'
        AND state_data->>'average_similarity' IS NOT NULL
    """
    
    try:
        row = await db_pool.fetchrow(query)
        
        return {
            "period": "24_hours",
            "avg_similarity": float(row["avg_similarity"]) if row and row["avg_similarity"] else 0.0,
            "total_retrievals": row["total_retrievals"] if row else 0,
            "low_quality_count": row["low_quality"] if row else 0,
            "high_quality_count": row["high_quality"] if row else 0
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/performance")
async def get_performance_metrics() -> Dict:
    """Get performance metrics"""
    # This would typically integrate with Prometheus or similar
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "note": "Integrate with Prometheus for detailed metrics",
        "endpoints": {
            "/metrics": "Prometheus metrics endpoint (to be implemented)",
            "/health": "Health check endpoint"
        }
    }
