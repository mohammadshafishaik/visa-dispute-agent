#!/bin/bash

echo "=========================================="
echo "VISA DISPUTE AGENT - COMPLETE TEST"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if services are running
echo "1. Checking services..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ API is running${NC}"
    echo "$HEALTH" | python3 -m json.tool
else
    echo -e "${RED}✗ API is not running${NC}"
    exit 1
fi

echo ""
echo "2. Submitting test dispute..."
echo ""

# Submit a dispute
RESPONSE=$(curl -s -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "DSP-TEST-001",
    "customer_id": "CUST-12345",
    "transaction_id": "TXN-98765",
    "amount": 299.99,
    "currency": "USD",
    "reason_code": "10.4",
    "description": "Customer claims unauthorized transaction on their card for online purchase",
    "timestamp": "2024-11-28T10:00:00Z"
  }')

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool

# Check if successful
if echo "$RESPONSE" | grep -q "processing\|accepted"; then
    echo ""
    echo -e "${GREEN}✓ Dispute submitted successfully${NC}"
    
    # Extract dispute ID
    DISPUTE_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('dispute_id', 'DSP-TEST-001'))")
    
    echo ""
    echo "3. Checking dispute status..."
    sleep 2
    
    STATUS=$(curl -s http://localhost:8000/disputes/$DISPUTE_ID)
    echo "$STATUS" | python3 -m json.tool
    
    echo ""
    echo "4. Checking review queue..."
    QUEUE=$(curl -s http://localhost:8000/review-queue)
    echo "$QUEUE" | python3 -m json.tool
    
else
    echo ""
    echo -e "${RED}✗ Dispute submission failed${NC}"
fi

echo ""
echo "=========================================="
echo "TEST COMPLETE"
echo "=========================================="
