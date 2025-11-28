#!/bin/bash
set -e

echo "🚀 Starting Visa Dispute Agent on Render..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
python scripts/wait_for_services.py || echo "⚠️  Database check skipped"

# Run migrations
echo "📊 Running database migrations..."
alembic upgrade head || echo "⚠️  Migrations skipped (run manually if needed)"

# Seed ChromaDB (optional - can be done manually)
echo "🌱 Seeding Visa rules..."
python scripts/seed_chromadb.py || echo "⚠️  Seeding skipped (run manually if needed)"

# Start the application
echo "✅ Starting FastAPI application..."
exec uvicorn app.api.main:app --host 0.0.0.0 --port ${PORT:-8000}
