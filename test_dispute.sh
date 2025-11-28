#!/bin/bash

echo "=========================================="
echo "TESTING VISA DISPUTE AGENT"
echo "=========================================="

# Test 1: Health Check
echo -e "\n1. Health Check:"
curl -s http://localhost:8000/health | python3 -m json.tool

# Test 2: Submit Dispute (POST request)
echo -e "\n\n2. Submitting Dispute:"
curl -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "DSP-TEST-123",
    "customer_id": "CUST-456",
    "transaction_id": "TXN-789",
    "amount": 500.00,
    "currency": "USD",
    "reason_code": "10.4",
    "description": "Unauthorized online purchase - customer claims fraud",
    "timestamp": "2024-11-28T10:00:00Z"
  }' | python3 -m json.tool

echo -e "\n\n=========================================="
echo "✓ TEST COMPLETE"
echo "=========================================="
