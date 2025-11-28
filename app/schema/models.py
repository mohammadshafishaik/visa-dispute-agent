"""Pydantic schemas for data validation"""
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class DisputeWebhook(BaseModel):
    """Schema for incoming dispute webhook payloads"""
    dispute_id: str = Field(..., description="Unique dispute identifier")
    customer_id: str = Field(..., description="Customer identifier")
    transaction_id: str = Field(..., description="Transaction identifier")
    amount: Decimal = Field(..., description="Dispute amount")
    currency: str = Field(..., description="Currency code (e.g., USD)")
    reason_code: str = Field(..., description="Visa reason code")
    description: str = Field(..., description="Dispute description")
    timestamp: datetime = Field(..., description="Dispute creation timestamp")
    
    # Optional fields for email and customer details
    customer_email: Optional[str] = Field(None, description="Customer email address")
    customer_name: Optional[str] = Field(None, description="Customer full name")
    customer_phone: Optional[str] = Field(None, description="Customer phone number")
    transaction_date: Optional[str] = Field(None, description="Transaction date")
    merchant_name: Optional[str] = Field(None, description="Merchant name")
    card_number: Optional[str] = Field(None, description="Card number (last 4 digits)")


class DisputeDecision(BaseModel):
    """Schema for adjudication decisions"""
    dispute_id: str = Field(..., description="Unique dispute identifier")
    decision: Literal["accept", "reject", "escalate"] = Field(..., description="Decision type")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    reasoning: str = Field(..., description="Explanation for the decision")
    supporting_rules: List[str] = Field(..., description="List of relevant Visa rule references")
    recommended_action: str = Field(..., description="Recommended next action")


class TransactionData(BaseModel):
    """Schema for transaction history records"""
    transaction_id: str = Field(..., description="Transaction identifier")
    customer_id: str = Field(..., description="Customer identifier")
    amount: Decimal = Field(..., description="Transaction amount")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    merchant: str = Field(..., description="Merchant name")
    status: str = Field(..., description="Transaction status")


class FraudAnalysis(BaseModel):
    """Schema for fraud pattern analysis results"""
    has_suspicious_patterns: bool = Field(..., description="Whether suspicious patterns detected")
    chargeback_rate: float = Field(..., ge=0.0, le=1.0, description="Historical chargeback rate")
    pattern_details: List[str] = Field(default_factory=list, description="Detected pattern details")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Overall risk score")


class Document(BaseModel):
    """Schema for retrieved documents from RAG"""
    content: str = Field(..., description="Document text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")


class RetrievalResult(BaseModel):
    """Schema for RAG retrieval results"""
    documents: List[Document] = Field(..., description="Retrieved documents")
    query: str = Field(..., description="Search query used")
    average_similarity: float = Field(..., ge=0.0, le=1.0, description="Average similarity score")


class DisputeResponse(BaseModel):
    """Schema for API responses"""
    status: Literal["accepted", "rejected", "processing"] = Field(..., description="Response status")
    dispute_id: str = Field(..., description="Dispute identifier")
    message: str = Field(..., description="Response message")
    rejection_code: Optional[str] = Field(None, description="Rejection code if status is rejected")


class DisputeStatus(BaseModel):
    """Schema for dispute status queries"""
    dispute_id: str
    current_node: str
    status: str
    confidence_score: Optional[float] = None
    decision: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class HumanReviewCase(BaseModel):
    """Schema for human review queue entries"""
    dispute_id: str
    confidence_score: float
    decision: str
    reasoning: str
    supporting_rules: List[str]
    status: Literal["pending_review", "in_review", "resolved"]
    created_at: datetime
