# Cross-service tests

Per-service unit/API tests live inside each service (`services/*/tests/`,
`workers/*/tests/`) so each suite runs in isolation with that service's own
`PYTHONPATH` -- avoids the classic monorepo problem of multiple services
each having a top-level `app` package colliding in one pytest session.

This directory is reserved for true cross-service integration/e2e tests that
exercise the running docker-compose stack over HTTP (e.g. "register, login,
create a workflow, execute it, approve it, assert it completes") rather than
importing service internals. Not included in this build -- the per-service
tests plus the eval harness cover the logic that matters most to verify
without needing the full stack running; add e2e tests here once you have a
CI environment that can run `docker compose up` first.
