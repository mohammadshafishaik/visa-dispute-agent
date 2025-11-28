"""FastAPI server and endpoints"""
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.schema.models import (
    DisputeWebhook,
    DisputeResponse,
    DisputeStatus,
    HumanReviewCase
)
from app.agents.dispute_graph import dispute_graph
from app.db.connection import db_pool
from app.db.vector_store import get_vector_store
from app.db.human_review import get_pending_reviews
from app.config.settings import settings
from app.api.monitoring import router as monitoring_router
from app.api.web_ui import router as web_ui_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    # Startup
    await db_pool.connect(settings.database_url)
    vector_store = get_vector_store()
    vector_store.initialize()
    
    yield
    
    # Shutdown
    await db_pool.close()


app = FastAPI(
    title="Visa Dispute Agent",
    description="Event-Driven Autonomous Agent for Visa Dispute Resolution",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(monitoring_router)
app.include_router(web_ui_router)


@app.post("/webhooks/dispute", response_model=DisputeResponse, status_code=status.HTTP_202_ACCEPTED)
async def receive_dispute(request: Request, payload: DisputeWebhook) -> DisputeResponse:
    """Receive dispute webhook and initiate processing with bank-style validation"""
    from app.api.security import check_rate_limit
    from app.tools.rejection_rules import bank_rejection_rules
    
    # Check rate limit
    await check_rate_limit(request)
    
    try:
        # Bank-style validation - reject immediately if invalid
        payload_dict = payload.model_dump(mode='json')
        is_valid, rejection_code, rejection_message = bank_rejection_rules.validate_dispute(payload_dict)
        
        if not is_valid:
            # Log rejection
            from app.db.audit_logger import audit_logger
            await audit_logger.log_error(
                payload.dispute_id,
                "validation",
                f"[{rejection_code}] {rejection_message}",
                {"payload": payload_dict}
            )
            
            # Return rejection response with 200 status (not an error, just a rejection)
            return DisputeResponse(
                status="rejected",
                dispute_id=payload.dispute_id,
                message=f"[{rejection_code}] {rejection_message}",
                rejection_code=rejection_code
            )
        
        # Create initial state
        initial_state = {
            "dispute_id": payload.dispute_id,
            "payload": payload_dict,
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
        
        # Invoke the state graph (async execution)
        # In production, this should be queued for background processing
        result = await dispute_graph.ainvoke(initial_state)
        
        return DisputeResponse(
            status="accepted",
            dispute_id=payload.dispute_id,
            message="Dispute received and processing initiated"
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@app.get("/disputes/{dispute_id}", response_model=DisputeStatus)
async def get_dispute_status(dispute_id: str) -> DisputeStatus:
    """Query dispute status"""
    query = """
        SELECT dispute_id, final_decision, confidence_score, status, created_at, updated_at
        FROM dispute_history
        WHERE dispute_id = $1
    """
    
    row = await db_pool.fetchrow(query, dispute_id)
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispute {dispute_id} not found"
        )
    
    return DisputeStatus(
        dispute_id=row["dispute_id"],
        current_node="completed",
        status=row["status"],
        confidence_score=float(row["confidence_score"]) if row["confidence_score"] else None,
        decision=row["final_decision"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )


@app.get("/review-queue", response_model=List[HumanReviewCase])
async def get_review_queue() -> List[HumanReviewCase]:
    """List cases pending human review"""
    return await get_pending_reviews()


@app.get("/health")
async def health_check() -> dict:
    """System health check"""
    try:
        # Check database connection
        await db_pool.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    try:
        # Check ChromaDB connection
        vector_store = get_vector_store()
        count = vector_store.get_collection_count()
        vector_status = f"healthy ({count} documents)"
    except Exception as e:
        vector_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" and "healthy" in vector_status else "degraded",
        "database": db_status,
        "vector_store": vector_status,
        "version": "0.1.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
