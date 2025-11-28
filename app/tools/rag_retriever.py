"""RAG retriever tool with self-reflective query rewriting"""
from typing import List, Union
from app.db.vector_store import get_vector_store
from app.schema.models import Document, RetrievalResult


class RAGRetriever:
    """Retrieves relevant Visa rules using RAG with self-correction"""
    
    def __init__(self, llm, similarity_threshold: float = 0.7) -> None:
        self.llm = llm
        self.similarity_threshold = similarity_threshold
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> RetrievalResult:
        """Retrieve relevant documents with similarity scores"""
        vector_store = get_vector_store()
        documents, metadatas, similarity_scores = vector_store.query(query, top_k)
        
        doc_objects = [
            Document(
                content=doc,
                metadata=meta,
                similarity_score=score
            )
            for doc, meta, score in zip(documents, metadatas, similarity_scores)
        ]
        
        avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
        
        return RetrievalResult(
            documents=doc_objects,
            query=query,
            average_similarity=avg_similarity
        )
    
    async def rewrite_query(
        self,
        original_query: str,
        attempt: int,
        dispute_context: dict
    ) -> str:
        """Generate alternative query formulation based on attempt number"""
        if attempt == 1:
            # Strategy 1: Extract key entities and use synonyms
            prompt = f"""Given this dispute query: "{original_query}"
            
Rewrite it to focus on key entities and use alternative terminology.
Extract the main dispute reason, amount context, and relevant Visa regulation categories.

Provide only the rewritten query, no explanation."""
            
        elif attempt == 2:
            # Strategy 2: Use broader category-based query
            prompt = f"""Given this dispute query: "{original_query}"
            
Rewrite it using broader Visa dispute categories and regulation types.
Focus on the general dispute category rather than specific details.
Include terms like "chargeback", "fraud", "authorization", "processing error" as relevant.

Provide only the rewritten query, no explanation."""
            
        else:
            # Strategy 3: Use reason code and regulatory framework
            reason_code = dispute_context.get("reason_code", "")
            prompt = f"""Given this dispute with reason code {reason_code}: "{original_query}"
            
Rewrite the query to focus on Visa reason code {reason_code} regulations and related dispute resolution procedures.
Use formal regulatory language and reference Visa dispute resolution framework.

Provide only the rewritten query, no explanation."""
        
        response = await self.llm.ainvoke(prompt)
        return response.content.strip()
    
    def evaluate_retrieval_quality(self, result: RetrievalResult) -> bool:
        """Determine if retrieval quality is sufficient"""
        return result.average_similarity >= self.similarity_threshold
    
    async def retrieve_with_self_correction(
        self,
        initial_query: str,
        dispute_context: dict,
        max_attempts: int = 3,
        top_k: int = 5
    ) -> tuple[RetrievalResult, int]:
        """Retrieve with automatic query rewriting if quality is low"""
        query = initial_query
        
        for attempt in range(max_attempts):
            result = await self.retrieve(query, top_k)
            
            if self.evaluate_retrieval_quality(result):
                return result, attempt + 1
            
            # If not the last attempt, rewrite the query
            if attempt < max_attempts - 1:
                query = await self.rewrite_query(initial_query, attempt + 1, dispute_context)
        
        # Return the last result even if quality is low
        return result, max_attempts
