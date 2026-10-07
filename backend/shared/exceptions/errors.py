"""
Consistent domain exceptions + error envelope for every service.

Interview point: clients should never see a raw stack trace. Every error
crosses the wire as {"error": {"code", "message", "request_id"}}.
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from shared.logging.logger import get_logger, request_id_var

logger = get_logger("shared.exceptions")


class AppError(Exception):
    status_code = 500
    code = "INTERNAL_ERROR"

    def __init__(self, message: str, code: str | None = None, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class ValidationAppError(AppError):
    status_code = 422
    code = "VALIDATION_ERROR"


class AuthenticationError(AppError):
    status_code = 401
    code = "AUTHENTICATION_ERROR"


class AuthorizationError(AppError):
    status_code = 403
    code = "AUTHORIZATION_ERROR"


class DependencyError(AppError):
    status_code = 503
    code = "DEPENDENCY_UNAVAILABLE"


class ExternalAPIError(AppError):
    status_code = 502
    code = "EXTERNAL_API_ERROR"


class LLMError(AppError):
    status_code = 502
    code = "LLM_ERROR"


def error_response(code: str, message: str, status_code: int = 500) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id_var.get(),
            }
        },
    )


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        logger.warning("handled app error", extra={"error_type": exc.code, "path": str(request.url)})
        return error_response(exc.code, exc.message, exc.status_code)

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception):
        logger.error("unhandled exception", exc_info=exc, extra={"path": str(request.url)})
        return error_response("INTERNAL_ERROR", "An unexpected error occurred", 500)
