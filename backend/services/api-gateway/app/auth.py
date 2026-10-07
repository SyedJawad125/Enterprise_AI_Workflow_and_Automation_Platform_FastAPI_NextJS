"""
The Gateway verifies JWT access tokens locally (shared HS256 secret with
Auth Service) so authentication doesn't cost a network hop on every
request. Downstream services still receive the decoded identity via
forwarded headers and independently enforce AUTHORIZATION (permission
checks) for sensitive operations -- the Gateway checks "is this a valid,
non-expired token", not "is this user allowed to do X".
"""
from __future__ import annotations

import jwt
from fastapi import Request

from shared.exceptions import AuthenticationError, AuthorizationError
from shared.security import decode_token


def get_bearer_token(request: Request) -> str:
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        raise AuthenticationError("Missing or malformed Authorization header")
    return header.split(" ", 1)[1]


def require_auth(request: Request):
    token = get_bearer_token(request)
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Access token has expired")
    except jwt.PyJWTError:
        raise AuthenticationError("Invalid access token")
    if payload.type != "access":
        raise AuthenticationError("Not an access token")
    return payload


def require_permission(permission: str):
    def _dependency(request: Request):
        payload = require_auth(request)
        if permission not in payload.permissions:
            raise AuthorizationError(f"Missing required permission: {permission}")
        return payload
    return _dependency
