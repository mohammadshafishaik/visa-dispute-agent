#!/usr/bin/env python3
"""Wait for required services to be ready before starting the application"""
import time
import sys
import os
import psycopg2
import requests
from typing import Tuple


def wait_for_postgres(max_retries: int = 30, delay: int = 2) -> bool:
    """Wait for PostgreSQL to be ready"""
    db_url = os.getenv("DATABASE_URL", "postgresql://visa_user:visa_password@postgres:5432/visa_disputes")
    
    # Parse connection string
    parts = db_url.replace("postgresql://", "").split("@")
    user_pass = parts[0].split(":")
    host_db = parts[1].split("/")
    host_port = host_db[0].split(":")
    
    user = user_pass[0]
    password = user_pass[1]
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 5432
    database = host_db[1]
    
    print(f"Waiting for PostgreSQL at {host}:{port}...")
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connect_timeout=3
            )
            conn.close()
            print(f"✓ PostgreSQL is ready!")
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Attempt {attempt + 1}/{max_retries}: PostgreSQL not ready yet... ({e})")
                time.sleep(delay)
            else:
                print(f"✗ PostgreSQL failed to become ready after {max_retries} attempts")
                return False
    
    return False


def wait_for_chromadb(max_retries: int = 30, delay: int = 2) -> bool:
    """Wait for ChromaDB to be ready"""
    host = os.getenv("CHROMADB_HOST", "localhost")
    port = int(os.getenv("CHROMADB_PORT", "8000"))
    
    print(f"Waiting for ChromaDB at {host}:{port}...")
    
    for attempt in range(max_retries):
        try:
            # Try to connect to ChromaDB heartbeat endpoint
            response = requests.get(
                f"http://{host}:{port}/api/v1/heartbeat",
                timeout=3
            )
            if response.status_code == 200:
                print(f"✓ ChromaDB is ready!")
                return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Attempt {attempt + 1}/{max_retries}: ChromaDB not ready yet... ({type(e).__name__})")
                time.sleep(delay)
            else:
                print(f"✗ ChromaDB failed to become ready after {max_retries} attempts")
                return False
    
    return False


def main() -> int:
    """Main function to wait for all services"""
    print("=" * 60)
    print("Waiting for required services to be ready...")
    print("=" * 60)
    
    # Wait for PostgreSQL
    if not wait_for_postgres():
        print("\n❌ Failed to connect to PostgreSQL")
        return 1
    
    # Wait for ChromaDB
    if not wait_for_chromadb():
        print("\n❌ Failed to connect to ChromaDB")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ All services are ready!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
