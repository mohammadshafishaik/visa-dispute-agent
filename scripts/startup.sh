#!/bin/bash
# Comprehensive startup script for Visa Dispute Agent

set -e

echo "================================"
echo "Visa Dispute Agent - Startup"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}Error: Poetry is not installed${NC}"
    echo "Install it with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    echo "Please start Docker Desktop"
    exit 1
fi

# Step 1: Install dependencies
echo -e "${YELLOW}Step 1: Installing dependencies...${NC}"
poetry install
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 2: Start infrastructure
echo -e "${YELLOW}Step 2: Starting infrastructure (PostgreSQL + ChromaDB)...${NC}"
docker-compose up -d
echo "Waiting for services to be ready..."
sleep 5
echo -e "${GREEN}✓ Infrastructure started${NC}"
echo ""

# Step 3: Run database migrations
echo -e "${YELLOW}Step 3: Running database migrations...${NC}"
poetry run alembic upgrade head
echo -e "${GREEN}✓ Migrations complete${NC}"
echo ""

# Step 4: Seed ChromaDB
echo -e "${YELLOW}Step 4: Seeding ChromaDB with Visa rules...${NC}"
poetry run python scripts/seed_chromadb.py
echo -e "${GREEN}✓ ChromaDB seeded${NC}"
echo ""

# Step 5: Verify installation
echo -e "${YELLOW}Step 5: Verifying installation...${NC}"
poetry run python scripts/verify_installation.py
echo ""

# Step 6: Run tests
echo -e "${YELLOW}Step 6: Running tests...${NC}"
poetry run pytest tests/property_tests/ -v --tb=short -x
echo -e "${GREEN}✓ Tests passed${NC}"
echo ""

echo "================================"
echo -e "${GREEN}Startup Complete!${NC}"
echo "================================"
echo ""
echo "The system is ready. You can now:"
echo "  1. Start the server: make run"
echo "  2. View API docs: http://localhost:8000/docs"
echo "  3. Run load tests: python scripts/load_test.py"
echo "  4. Check monitoring: http://localhost:8000/monitoring/metrics"
echo ""
