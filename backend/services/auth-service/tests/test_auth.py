"""
Auth Service test suite: registration, login, JWT issuance, refresh-token
rotation + revocation, logout, and role -> permission mapping. This mirrors
the auth coverage from Projects 1 and 2, adapted to this service's
standalone JWT/RBAC design (spec sections 6 and 31).
"""
import pytest
from httpx import AsyncClient, ASGITransport

from shared.security import permissions_for_role, decode_token


@pytest.mark.asyncio
async def test_register_creates_user_with_default_role(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/auth/register", json={
            "email": "alice@example.com", "password": "SuperSecret1",
        })
    assert resp.status_code == 201
    data = resp.json()
    assert data["role"] == "USER"
    assert set(data["permissions"]) == set(permissions_for_role("USER"))


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/auth/register", json={"email": "bob@example.com", "password": "SuperSecret1"})
        resp = await client.post("/auth/register", json={"email": "bob@example.com", "password": "AnotherPass1"})
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "EMAIL_TAKEN"


@pytest.mark.asyncio
async def test_login_succeeds_with_correct_credentials_and_issues_tokens(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/auth/register", json={
            "email": "carol@example.com", "password": "SuperSecret1", "role": "OPERATOR",
        })
        resp = await client.post("/auth/login", json={"email": "carol@example.com", "password": "SuperSecret1"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data and "refresh_token" in data

    access_payload = decode_token(data["access_token"])
    assert access_payload.type == "access"
    assert access_payload.role == "OPERATOR"
    assert "workflow:execute" in access_payload.permissions


@pytest.mark.asyncio
async def test_login_fails_with_wrong_password(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/auth/register", json={"email": "dave@example.com", "password": "SuperSecret1"})
        resp = await client.post("/auth/login", json={"email": "dave@example.com", "password": "WrongPassword"})
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "AUTHENTICATION_ERROR"


@pytest.mark.asyncio
async def test_refresh_rotates_token_and_revokes_previous(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/auth/register", json={"email": "erin@example.com", "password": "SuperSecret1"})
        login_resp = await client.post("/auth/login", json={"email": "erin@example.com", "password": "SuperSecret1"})
        old_refresh = login_resp.json()["refresh_token"]

        refresh_resp = await client.post("/auth/refresh", json={"refresh_token": old_refresh})
        assert refresh_resp.status_code == 200
        new_refresh = refresh_resp.json()["refresh_token"]
        assert new_refresh != old_refresh

        # Using the OLD refresh token again must now fail -- it was rotated/revoked.
        reuse_resp = await client.post("/auth/refresh", json={"refresh_token": old_refresh})
        assert reuse_resp.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/auth/register", json={"email": "frank@example.com", "password": "SuperSecret1"})
        login_resp = await client.post("/auth/login", json={"email": "frank@example.com", "password": "SuperSecret1"})
        refresh_token = login_resp.json()["refresh_token"]

        logout_resp = await client.post("/auth/logout", json={"refresh_token": refresh_token})
        assert logout_resp.status_code == 204

        reuse_resp = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert reuse_resp.status_code == 401


@pytest.mark.parametrize("role,expected_permission", [
    ("ADMIN", "admin:manage"),
    ("OPERATOR", "workflow:execute"),
    ("APPROVER", "workflow:approve"),
    ("USER", "workflow:create"),
])
def test_role_permission_mapping(role, expected_permission):
    assert expected_permission in permissions_for_role(role)
