"""
JWT creation/verification shared by Auth Service (issues tokens) and every
other service + the Gateway (verifies tokens). Sharing this module -- not a
network call -- keeps token verification fast and keeps Auth Service from
being a single point of failure for every request in the system.
"""
from __future__ import annotations

import os
import time
import uuid
from typing import Any, Optional

import jwt
from pydantic import BaseModel

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_SECONDS = int(os.environ.get("ACCESS_TOKEN_TTL_SECONDS", 900))       # 15 min
REFRESH_TOKEN_TTL_SECONDS = int(os.environ.get("REFRESH_TOKEN_TTL_SECONDS", 1209600))  # 14 days


class TokenPayload(BaseModel):
    sub: str
    role: str
    permissions: list[str]
    type: str
    jti: str
    exp: int
    iat: int


def _build(sub: str, role: str, permissions: list[str], token_type: str, ttl: int) -> str:
    now = int(time.time())
    payload = {
        "sub": sub,
        "role": role,
        "permissions": permissions,
        "type": token_type,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + ttl,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_access_token(sub: str, role: str, permissions: list[str]) -> str:
    return _build(sub, role, permissions, "access", ACCESS_TOKEN_TTL_SECONDS)


def create_refresh_token(sub: str, role: str, permissions: list[str]) -> str:
    return _build(sub, role, permissions, "refresh", REFRESH_TOKEN_TTL_SECONDS)


def decode_token(token: str) -> TokenPayload:
    data: dict[str, Any] = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return TokenPayload(**data)
