# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, implement:
- Webhook signature verification (HMAC)
- API key authentication
- Rate limiting per client

## Endpoints

### 1. Receive Dispute Webhook

Receives dispute notifications from payment processors and initiates processing.

**Endpoint:** `POST /webhooks/dispute`

**Request Body:**
```json
{
  "dispute_id": "disp_123abc",
  "customer_id": "cust_456def",
  "transaction_id": "txn_789ghi",
  "amount": "150.00",
  "currency": "USD",
  "reason_code": "10.4",
  "description": "Customer claims unauthorized transaction",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response (202 Accepted):**
```json
{
  "status": "accepted",
  "dispute_id": "disp_123abc",
  "message": "Dispute received and processing initiated"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Validation error: field 'amount' must be positive"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "disp_123",
    "customer_id": "cust_456",
    "transaction_id": "txn_789",
    "amount": "150.00",
    "currency": "USD",
    "reason_code": "10.4",
    "description": "Customer claims unauthorized transaction",
    "timestamp": "2024-01-15T10:30:00Z"
  }'
```

### 2. Get Dispute Status

Queries the current status of a dispute.

**Endpoint:** `GET /disputes/{dispute_id}`

**Path Parameters:**
- `dispute_id` (string, required): Unique dispute identifier

**Response (200 OK):**
```json
{
  "dispute_id": "disp_123abc",
  "current_node": "completed",
  "status": "resolved",
  "confidence_score": 0.92,
  "decision": "accept",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Dispute disp_123abc not found"
}
```

**Example cURL:**
```bash
curl http://localhost:8000/disputes/disp_123
```

### 3. Get Human Review Queue

Lists all disputes pending human review.

**Endpoint:** `GET /review-queue`

**Response (200 OK):**
```json
[
  {
    "dispute_id": "disp_456def",
    "confidence_score": 0.72,
    "decision": "escalate",
    "reasoning": "Insufficient evidence to make automated decision",
    "supporting_rules": ["visa_rule_001", "visa_rule_005"],
    "status": "pending_review",
    "created_at": "2024-01-15T09:00:00Z"
  },
  {
    "dispute_id": "disp_789ghi",
    "confidence_score": 0.65,
    "decision": "escalate",
    "reasoning": "Complex case requiring manual review",
    "supporting_rules": ["visa_rule_003"],
    "status": "pending_review",
    "created_at": "2024-01-15T08:30:00Z"
  }
]
```

**Example cURL:**
```bash
curl http://localhost:8000/review-queue
```

### 4. Health Check

Checks the health status of the system and its dependencies.

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "healthy",
  "vector_store": "healthy (12 documents)",
  "version": "0.1.0"
}
```

**Response (200 OK - Degraded):**
```json
{
  "status": "degraded",
  "database": "healthy",
  "vector_store": "unhealthy: connection timeout",
  "version": "0.1.0"
}
```

**Example cURL:**
```bash
curl http://localhost:8000/health
```

## Data Models

### DisputeWebhook

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| dispute_id | string | Yes | Unique dispute identifier |
| customer_id | string | Yes | Customer identifier |
| transaction_id | string | Yes | Transaction identifier |
| amount | decimal | Yes | Dispute amount (must be positive) |
| currency | string | Yes | Currency code (e.g., USD, EUR) |
| reason_code | string | Yes | Visa reason code (e.g., 10.4, 13.1) |
| description | string | Yes | Dispute description (min 10 chars) |
| timestamp | datetime | Yes | Dispute creation timestamp (ISO 8601) |

### DisputeDecision

| Field | Type | Description |
|-------|------|-------------|
| dispute_id | string | Unique dispute identifier |
| decision | enum | One of: "accept", "reject", "escalate" |
| confidence_score | float | Confidence score (0.0-1.0) |
| reasoning | string | Explanation for the decision |
| supporting_rules | array[string] | List of relevant Visa rule references |
| recommended_action | string | Recommended next action |

### HumanReviewCase

| Field | Type | Description |
|-------|------|-------------|
| dispute_id | string | Unique dispute identifier |
| confidence_score | float | Confidence score (0.0-1.0) |
| decision | string | Decision type |
| reasoning | string | Explanation for escalation |
| supporting_rules | array[string] | Relevant Visa rules |
| status | enum | One of: "pending_review", "in_review", "resolved" |
| created_at | datetime | When case was created |

## Workflow

### Happy Path (High Confidence)

```
1. POST /webhooks/dispute
   ↓
2. Input Node (validate and initialize)
   ↓
3. Enrichment Node (fetch transaction history)
   ↓
4. Legal Research Node (RAG retrieval)
   ↓
5. Adjudication Node (LLM decision)
   ↓
6. Confidence Check (≥0.85)
   ↓
7. Action Node (send email)
   ↓
8. Complete (audit logged)
```

### Low Confidence Path

```
1. POST /webhooks/dispute
   ↓
2-5. (same as above)
   ↓
6. Confidence Check (<0.85)
   ↓
7. Human Review Node
   ↓
8. GET /review-queue (case appears here)
```

### Self-Correction Path

```
1. POST /webhooks/dispute
   ↓
2-3. (same as above)
   ↓
4. Legal Research Node (low similarity <0.7)
   ↓
5. Query Rewrite (attempt 1)
   ↓
6. Legal Research Node (retry)
   ↓
7. Still low? Rewrite again (attempt 2)
   ↓
8. Still low? Rewrite again (attempt 3)
   ↓
9. Still low? → Human Review
```

## Error Handling

### Validation Errors (400)

Returned when the request payload fails schema validation:
- Missing required fields
- Invalid data types
- Out-of-range values
- Malformed timestamps

### Not Found (404)

Returned when querying a non-existent dispute.

### Internal Server Error (500)

Returned when an unexpected error occurs during processing. The error is logged to the audit trail.

## Rate Limiting

**Not currently implemented.** In production, implement:
- Per-client rate limiting (e.g., 100 requests/minute)
- Global rate limiting (e.g., 1000 requests/minute)
- Exponential backoff for repeated failures

## Monitoring

### Key Metrics to Track

1. **Request Metrics**
   - Request rate per endpoint
   - Response time (p50, p95, p99)
   - Error rate by status code

2. **Business Metrics**
   - Disputes processed per hour
   - Average confidence score
   - Human review queue depth
   - Automated vs. escalated ratio

3. **System Metrics**
   - Database connection pool usage
   - ChromaDB query latency
   - LLM API latency and token usage
   - Memory and CPU usage

### Logging

All requests are logged with:
- Request ID (correlation ID)
- Timestamp
- Endpoint and method
- Response status
- Processing time

All disputes are logged to the audit trail with:
- Node transitions
- Decision reasoning
- Confidence scores
- Actions taken

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Explore all endpoints
- View request/response schemas
- Test API calls directly from the browser
- Download OpenAPI specification

## Webhook Integration

### Payment Processor Setup

Configure your payment processor (Stripe, Visa) to send webhooks to:

```
https://your-domain.com/webhooks/dispute
```

### Webhook Signature Verification

**TODO**: Implement HMAC signature verification:

```python
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### Retry Logic

Payment processors typically retry failed webhooks:
- Immediate retry
- 1 minute later
- 5 minutes later
- 30 minutes later
- 1 hour later

Ensure your endpoint is idempotent to handle duplicate webhooks.

## Testing

### Test Webhook

```bash
# Send a test dispute
curl -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "test_001",
    "customer_id": "test_customer",
    "transaction_id": "test_txn",
    "amount": "99.99",
    "currency": "USD",
    "reason_code": "10.4",
    "description": "Test dispute for development",
    "timestamp": "2024-01-15T12:00:00Z"
  }'

# Check status
curl http://localhost:8000/disputes/test_001

# Check review queue
curl http://localhost:8000/review-queue
```

## Support

For API issues or questions:
- Check logs: `docker-compose logs -f`
- Review audit trail in PostgreSQL
- Check health endpoint: `GET /health`
- Contact: support@example.com
