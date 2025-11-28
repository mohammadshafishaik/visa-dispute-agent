"""Simple in-memory database for testing without Docker"""
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


class SimpleDatabase:
    """In-memory database replacement for testing without PostgreSQL"""
    
    def __init__(self):
        self.audit_log: List[Dict] = []
        self.human_review_queue: List[Dict] = []
        self.dispute_history: List[Dict] = []
    
    async def connect(self, database_url: str) -> None:
        """Initialize (no-op for in-memory)"""
        print("✓ Using in-memory database (no Docker required)")
    
    async def close(self) -> None:
        """Close (no-op for in-memory)"""
        pass
    
    async def execute(self, query: str, *args) -> str:
        """Execute a query"""
        if "INSERT INTO audit_log" in query:
            self.audit_log.append({
                "dispute_id": args[0] if args else None,
                "node_name": args[1] if len(args) > 1 else None,
                "event_type": args[2] if len(args) > 2 else None,
                "timestamp": datetime.utcnow(),
                "data": args[3:] if len(args) > 3 else []
            })
        elif "INSERT INTO human_review_queue" in query:
            self.human_review_queue.append({
                "dispute_id": args[0] if args else None,
                "confidence_score": args[1] if len(args) > 1 else None,
                "decision": args[2] if len(args) > 2 else None,
                "reasoning": args[3] if len(args) > 3 else None,
                "status": "pending_review",
                "created_at": datetime.utcnow()
            })
        return "OK"
    
    async def fetch(self, query: str, *args) -> List[Dict]:
        """Fetch multiple rows"""
        if "FROM human_review_queue" in query:
            return [
                {
                    "dispute_id": item["dispute_id"],
                    "confidence_score": item["confidence_score"],
                    "decision": item["decision"],
                    "reasoning": item["reasoning"],
                    "supporting_rules": "[]",
                    "status": item["status"],
                    "created_at": item["created_at"]
                }
                for item in self.human_review_queue
            ]
        return []
    
    async def fetchrow(self, query: str, *args) -> Optional[Dict]:
        """Fetch single row"""
        return None


# Global simple database instance
db_pool = SimpleDatabase()
