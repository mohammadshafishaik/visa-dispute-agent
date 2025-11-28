"""Unit tests for RAG retriever"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.tools.rag_retriever import RAGRetriever
from app.schema.models import Document, RetrievalResult


@pytest.fixture
def mock_llm():
    """Create a mock LLM"""
    llm = AsyncMock()
    llm.ainvoke = AsyncMock()
    return llm


@pytest.fixture
def rag_retriever(mock_llm):
    """Create RAG retriever with mock LLM"""
    return RAGRetriever(mock_llm, similarity_threshold=0.7)


def test_evaluate_retrieval_quality_high(rag_retriever):
    """Verify high similarity scores pass quality check"""
    result = RetrievalResult(
        documents=[
            Document(content="Rule 1", metadata={}, similarity_score=0.85),
            Document(content="Rule 2", metadata={}, similarity_score=0.90)
        ],
        query="test query",
        average_similarity=0.875
    )
    
    assert rag_retriever.evaluate_retrieval_quality(result) is True


def test_evaluate_retrieval_quality_low(rag_retriever):
    """Verify low similarity scores fail quality check"""
    result = RetrievalResult(
        documents=[
            Document(content="Rule 1", metadata={}, similarity_score=0.50),
            Document(content="Rule 2", metadata={}, similarity_score=0.60)
        ],
        query="test query",
        average_similarity=0.55
    )
    
    assert rag_retriever.evaluate_retrieval_quality(result) is False


def test_evaluate_retrieval_quality_threshold(rag_retriever):
    """Verify exact threshold value"""
    result = RetrievalResult(
        documents=[
            Document(content="Rule 1", metadata={}, similarity_score=0.70)
        ],
        query="test query",
        average_similarity=0.70
    )
    
    assert rag_retriever.evaluate_retrieval_quality(result) is True


@pytest.mark.asyncio
async def test_rewrite_query_different_strategies(rag_retriever, mock_llm):
    """Verify different query rewriting strategies"""
    mock_llm.ainvoke.return_value = MagicMock(content="Rewritten query")
    
    original = "dispute chargeback reason code 10.4"
    dispute_context = {"reason_code": "10.4"}
    
    # Test each strategy
    for attempt in [1, 2, 3]:
        rewritten = await rag_retriever.rewrite_query(original, attempt, dispute_context)
        assert rewritten == "Rewritten query"
        assert mock_llm.ainvoke.called
