"""
E2E tests hit the REAL running docker-compose stack over HTTP -- no mocks,
no in-process imports of service internals. That's the whole point of an
E2E suite: it's the only place that actually proves the services agree with
each other over the wire (a bug where two services silently disagree on a
field name would pass every per-service unit test and only show up here).

Because that means these tests need `docker compose up` first, they are
NOT run as part of a normal `pytest` invocation -- pytest.ini here restricts
this directory to `-m e2e`, and `skip_if_stack_down` below skips gracefully
(rather than erroring) when the Gateway isn't reachable, so a plain
`pytest` from the repo root or CI without Docker never fails because of this
directory.

Run for real with: `docker compose up -d && pytest tests/e2e -v -m e2e`
"""
import time
import uuid

import httpx
import pytest

GATEWAY_URL = "http://localhost:8000"


def _stack_is_up() -> bool:
    try:
        resp = httpx.get(f"{GATEWAY_URL}/health", timeout=2)
        return resp.status_code == 200
    except httpx.HTTPError:
        return False


@pytest.fixture(scope="session", autouse=True)
def skip_if_stack_down():
    if not _stack_is_up():
        pytest.skip(
            "docker-compose stack is not running at " + GATEWAY_URL +
            " -- run `docker compose up -d` first to execute the E2E suite.",
            allow_module_level=True,
        )


@pytest.fixture()
def registered_user():
    """A fresh ADMIN user + access token for each test (unique email avoids
    collisions between test runs against a persistent dev database)."""
    email = f"e2e-{uuid.uuid4().hex[:10]}@example.com"
    password = "SuperSecret1"
    with httpx.Client(base_url=GATEWAY_URL, timeout=10) as client:
        client.post("/api/v1/auth/register", json={"email": email, "password": password, "role": "ADMIN"})
        login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
        login_resp.raise_for_status()
        token = login_resp.json()["access_token"]
    return {"email": email, "token": token}


def poll_execution_status(client: httpx.Client, execution_id: str, token: str, timeout_seconds: float = 20.0) -> dict:
    """Polls execution status until it reaches a terminal or waiting state,
    since the whole flow is asynchronous (Gateway -> Workflow Service ->
    RabbitMQ/Celery -> workers -> callback). A tight poll loop with a bound
    is the standard way to assert against eventually-consistent async
    systems in a test."""
    terminal = {"COMPLETED", "FAILED", "CANCELLED", "WAITING_FOR_APPROVAL"}
    deadline = time.monotonic() + timeout_seconds
    headers = {"Authorization": f"Bearer {token}"}
    last = {}
    while time.monotonic() < deadline:
        resp = client.get(f"/api/v1/workflows/executions/{execution_id}/status", headers=headers)
        resp.raise_for_status()
        last = resp.json()
        if last["status"] in terminal:
            return last
        time.sleep(0.5)
    return last  # return whatever we last saw; the assertion will fail informatively
