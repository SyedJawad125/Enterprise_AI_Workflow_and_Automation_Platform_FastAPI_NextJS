import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import httpx
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response as FastAPIResponse

from shared.exceptions import install_exception_handlers
from shared.logging.logger import RequestContextMiddleware, correlation_id_var, get_logger, request_id_var

from app.auth import require_auth, require_permission
from app.core.config import AUDIT_SERVICE_URL, AUTH_SERVICE_URL, WORKFLOW_SERVICE_URL
from app.rate_limit import check_rate_limit

logger = get_logger("api-gateway")

app = FastAPI(title="API Gateway", version="1.0.0")
app.add_middleware(RequestContextMiddleware)

# CORS: the frontend (served from its own origin, e.g. :3000) calls this
# Gateway (:8000) from the browser -- without this, every browser request
# would be blocked by CORS before it even reaches our rate limiter/auth.
# Origins are configurable via env so a real deployment can lock this down
# to its actual frontend domain instead of the permissive dev default.
_cors_origins = os.environ.get("GATEWAY_CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if _cors_origins == "*" else [o.strip() for o in _cors_origins.split(",")],
    allow_credentials=_cors_origins != "*",  # browsers reject credentials=true combined with origin=*
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Correlation-ID"],
)

install_exception_handlers(app)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}


def _forward_headers(request: Request | None = None) -> dict:
    headers = {}
    if request_id_var.get():
        headers["X-Request-ID"] = request_id_var.get()
    if correlation_id_var.get():
        headers["X-Correlation-ID"] = correlation_id_var.get()
    if request is not None:
        # Pass through client-supplied idempotency keys untouched -- the
        # Gateway must not invent or strip this, since the downstream
        # service (Workflow Service) is what enforces the idempotency
        # contract on it.
        idem = request.headers.get("idempotency-key")
        if idem:
            headers["Idempotency-Key"] = idem
    return headers


async def _proxy(method: str, url: str, json_body: dict | None = None, params: dict | None = None, request: Request | None = None) -> httpx.Response:
    async with httpx.AsyncClient(timeout=30) as client:
        return await client.request(method, url, json=json_body, params=params, headers=_forward_headers(request))


# ------------------------------------------------------------------- Auth

@app.post("/api/v1/auth/register", status_code=201)
async def register(request: Request):
    await check_rate_limit("auth", request.client.host if request.client else "anon")
    body = await request.json()
    resp = await _proxy("POST", f"{AUTH_SERVICE_URL}/auth/register", json_body=body)
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.post("/api/v1/auth/login")
async def login(request: Request):
    await check_rate_limit("auth", request.client.host if request.client else "anon")
    body = await request.json()
    resp = await _proxy("POST", f"{AUTH_SERVICE_URL}/auth/login", json_body=body)
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.post("/api/v1/auth/refresh")
async def refresh(request: Request):
    body = await request.json()
    resp = await _proxy("POST", f"{AUTH_SERVICE_URL}/auth/refresh", json_body=body)
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.post("/api/v1/auth/logout", status_code=204)
async def logout(request: Request):
    body = await request.json()
    await _proxy("POST", f"{AUTH_SERVICE_URL}/auth/logout", json_body=body)
    return None


# --------------------------------------------------------------- Workflows

@app.post("/api/v1/workflows", status_code=201)
async def create_workflow(request: Request, user=Depends(require_permission("workflow:create"))):
    await check_rate_limit("workflow_create", user.sub)
    body = await request.json()
    resp = await _proxy("POST", f"{WORKFLOW_SERVICE_URL}/workflows", json_body=body)
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str, user=Depends(require_permission("workflow:read"))):
    resp = await _proxy("GET", f"{WORKFLOW_SERVICE_URL}/workflows/{workflow_id}")
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.post("/api/v1/workflows/{workflow_id}/execute", status_code=202)
async def execute_workflow(workflow_id: str, request: Request, user=Depends(require_permission("workflow:execute"))):
    await check_rate_limit("workflow_execute", user.sub)
    body = await request.json()
    resp = await _proxy("POST", f"{WORKFLOW_SERVICE_URL}/workflows/{workflow_id}/execute", json_body=body, request=request)
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.get("/api/v1/workflows/executions/{execution_id}/status")
async def execution_status(execution_id: str, user=Depends(require_permission("workflow:read"))):
    resp = await _proxy("GET", f"{WORKFLOW_SERVICE_URL}/workflows/executions/{execution_id}/status")
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


# --------------------------------------------------------------- Approvals

@app.post("/api/v1/approvals/{approval_id}/approve")
async def approve(approval_id: str, request: Request, user=Depends(require_permission("workflow:approve"))):
    body = await request.json() if await request.body() else {"decided_by": user.sub}
    resp = await _proxy("POST", f"{WORKFLOW_SERVICE_URL}/approvals/{approval_id}/approve", json_body=body)
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.post("/api/v1/approvals/{approval_id}/reject")
async def reject(approval_id: str, request: Request, user=Depends(require_permission("workflow:approve"))):
    body = await request.json() if await request.body() else {"decided_by": user.sub}
    resp = await _proxy("POST", f"{WORKFLOW_SERVICE_URL}/approvals/{approval_id}/reject", json_body=body)
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


@app.get("/api/v1/approvals")
async def list_approvals(user=Depends(require_permission("workflow:approve"))):
    resp = await _proxy("GET", f"{WORKFLOW_SERVICE_URL}/approvals")
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")


# ------------------------------------------------------------------- Audit

@app.get("/api/v1/audit/events")
async def audit_events(request: Request, user=Depends(require_permission("audit:read"))):
    resp = await _proxy("GET", f"{AUDIT_SERVICE_URL}/audit/events", params=dict(request.query_params))
    return FastAPIResponse(content=resp.content, status_code=resp.status_code, media_type="application/json")
