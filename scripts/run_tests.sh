#!/bin/bash
# Test runner script for Visa Dispute Agent

set -e

echo "================================"
echo "Visa Dispute Agent - Test Suite"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}Error: Poetry is not installed${NC}"
    echo "Install it with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d ".venv" ] && [ ! -d "$(poetry env info -p 2>/dev/null)" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    poetry install
fi

echo -e "${GREEN}Running Property-Based Tests...${NC}"
echo "================================"
poetry run pytest tests/property_tests/ -v --tb=short || {
    echo -e "${RED}Property tests failed!${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}Running Unit Tests...${NC}"
echo "================================"
poetry run pytest tests/unit/ -v --tb=short || {
    echo -e "${RED}Unit tests failed!${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}Running Integration Tests...${NC}"
echo "================================"
poetry run pytest tests/integration/ -v --tb=short || {
    echo -e "${RED}Integration tests failed!${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}All tests passed! ✓${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Optional: Run with coverage
if [ "$1" == "--coverage" ]; then
    echo -e "${YELLOW}Generating coverage report...${NC}"
    poetry run pytest --cov=app --cov-report=html --cov-report=term
    echo ""
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
fi
