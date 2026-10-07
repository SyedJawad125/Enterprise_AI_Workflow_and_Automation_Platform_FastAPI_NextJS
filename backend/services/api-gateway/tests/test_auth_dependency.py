"""
Tests the Gateway's local JWT verification + RBAC dependency in isolation
(no network calls to Auth Service needed -- the Gateway verifies the shared
HS256 secret directly, per ADR on Gateway responsibilities).
"""
import time

import jwt
import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from app.auth import require_auth, require_permission
from shared.exceptions import install_exception_handlers
from shared.security.jwt_utils import JWT_SECRET, JWT_ALGORITHM

app = FastAPI()
install_exception_handlers(app)


@app.get("/whoami")
def whoami(user=Depends(require_auth)):
    return {"sub": user.sub, "role": user.role}


@app.get("/admin-only")
def admin_only(user=Depends(require_permission("admin:manage"))):
    return {"ok": True}


client = TestClient(app)


def make_token(role="USER", permissions=None, token_type="access", expired=False):
    now = int(time.time())
    payload = {
        "sub": "user-123", "role": role, "permissions": permissions or [],
        "type": token_type, "jti": "jti-1",
        "iat": now, "exp": now - 10 if expired else now + 900,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def test_missing_authorization_header_is_rejected():
    resp = client.get("/whoami")
    assert resp.status_code == 401


def test_valid_token_is_accepted():
    token = make_token()
    resp = client.get("/whoami", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["sub"] == "user-123"


def test_expired_token_is_rejected():
    token = make_token(expired=True)
    resp = client.get("/whoami", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401


def test_refresh_token_cannot_be_used_as_access_token():
    token = make_token(token_type="refresh")
    resp = client.get("/whoami", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401


def test_missing_permission_is_forbidden():
    token = make_token(permissions=["workflow:read"])
    resp = client.get("/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_correct_permission_is_authorized():
    token = make_token(permissions=["admin:manage"])
    resp = client.get("/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
