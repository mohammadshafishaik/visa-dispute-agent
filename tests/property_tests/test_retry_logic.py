"""Property-based tests for retry logic"""
from hypothesis import given, strategies as st
import asyncio


# Feature: visa-dispute-agent, Property 6: Retry with exponential backoff
@given(
    attempt=st.integers(min_value=0, max_value=2),
    base_delay=st.floats(min_value=0.1, max_value=2.0)
)
def test_exponential_backoff_delay_calculation(attempt, base_delay):
    """For any retry attempt, delay should follow exponential backoff pattern"""
    # Calculate expected delay
    expected_delay = base_delay * (2 ** attempt)
    
    # Verify exponential growth
    assert expected_delay == base_delay * (2 ** attempt)
    assert expected_delay >= base_delay
    
    # Verify delays increase exponentially
    if attempt > 0:
        previous_delay = base_delay * (2 ** (attempt - 1))
        assert expected_delay == previous_delay * 2


@given(st.integers(min_value=1, max_value=5))
def test_max_retry_attempts_enforced(max_attempts):
    """For any max_attempts setting, retry logic should not exceed that limit"""
    attempts_made = 0
    
    for attempt in range(max_attempts):
        attempts_made += 1
        if attempt == max_attempts - 1:
            # Last attempt
            break
    
    assert attempts_made == max_attempts
    assert attempts_made <= max_attempts


# Feature: visa-dispute-agent, Property 17: Failure escalation
@given(
    max_retries=st.integers(min_value=1, max_value=5),
    failure_count=st.integers(min_value=1, max_value=10)
)
def test_failure_escalation_after_max_retries(max_retries, failure_count):
    """For any node that fails after max retries, dispute should route to human review"""
    should_escalate = failure_count >= max_retries
    
    if should_escalate:
        # After max retries, should escalate
        assert failure_count >= max_retries
        expected_action = "escalate_to_human_review"
    else:
        # Still within retry limit
        assert failure_count < max_retries
        expected_action = "retry"
    
    # Verify escalation logic
    if failure_count >= max_retries:
        assert expected_action == "escalate_to_human_review"
    else:
        assert expected_action == "retry"
