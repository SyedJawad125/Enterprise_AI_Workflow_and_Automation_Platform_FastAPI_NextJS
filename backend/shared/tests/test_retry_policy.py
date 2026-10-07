"""
Pure-logic tests for the retry classification + schedule every worker uses.
No broker/network needed -- this is exactly the kind of decision logic that
should be extracted and testable in isolation (spec section 16's
retry-safety distinction, verified here rather than just asserted in a
docstring).

Run from the repo root: PYTHONPATH=. pytest shared/tests/ -v
"""
import httpx

from shared.messaging.retry_policy import is_retryable, next_retry_delay, RETRY_DELAYS, MAX_RETRIES


def _status_error(status_code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "http://example.test/thing")
    response = httpx.Response(status_code, request=request)
    return httpx.HTTPStatusError("error", request=request, response=response)


def test_5xx_is_retryable():
    assert is_retryable(_status_error(500)) is True
    assert is_retryable(_status_error(503)) is True


def test_4xx_is_not_retryable():
    assert is_retryable(_status_error(404)) is False
    assert is_retryable(_status_error(422)) is False
    assert is_retryable(_status_error(400)) is False


def test_network_level_errors_are_retryable():
    request = httpx.Request("POST", "http://example.test/thing")
    assert is_retryable(httpx.ConnectError("refused", request=request)) is True
    assert is_retryable(httpx.ReadTimeout("timed out", request=request)) is True


def test_non_http_exception_is_not_retryable():
    assert is_retryable(ValueError("not an http error")) is False


def test_retry_schedule_matches_configured_delays():
    for i, expected_delay in enumerate(RETRY_DELAYS):
        assert next_retry_delay(i) == expected_delay


def test_retry_schedule_exhausts_after_max_retries():
    assert next_retry_delay(MAX_RETRIES) is None
    assert next_retry_delay(MAX_RETRIES + 5) is None
