"""ChromaDB vector store management"""
import chromadb
import os
from chromadb.config import Settings
from typing import List, Optional
from app.schema.models import Document


class VectorStore:
    """Manages ChromaDB vector store for Visa rules"""
    
    def __init__(self, host: str = None, port: int = None) -> None:
        # Use environment variables if not provided
        if host is None:
            host = os.getenv("CHROMADB_HOST", "localhost")
        if port is None:
            port = int(os.getenv("CHROMADB_PORT", "8000"))
            
        self.client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection_name = "visa_rules"
        self.collection: Optional[chromadb.Collection] = None
    
    def initialize(self) -> None:
        """Initialize or get the Visa rules collection"""
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Visa regulations and dispute resolution rules"}
        )
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[dict],
        ids: List[str]
    ) -> None:
        """Add documents to the collection"""
        if not self.collection:
            raise RuntimeError("Collection not initialized")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(
        self,
        query_text: str,
        top_k: int = 5
    ) -> tuple[List[str], List[dict], List[float]]:
        """Query the collection for relevant documents"""
        if not self.collection:
            raise RuntimeError("Collection not initialized")
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        
        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []
        
        # Convert distances to similarity scores (1 - normalized distance)
        similarity_scores = [1.0 - (d / 2.0) for d in distances]
        
        return documents, metadatas, similarity_scores
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        if not self.collection:
            raise RuntimeError("Collection not initialized")
        return self.collection.count()


# Global vector store instance (lazy initialization)
_vector_store_instance = None

def get_vector_store() -> VectorStore:
    """Get or create the global vector store instance"""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance

# For backward compatibility
vector_store = None  # Will be initialized on first use
