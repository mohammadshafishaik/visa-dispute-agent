#!/usr/bin/env python3
"""Test the complete dispute workflow"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_dispute_submission():
    """Test submitting a dispute"""
    print("=" * 60)
    print("TESTING VISA DISPUTE AGENT")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1. Checking system health...")
    response = requests.get(f"{BASE_URL}/health")
    health = response.json()
    print(f"   Status: {health['status']}")
    print(f"   Database: {health['database']}")
    print(f"   Vector Store: {health['vector_store']}")
    
    # Test 2: Submit a dispute
    print("\n2. Submitting a fraud dispute...")
    dispute_data = {
        "dispute_id": "DSP-TEST-001",
        "customer_id": "CUST-12345",
        "transaction_id": "TXN-98765",
        "amount": 299.99,
        "currency": "USD",
        "reason_code": "10.4",
        "description": "Unauthorized transaction - customer claims they did not make this purchase",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"   Dispute ID: {dispute_data['dispute_id']}")
    print(f"   Amount: ${dispute_data['amount']}")
    print(f"   Reason Code: {dispute_data['reason_code']}")
    
    response = requests.post(
        f"{BASE_URL}/webhooks/dispute",
        json=dispute_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n   ✓ Dispute submitted successfully!")
        print(f"   Status: {result.get('status')}")
        print(f"   Message: {result.get('message')}")
    else:
        print(f"\n   ✗ Error: {response.status_code}")
        print(f"   {response.text}")
        return
    
    # Test 3: Check dispute status
    print("\n3. Checking dispute status...")
    time.sleep(2)  # Give it a moment to process
    
    response = requests.get(f"{BASE_URL}/disputes/{dispute_data['dispute_id']}")
    if response.status_code == 200:
        status = response.json()
        print(f"   Current Node: {status.get('current_node')}")
        print(f"   Status: {status.get('status')}")
        if status.get('confidence_score'):
            print(f"   Confidence: {status.get('confidence_score'):.2f}")
        if status.get('decision'):
            print(f"   Decision: {status.get('decision')}")
    
    # Test 4: Check review queue
    print("\n4. Checking human review queue...")
    response = requests.get(f"{BASE_URL}/review-queue")
    if response.status_code == 200:
        queue = response.json()
        print(f"   Cases in queue: {len(queue)}")
        if queue:
            print(f"   Latest case: {queue[0].get('dispute_id')}")
    
    print("\n" + "=" * 60)
    print("✓ WORKFLOW TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_dispute_submission()
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to server. Is it running on port 8000?")
    except Exception as e:
        print(f"✗ Error: {e}")
