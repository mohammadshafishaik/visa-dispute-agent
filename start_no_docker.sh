#!/bin/bash

echo "🚀 Starting Visa Dispute Agent System (No Docker)..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary chromadb openai langchain langgraph
fi

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 &>/dev/null; then
    echo "⚠️  PostgreSQL is not running. You need to:"
    echo "   1. Install PostgreSQL: brew install postgresql"
    echo "   2. Start it: brew services start postgresql"
    echo "   3. Create database: createdb visa_disputes"
    exit 1
fi

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Seed ChromaDB (will use local ChromaDB)
echo "🌱 Seeding ChromaDB..."
python scripts/seed_chromadb.py

# Start the server
echo "🚀 Starting API server..."
echo ""
echo "✅ Server starting at http://localhost:8000"
echo "📚 API Docs at http://localhost:8000/docs"
echo ""
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
