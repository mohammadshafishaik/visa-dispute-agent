# Quick Start Guide

Get the Visa Dispute Agent up and running in 5 minutes.

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- OpenAI API key

## Step 1: Clone and Install

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Minimum required:
# LLM_API_KEY=your-openai-api-key-here
```

## Step 3: Start Infrastructure

```bash
# Start PostgreSQL and ChromaDB
docker-compose up -d

# Wait a few seconds for services to start
sleep 5
```

## Step 4: Initialize Database

```bash
# Run database migrations
poetry run alembic upgrade head

# Seed ChromaDB with Visa rules
poetry run python scripts/seed_chromadb.py
```

## Step 5: Run the Server

```bash
# Start the FastAPI server
poetry run uvicorn app.api.main:app --reload
```

The server will start at http://localhost:8000

## Step 6: Test the API

### Check Health

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "database": "healthy",
  "vector_store": "healthy (12 documents)",
  "version": "0.1.0"
}
```

### Send a Test Dispute

```bash
curl -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "test_001",
    "customer_id": "cust_123",
    "transaction_id": "txn_456",
    "amount": "150.00",
    "currency": "USD",
    "reason_code": "10.4",
    "description": "Customer claims they did not authorize this transaction",
    "timestamp": "2024-01-15T10:30:00Z"
  }'
```

Expected output:
```json
{
  "status": "accepted",
  "dispute_id": "test_001",
  "message": "Dispute received and processing initiated"
}
```

### Check Review Queue

```bash
curl http://localhost:8000/review-queue
```

## Interactive API Documentation

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Run Tests

```bash
# Run all tests
poetry run pytest -v

# Run only property-based tests
poetry run pytest tests/property_tests/ -v

# Run with coverage
poetry run pytest --cov=app --cov-report=html
```

## Using the Makefile

For convenience, use the Makefile commands:

```bash
# One-command setup (install + docker + migrate + seed)
make setup

# Run the server
make run

# Run tests
make test

# Run property tests only
make test-property

# Format code
make format

# Lint code
make lint

# Clean up
make clean
```

## Project Structure

```
visa-dispute-agent/
├── app/
│   ├── agents/          # LangGraph state machine
│   ├── api/             # FastAPI endpoints
│   ├── config/          # Configuration management
│   ├── db/              # Database layer
│   ├── schema/          # Pydantic models
│   └── tools/           # RAG and enrichment tools
├── tests/
│   ├── unit/            # Unit tests
│   ├── property_tests/  # Property-based tests
│   └── integration/     # Integration tests
├── scripts/             # Utility scripts
├── alembic/             # Database migrations
└── docker-compose.yml   # Infrastructure services
```

## Common Issues

### Port Already in Use

If port 8000 is already in use:
```bash
# Use a different port
poetry run uvicorn app.api.main:app --reload --port 8001
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart services
docker-compose restart
```

### ChromaDB Connection Error

```bash
# Check if ChromaDB is running
docker-compose ps chromadb

# View logs
docker-compose logs chromadb
```

### Missing OpenAI API Key

Make sure you've set `LLM_API_KEY` in your `.env` file:
```bash
echo "LLM_API_KEY=your-key-here" >> .env
```

## Next Steps

1. **Read the Documentation**
   - [README.md](README.md) - Project overview
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
   - [PROJECT_STATUS.md](PROJECT_STATUS.md) - Implementation status

2. **Explore the Code**
   - Start with `app/api/main.py` - API endpoints
   - Then `app/agents/dispute_graph.py` - Workflow logic
   - Check `app/tools/rag_retriever.py` - RAG implementation

3. **Run the Tests**
   - Property tests demonstrate correctness properties
   - Unit tests show component behavior
   - Integration tests verify end-to-end workflows

4. **Customize**
   - Add more Visa rules to ChromaDB
   - Adjust confidence threshold in `.env`
   - Implement Gmail API integration
   - Add custom fraud detection patterns

## Development Workflow

```bash
# 1. Make changes to code
vim app/agents/dispute_graph.py

# 2. Format and lint
make format
make lint

# 3. Run tests
make test

# 4. Test manually
make run
# In another terminal:
curl -X POST http://localhost:8000/webhooks/dispute ...

# 5. Check logs
docker-compose logs -f

# 6. Commit changes
git add .
git commit -m "Add feature X"
```

## Getting Help

- Check the logs: `docker-compose logs -f`
- Review the audit trail in PostgreSQL
- Check the health endpoint: `curl http://localhost:8000/health`
- Read the full documentation in the docs/ directory

## Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md).

Key considerations:
- Use environment variables for all secrets
- Enable webhook signature verification
- Set up monitoring and alerting
- Configure rate limiting
- Use a production-grade database
- Implement proper logging and observability

---

**Ready to go!** 🚀

The Visa Dispute Agent is now running and ready to process disputes automatically.
