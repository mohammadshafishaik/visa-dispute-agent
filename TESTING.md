# Testing Guide

## Overview

The Visa Dispute Agent uses a comprehensive testing strategy with three types of tests:

1. **Property-Based Tests** - Verify correctness properties using Hypothesis
2. **Unit Tests** - Test individual components in isolation
3. **Integration Tests** - Test end-to-end workflows

## Running Tests

### Quick Start

```bash
# Run all tests
make test

# Run specific test types
make test-property    # Property-based tests only
make test-unit        # Unit tests only

# Run with coverage
make test-coverage

# Or use the test runner script
./scripts/run_tests.sh
./scripts/run_tests.sh --coverage
```

### Manual Test Execution

```bash
# All tests
poetry run pytest -v

# Specific test file
poetry run pytest tests/property_tests/test_webhook_validation.py -v

# Specific test function
poetry run pytest tests/property_tests/test_webhook_validation.py::test_valid_webhooks_are_accepted -v

# With detailed output
poetry run pytest -vv --tb=long

# Stop on first failure
poetry run pytest -x
```

## Property-Based Tests

Property-based tests use Hypothesis to generate diverse test inputs and verify correctness properties.

### Configuration

- **Max Examples**: 100 iterations per test
- **Deadline**: 5000ms per test case
- **Profile**: Configured in `tests/conftest.py`

### Property Tests Implemented

#### ✅ Property 1: Webhook Payload Validation
**File**: `tests/property_tests/test_webhook_validation.py`
- Verifies valid webhooks are accepted
- Verifies invalid webhooks are rejected with proper errors
- Tests all field validations

#### ✅ Property 2: State Initialization Completeness
**File**: `tests/property_tests/test_state_initialization.py`
- Verifies all required fields are present in initial state
- Tests with diverse webhook inputs

#### ✅ Property 6: Retry with Exponential Backoff
**File**: `tests/property_tests/test_retry_logic.py`
- Verifies exponential backoff delay calculation
- Tests max retry attempts enforcement

#### ✅ Property 7: RAG Query Generation
**File**: `tests/property_tests/test_rag_properties.py`
- Verifies queries include dispute details
- Tests with various reason codes and descriptions

#### ✅ Property 8: Similarity Score Calculation
**File**: `tests/property_tests/test_rag_properties.py`
- Verifies all documents have scores between 0.0-1.0
- Tests with diverse document sets

#### ✅ Property 9: Self-Reflective Query Rewriting
**File**: `tests/property_tests/test_similarity_routing.py`
- Verifies low similarity triggers rewrite
- Tests query rewrite loop with max 3 attempts

#### ✅ Property 10: High-Quality Retrieval Progression
**File**: `tests/property_tests/test_similarity_routing.py`
- Verifies high similarity proceeds to adjudication
- Tests threshold logic

#### ✅ Property 11: Adjudication Decision Structure
**File**: `tests/property_tests/test_schema_validation.py`
- Verifies decision conforms to schema
- Tests all decision fields

#### ✅ Property 12: Confidence-Based Routing
**File**: `tests/property_tests/test_confidence_routing.py`
- Verifies routing based on 0.85 threshold
- Tests all confidence score ranges

#### ✅ Property 13: Human Review Queue Persistence
**File**: `tests/property_tests/test_validation_retry.py`
- Verifies low confidence cases are persisted
- Tests queue entry structure

#### ✅ Property 16: Conditional Routing Correctness
**File**: `tests/property_tests/test_rag_properties.py`
- Verifies routing decisions match state conditions
- Tests all routing paths

#### ✅ Property 17: Failure Escalation
**File**: `tests/property_tests/test_retry_logic.py`
- Verifies escalation after max retries
- Tests failure handling

#### ✅ Property 18: Schema Validation Enforcement
**File**: `tests/property_tests/test_schema_validation.py`
- Verifies all outputs are validated
- Tests validation edge cases

#### ✅ Property 19: Validation Retry with Correction
**File**: `tests/property_tests/test_validation_retry.py`
- Verifies retry logic for validation failures
- Tests max 3 attempts before escalation

#### ✅ Property 20: Transaction Data Schema Conformance
**File**: `tests/property_tests/test_schema_validation.py`
- Verifies transaction data conforms to schema
- Tests all transaction fields

### Remaining Property Tests

The following properties still need dedicated tests:

- [ ] Property 3: Audit trail completeness
- [ ] Property 4: Enrichment service invocation
- [ ] Property 5: Enrichment state update
- [ ] Property 14: Email action execution
- [ ] Property 15: Action logging with metadata

## Unit Tests

Unit tests verify individual components work correctly in isolation.

### Test Files

#### `tests/unit/test_fraud_detection.py`
- High chargeback rate detection
- Low chargeback rate handling
- High-value dispute flagging
- Empty transaction history handling

#### `tests/unit/test_rag_retriever.py`
- Retrieval quality evaluation
- Query rewriting strategies
- Similarity threshold logic

### Writing Unit Tests

```python
import pytest
from app.tools.transaction_enrichment import TransactionEnrichment

def test_fraud_detection():
    """Test fraud pattern detection"""
    enrichment = TransactionEnrichment("http://test")
    
    # Create test data
    transactions = [...]
    
    # Execute
    analysis = enrichment.detect_fraud_patterns(transactions, amount)
    
    # Assert
    assert analysis.chargeback_rate == expected_rate
    assert analysis.has_suspicious_patterns is True
```

## Integration Tests

Integration tests verify end-to-end workflows.

### Test Files

#### `tests/integration/test_dispute_workflow.py`
- Happy path: high confidence → email sent
- Low confidence → human review
- Low similarity → query rewrite
- Max attempts → escalation
- Error handling → human review

### Running Integration Tests

Integration tests require:
- PostgreSQL database
- ChromaDB vector store
- Mock external services

```bash
# Start infrastructure
docker-compose up -d

# Run integration tests
poetry run pytest tests/integration/ -v

# Cleanup
docker-compose down -v
```

## Test Coverage

### Generating Coverage Reports

```bash
# Terminal report
poetry run pytest --cov=app --cov-report=term

# HTML report
poetry run pytest --cov=app --cov-report=html

# Open HTML report
open htmlcov/index.html
```

### Coverage Goals

- **Overall**: >80%
- **Critical paths**: >90%
- **Property tests**: All correctness properties covered

### Current Coverage

Run `make test-coverage` to see current coverage metrics.

## Mocking External Services

### Mock LLM Responses

```python
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_llm():
    llm = AsyncMock()
    llm.ainvoke = AsyncMock(return_value=MagicMock(
        content='{"decision": "accept", "confidence_score": 0.9, ...}'
    ))
    return llm
```

### Mock Database Operations

```python
from unittest.mock import patch

@patch('app.db.audit_logger.audit_logger.log_node_entry', new_callable=AsyncMock)
async def test_with_mock_db(mock_log):
    # Test code
    pass
```

### Mock External APIs

```python
import httpx
from unittest.mock import AsyncMock

@pytest.fixture
def mock_enrichment_api(monkeypatch):
    async def mock_get(*args, **kwargs):
        return httpx.Response(200, json={"transactions": []})
    
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
```

## Debugging Tests

### Verbose Output

```bash
# Show print statements
poetry run pytest -v -s

# Show full tracebacks
poetry run pytest -v --tb=long

# Show local variables in tracebacks
poetry run pytest -v --tb=long --showlocals
```

### Debug Specific Test

```bash
# Run single test with debugging
poetry run pytest tests/unit/test_fraud_detection.py::test_high_chargeback_rate_detected -vv -s
```

### Using pdb

```python
def test_something():
    import pdb; pdb.set_trace()
    # Test code
```

## Continuous Integration

### GitHub Actions (Example)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      
      - name: Run tests
        run: poetry run pytest --cov=app
        env:
          DATABASE_URL: postgresql://postgres:test@localhost/test
          LLM_API_KEY: test-key
```

## Best Practices

### 1. Test Naming

```python
# Good
def test_high_confidence_routes_to_action():
    pass

# Bad
def test1():
    pass
```

### 2. Arrange-Act-Assert

```python
def test_something():
    # Arrange
    data = create_test_data()
    
    # Act
    result = function_under_test(data)
    
    # Assert
    assert result == expected
```

### 3. One Assertion Per Test

```python
# Good
def test_confidence_above_threshold():
    assert confidence >= 0.85

def test_routes_to_action():
    assert next_node == "action"

# Avoid
def test_everything():
    assert confidence >= 0.85
    assert next_node == "action"
    assert state["error"] is None
```

### 4. Use Fixtures

```python
@pytest.fixture
def sample_dispute():
    return DisputeWebhook(...)

def test_with_fixture(sample_dispute):
    # Use sample_dispute
    pass
```

### 5. Parametrize Tests

```python
@pytest.mark.parametrize("confidence,expected", [
    (0.9, "action"),
    (0.7, "human_review"),
    (0.85, "action"),
])
def test_routing(confidence, expected):
    assert route_by_confidence(confidence) == expected
```

## Troubleshooting

### Tests Fail Locally

1. Check dependencies: `poetry install`
2. Check database: `docker-compose ps`
3. Check environment: `cat .env`
4. Clear cache: `make clean`

### Hypothesis Failures

If Hypothesis finds a failing example:
1. It will print the minimal failing case
2. Add that case as a regular test
3. Fix the bug
4. Re-run Hypothesis tests

### Slow Tests

```bash
# Show slowest tests
poetry run pytest --durations=10

# Run only fast tests
poetry run pytest -m "not slow"
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)
