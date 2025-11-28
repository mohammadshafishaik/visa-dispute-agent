"""Database connection management"""
import asyncpg
from typing import Optional


class DatabasePool:
    """Manages PostgreSQL connection pool"""
    
    def __init__(self) -> None:
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self, database_url: str) -> None:
        """Initialize connection pool"""
        self.pool = await asyncpg.create_pool(
            database_url,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
    
    async def close(self) -> None:
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
    
    async def execute(self, query: str, *args: any) -> str:
        """Execute a query without returning results"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args: any) -> list:
        """Execute a query and return all results"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def fetchrow(self, query: str, *args: any) -> Optional[asyncpg.Record]:
        """Execute a query and return a single row"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)


# Global database pool instance
db_pool = DatabasePool()
