# Enterprise AI Workflow & Automation Platform

Portfolio Project 3 — a FastAPI microservices platform that orchestrates AI-powered
business workflows with event-driven architecture, human-in-the-loop approval, and
observability. AI is one component of a distributed backend, not the whole app.

This README reflects the state of the project **after an industry-level audit and
upgrade pass** (see `docs/architecture/audit-findings.md` for the full audit report).
Earlier versions of this README overclaimed two things that have since actually been
built for real: Alembic migrations and idempotency at the workflow-execute layer.
Nothing below is documented-but-not-implemented; every claim here has a passing test
or an explicit, honest caveat next to it.

## Quick start

```bash
cp .env.example .env
make up              # docker compose up --build -d
open http://localhost:3000   # static dashboard (frontend still pending a later pass)
```

No LLM API key is required: `LLM_PROVIDER=mock` (the default) runs the full
LangGraph reasoning flow deterministically. Set `LLM_PROVIDER=openai` (or
`groq`) with a real key in `.env` to switch — no code changes needed (ADR-010).

## Architecture

```
Frontend -> API Gateway -> Auth Service / Workflow Service / Audit Service (sync REST)
                                  |
                            RabbitMQ (topic exchange, audit fan-out + retry cascade)
                                  |
                    Celery (broker=RabbitMQ) dispatches:
                    ai-worker -> AI Service -> LangGraph -> LLM Provider
                    integration-worker -> Integration Service -> Mock APIs
                    notification-worker -> Notification Service
```

- **7 services**: api-gateway, auth-service, workflow-service, ai-service,
  integration-service, notification-service, audit-service.
- **3 Celery workers**: ai-worker, integration-worker, notification-worker.
- **Schema-per-service Postgres** (`auth`, `workflow`, `ai`, `audit`, `integration`).
- **LangGraph**, scoped only to the AI reasoning sub-flow inside AI Service.

Full rationale for every major choice: `docs/decisions/ADR-001.md` through
`ADR-012.md`. Full audit findings and what changed as a result:
`docs/architecture/audit-findings.md`.

## Communication matrix

| From | To | Protocol | Purpose |
|---|---|---|---|
| Frontend | API Gateway | HTTP | Public API entry point |
| Gateway | Auth Service | HTTP | Login/register/refresh/logout |
| Gateway | Workflow Service | HTTP | Workflow CRUD, execute, status, approvals |
| Gateway | Audit Service | HTTP (read-only) | Audit log queries |
| Workflow Service | Celery (via RabbitMQ) | AMQP | Dispatch ai_analysis / execute_action / notify steps |
| ai-worker | AI Service | HTTP | Run the LangGraph reasoning flow |
| AI Service | Integration Service | HTTP | Controlled read-only tool calls (customer/order/ticket lookup) |
| integration-worker | Integration Service | HTTP | Execute the approved refund (idempotent) |
| notification-worker | Notification Service | HTTP | Deliver (mocked) notifications |
| Every worker | Workflow Service | HTTP (internal) | Report step completion, carries `X-Correlation-ID` |
| Every service/worker | Audit Service | AMQP (topic exchange, fan-out) | Audit event trail |

## Retry & Dead-Letter Queue behavior

Two retry mechanisms, used deliberately in different places (see ADR-003 for the
full reasoning — this is not an oversight, it's "each consumer uses the mechanism
appropriate to whether it already has a task framework underneath it"):

- **Celery-backed queues** (`ai.processing.queue`, `integration.processing.queue`,
  `notification.queue`): retry via `self.retry(countdown=...)` on a fixed 5s/15s/30s
  schedule (`shared/messaging/retry_policy.py`), but **only for retryable errors** —
  network failures and 5xx responses. A 4xx (e.g. an unknown order) fails
  immediately, one attempt, no retry — retrying a refund call that was rejected
  outright would be pure risk with zero chance of success. After the schedule is
  exhausted, the worker reports the failure to Workflow Service (so the business
  workflow moves to `FAILED`) **and re-raises**, so RabbitMQ actually dead-letters
  the raw message into `<queue>.dlq` — inspectable in the RabbitMQ management UI at
  `localhost:15672`, not just visible as an application log line.
- **Audit Service's raw-AMQP consumer** (the one component with no task framework)
  implements the classic cascade directly: `audit.queue` → failure → `audit.retry.queue`
  (per-message TTL from the same 5s/15s/30s schedule) → TTL expires → dead-lettered
  back into `events.exchange` → re-delivered → after 3 attempts → `audit.queue.dlq`.
  The retry/DLQ *decision* logic is unit-tested in
  `services/audit-service/tests/test_consumer_retry_logic.py` (3 passing tests);
  the AMQP wiring itself needs a live broker to exercise, which this sandbox doesn't
  have — verified via `py_compile` and structural review instead.

## Idempotency

Two layers, same pattern:
- `POST /api/v1/workflows/{id}/execute` accepts an `Idempotency-Key` header. A
  repeated request with the same key (scoped per workflow) returns the existing
  execution instead of starting a second one. Tested in
  `services/workflow-service/tests/test_execute_idempotency.py`.
- `POST /payments/refund` (Integration Service) requires an `Idempotency-Key`; a
  retried refund returns the cached result instead of refunding twice. The
  integration-worker derives this key deterministically (`{execution_id}:{action}`),
  so a Celery-level retry of the same step is automatically idempotent-safe. Tested
  in `services/integration-service/tests/test_idempotency.py`.

## Correlation IDs

Propagated end-to-end: Gateway → services → Celery task kwargs → workers'
downstream HTTP calls → **and back** on the workers' callback to Workflow Service
(this return leg was a gap found during the audit and has been fixed — every hop
now carries `X-Correlation-ID`). Query Audit Service by `correlation_id` to trace
one workflow execution across every service it touched; the E2E test
(`tests/e2e/test_customer_refund_workflow.py`) asserts this explicitly.

## Auth, roles & permissions

- `POST /auth/register`, `POST /auth/login` (issues access + refresh JWT),
  `POST /auth/refresh` (rotates + revokes the old refresh token),
  `POST /auth/logout` (revokes the refresh token).
- Roles: `ADMIN`, `OPERATOR`, `APPROVER`, `USER` → explicit permissions in
  `shared/security/roles.py`.
- Gateway verifies JWTs locally and enforces permissions per route; CORS is
  configured (`GATEWAY_CORS_ORIGINS` env var) so the frontend can call it from a
  different origin.

## Human-in-the-loop & AI safety

AI Service flags `requires_approval` based on risk. Workflow Service pauses in
`WAITING_FOR_APPROVAL` and only proceeds to the refund call after explicit
approval. **Audit fix:** a failed customer/order lookup now correctly `FAIL`s the
workflow instead of asking a human to approve a decision built on missing data
(previously it incorrectly routed to approval). AI's decision output is validated
against a Pydantic schema (`DecisionOutput`); invalid output gets one repair
attempt, then fails safe rather than being trusted blindly.

## Health & readiness

Every service has `GET /health` (liveness — no dependency calls). Four services
with real dependencies also have `GET /ready` (auth, workflow, ai, audit) — cheap,
timeout-bounded checks against Postgres/Redis/RabbitMQ via `shared/health/checks.py`.
Integration/Notification services have no external dependencies to check, so
`/health` alone is sufficient readiness for them.

## Database migrations

`workflow-service` uses real Alembic migrations (`services/workflow-service/alembic/`),
run automatically (`alembic upgrade head`) before the app starts, per its Dockerfile.
This is the reference pattern the other three stateful services (auth, ai, audit)
should be migrated to — they still use `Base.metadata.create_all()` at startup,
which is fine for a fresh database but cannot evolve an existing one. Tracked
honestly in ADR-007's consequences, not hidden.

## Running tests

Each service's tests run independently (real-world microservice pattern — no
shared top-level import of the same `app` package name):

```bash
cd services/auth-service && PYTHONPATH=.:../.. pytest tests/ -v
cd services/api-gateway && PYTHONPATH=.:../.. pytest tests/ -v
cd services/ai-service && PYTHONPATH=.:../.. pytest tests/ -v
cd services/integration-service && PYTHONPATH=.:../.. pytest tests/ -v
cd services/notification-service && PYTHONPATH=.:../.. pytest tests/ -v
cd services/workflow-service && PYTHONPATH=.:../.. pytest tests/ -v
cd services/audit-service && PYTHONPATH=.:../.. pytest tests/ -v
PYTHONPATH=. pytest shared/tests/ -v
```

**43 tests, all passing** as of this build (verified during generation).

For the E2E suite (requires the real stack — not run in the sandbox this was
authored in, see ADR-012 for why):
```bash
docker compose up -d
pytest tests/e2e -v -m e2e
```

## AI evaluation

```bash
cd eval && python generate_dataset.py
cd ../services/ai-service && PYTHONPATH=.:../.. python ../../eval/run_eval.py
```

`eval_report.json` in this repo is a **sample run against LLM_PROVIDER=mock with
Integration Service not running standalone** — tool-call and approval-gate metrics
in that specific file are lower than they'd be against the full stack, because the
mock provider's tool calls fail without Integration Service reachable (which the
"fail-safe" fix now correctly reports as `fail` rather than masking it). Intent
accuracy and structured-output validity are 100% and meaningful standalone. Re-run
against the docker-compose stack for representative approval-gate numbers.

## What's next (documented, not built)

- Alembic for auth-service, ai-service, audit-service (workflow-service is the reference)
- A live run of the E2E suite and the Alembic migration against a real Postgres
  (blocked in this authoring sandbox — no Docker daemon, and the OS package mirror
  needed to install Postgres directly returned 404s)
- OpenTelemetry distributed tracing across the correlation-ID chain
- True database-per-service (separate Postgres instances) for physical isolation
- The full 15-page Next.js dashboard (deferred by request — current frontend is a
  single static dashboard, sufficient to demonstrate the flow)
- Kubernetes manifests (explicitly out of scope per the original spec's v1)

## License / purpose

Portfolio project. Not a production deployment.
