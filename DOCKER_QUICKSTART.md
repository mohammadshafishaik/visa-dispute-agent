# Docker Quickstart Guide

## Prerequisites
- Docker Desktop installed and running
- No password needed - everything runs in containers!

## Quick Start

### 1. Start the System
```bash
docker compose up -d
```

This will:
- Start PostgreSQL database
- Start ChromaDB vector store
- Build and start the FastAPI application
- Run database migrations automatically
- Seed ChromaDB with Visa rules
- Start the API server

### 2. Check System Status
```bash
# View logs
docker compose logs -f

# Check health
curl http://localhost:8000/health
```

### 3. Access the API
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ChromaDB**: http://localhost:8001

### 4. Stop the System
```bash
# Stop containers (keeps data)
docker compose down

# Stop and remove all data
docker compose down -v
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| FastAPI App | 8000 | Main application API |
| PostgreSQL | 5432 | Database for dispute history |
| ChromaDB | 8001 | Vector store for Visa rules |

## Environment Variables

The system uses default values for development. To customize:

1. Copy `.env.example` to `.env`
2. Update values as needed
3. Restart: `docker compose down && docker compose up -d`

## Troubleshooting

### Services not starting?
```bash
# Check Docker is running
docker info

# View detailed logs
docker compose logs app
docker compose logs postgres
docker compose logs chromadb
```

### Reset everything
```bash
docker compose down -v
docker system prune -f
docker compose up --build -d
```

### Check individual service
```bash
# Check if app is healthy
docker compose exec app python -c "print('App container is working!')"

# Check database
docker compose exec postgres psql -U visa_user -d visa_disputes -c "SELECT 1;"
```

## Development

### Rebuild after code changes
```bash
docker compose up --build -d
```

### View real-time logs
```bash
docker compose logs -f app
```

### Access container shell
```bash
docker compose exec app bash
```

## Testing the API

### Health Check
```bash
curl http://localhost:8000/health
```

### Submit a Dispute
```bash
curl -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "DSP-2024-001",
    "cardholder_id": "CH-12345",
    "transaction_id": "TXN-98765",
    "amount": 150.00,
    "currency": "USD",
    "merchant_name": "Example Store",
    "dispute_reason": "unauthorized_transaction",
    "description": "I did not make this purchase",
    "transaction_date": "2024-01-15T10:30:00Z",
    "dispute_date": "2024-01-20T14:00:00Z"
  }'
```

### Check Dispute Status
```bash
curl http://localhost:8000/disputes/DSP-2024-001
```

## Success!

Your Visa Dispute Agent system is now running entirely in Docker with:
- ✅ Automatic service health checks
- ✅ Database migrations
- ✅ Vector store seeding
- ✅ Hot reload for development
- ✅ No manual setup required!
