# Deployment Guide

## Prerequisites

- Python 3.11+
- Poetry (Python package manager)
- Docker and Docker Compose
- PostgreSQL 15+
- OpenAI API key

## Local Development Setup

### 1. Install Dependencies

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
make install
# or
poetry install
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Required variables:
# - DATABASE_URL
# - CHROMADB_HOST
# - LLM_API_KEY
# - ENRICHMENT_API_URL (or use mock)
```

### 3. Start Infrastructure

```bash
# Start PostgreSQL and ChromaDB
make docker-up
# or
docker-compose up -d

# Wait for services to be ready
sleep 5
```

### 4. Initialize Database

```bash
# Run database migrations
make migrate
# or
poetry run alembic upgrade head

# Seed ChromaDB with Visa rules
make seed-db
# or
poetry run python scripts/seed_chromadb.py
```

### 5. Run the Application

```bash
# Start the FastAPI server
make run
# or
poetry run uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Testing

### Run All Tests

```bash
make test
# or
poetry run pytest -v
```

### Run Property-Based Tests

```bash
make test-property
# or
poetry run pytest tests/property_tests/ -v
```

### Run Unit Tests

```bash
make test-unit
# or
poetry run pytest tests/unit/ -v
```

### Run with Coverage

```bash
make test-coverage
# or
poetry run pytest --cov=app --cov-report=html --cov-report=term
```

## Production Deployment

### Environment Variables

Required environment variables for production:

```bash
# Database
DATABASE_URL=postgresql://user:password@db-host:5432/visa_disputes

# ChromaDB
CHROMADB_HOST=chromadb-host
CHROMADB_PORT=8000

# Enrichment Service
ENRICHMENT_API_URL=https://enrichment-api.example.com/api/v1

# Gmail API (optional)
GMAIL_API_CREDENTIALS=/path/to/credentials.json

# LLM
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4-turbo-preview

# Application
LOG_LEVEL=INFO
MAX_RETRY_ATTEMPTS=3
CONFIDENCE_THRESHOLD=0.85
SIMILARITY_THRESHOLD=0.7
```

### Docker Deployment

```bash
# Build Docker image
docker build -t visa-dispute-agent:latest .

# Run container
docker run -d \
  --name visa-dispute-agent \
  -p 8000:8000 \
  --env-file .env \
  visa-dispute-agent:latest
```

### Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests (to be created).

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "healthy",
  "vector_store": "healthy (12 documents)",
  "version": "0.1.0"
}
```

### Metrics

Key metrics to monitor:
- Request rate and latency per endpoint
- Error rate by error type
- Human review queue depth
- RAG retrieval quality (average similarity scores)
- Confidence score distribution
- Retry attempt frequency

### Logs

Structured JSON logs are written to stdout. Use a log aggregation service like:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Datadog
- CloudWatch Logs

## Database Maintenance

### Create New Migration

```bash
make migrate-create message="description of changes"
# or
poetry run alembic revision --autogenerate -m "description"
```

### Rollback Migration

```bash
poetry run alembic downgrade -1
```

### Backup Database

```bash
pg_dump -h localhost -U visa_user visa_disputes > backup.sql
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection
psql -h localhost -U visa_user -d visa_disputes
```

### ChromaDB Issues

```bash
# Check ChromaDB is running
docker-compose ps chromadb

# Check collection
curl http://localhost:8000/api/v1/collections
```

### LLM API Issues

- Verify API key is correct
- Check rate limits
- Monitor token usage

## Security Considerations

1. **API Security**
   - Implement webhook signature verification
   - Add rate limiting per client
   - Use API keys for authentication

2. **Data Security**
   - Encrypt sensitive data at rest
   - Use TLS for all external communications
   - Rotate credentials regularly

3. **LLM Security**
   - Implement prompt injection detection
   - Sanitize all outputs
   - Monitor token usage and costs

## Scaling

### Horizontal Scaling

- Deploy multiple FastAPI instances behind a load balancer
- Use shared PostgreSQL and ChromaDB instances
- Consider Redis for distributed rate limiting

### Vertical Scaling

- Increase database connection pool size
- Optimize ChromaDB index for faster retrieval
- Cache frequently accessed Visa rules

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review audit trail in PostgreSQL
- Check human review queue for escalated cases
