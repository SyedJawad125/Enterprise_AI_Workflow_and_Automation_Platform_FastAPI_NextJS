import jwt
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import JSONResponse

from shared.exceptions import AuthenticationError, ValidationAppError, install_exception_handlers
from shared.health import check_postgres
from shared.logging.logger import RequestContextMiddleware, get_logger
from shared.security import create_access_token, create_refresh_token, decode_token, permissions_for_role

from app.db import get_db, init_models, engine
from app.models import RefreshToken, User
from app.schemas import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.security import hash_password, verify_password

logger = get_logger("auth-service")

app = FastAPI(title="Auth Service")
app.add_middleware(RequestContextMiddleware)
install_exception_handlers(app)


@app.on_event("startup")
async def on_startup():
    await init_models()
    logger.info("auth-service started")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth-service"}


@app.get("/ready")
async def ready():
    postgres_status = await check_postgres(engine)
    status = "ready" if postgres_status == "healthy" else "not_ready"
    return JSONResponse(
        status_code=200 if status == "ready" else 503,
        content={"status": status, "service": "auth-service", "dependencies": {"postgres": postgres_status}},
    )


@app.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise ValidationAppError("A user with this email already exists", code="EMAIL_TAKEN")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    logger.info("user registered", extra={"user_id": str(user.id), "role": user.role})
    return UserResponse(
        id=str(user.id), email=user.email, role=user.role, permissions=permissions_for_role(user.role)
    )


@app.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password) or not user.is_active:
        raise AuthenticationError("Invalid email or password")

    permissions = permissions_for_role(user.role)
    access = create_access_token(str(user.id), user.role, permissions)
    refresh = create_refresh_token(str(user.id), user.role, permissions)

    refresh_payload = decode_token(refresh)
    db.add(RefreshToken(user_id=user.id, jti=refresh_payload.jti))
    await db.commit()

    logger.info("user logged in", extra={"user_id": str(user.id)})
    return TokenResponse(access_token=access, refresh_token=refresh)


@app.post("/auth/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        data = decode_token(payload.refresh_token)
    except jwt.PyJWTError:
        raise AuthenticationError("Invalid refresh token")

    if data.type != "refresh":
        raise AuthenticationError("Not a refresh token")

    token_row = await db.scalar(select(RefreshToken).where(RefreshToken.jti == data.jti))
    if not token_row or token_row.revoked:
        raise AuthenticationError("Refresh token has been revoked")

    permissions = permissions_for_role(data.role)
    new_access = create_access_token(data.sub, data.role, permissions)
    new_refresh = create_refresh_token(data.sub, data.role, permissions)

    token_row.revoked = True  # rotate refresh tokens on every use
    new_payload = decode_token(new_refresh)
    db.add(RefreshToken(user_id=token_row.user_id, jti=new_payload.jti))
    await db.commit()

    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


@app.post("/auth/logout", status_code=204)
async def logout(payload: LogoutRequest, db: AsyncSession = Depends(get_db)):
    try:
        data = decode_token(payload.refresh_token)
    except jwt.PyJWTError:
        return None
    token_row = await db.scalar(select(RefreshToken).where(RefreshToken.jti == data.jti))
    if token_row:
        token_row.revoked = True
        await db.commit()
    return None


@app.get("/auth/verify", response_model=UserResponse)
async def verify(token: str):
    """Internal endpoint the Gateway can call if it prefers remote verification
    over local JWT decoding. In this project the Gateway verifies locally
    (shared secret) for latency; this endpoint exists for services/tests that
    want an authoritative check without needing the shared secret."""
    try:
        data = decode_token(token)
    except jwt.PyJWTError:
        raise AuthenticationError("Invalid token")
    if data.type != "access":
        raise AuthenticationError("Not an access token")
    return UserResponse(id=data.sub, email="", role=data.role, permissions=data.permissions)
