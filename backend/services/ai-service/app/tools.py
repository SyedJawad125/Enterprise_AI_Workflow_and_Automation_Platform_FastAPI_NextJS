"""
Controlled tools the AI reasoning flow may call. This is the AI-safety
boundary described in the spec: the LLM never gets raw DB/HTTP access. It
can only request one of these pre-defined, schema-validated operations, and
every call is logged. Side-effecting actions (refund) are deliberately
*not* exposed here -- those only happen after human approval, executed by
Integration Service directly from the Workflow Service / worker, never by
the LLM's own tool loop.
"""
from __future__ import annotations

import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import INTEGRATION_SERVICE_URL
from shared.exceptions import ValidationAppError
from shared.logging.logger import get_logger

logger = get_logger("ai-service.tools")


class CustomerLookupArgs(BaseModel):
    customer_id: str


class OrderLookupArgs(BaseModel):
    order_id: str


class TicketLookupArgs(BaseModel):
    ticket_id: str


TOOL_SCHEMAS = {
    "customer_lookup": CustomerLookupArgs,
    "order_lookup": OrderLookupArgs,
    "ticket_lookup": TicketLookupArgs,
}


async def execute_tool(tool_name: str, arguments: dict) -> dict:
    schema = TOOL_SCHEMAS.get(tool_name)
    if schema is None:
        raise ValidationAppError(f"Unknown or disallowed tool: {tool_name}")

    try:
        validated = schema(**arguments)
    except ValidationError as exc:
        raise ValidationAppError(f"Invalid arguments for tool {tool_name}: {exc}")

    logger.info("tool call", extra={"tool": tool_name, "arguments": validated.model_dump()})

    async with httpx.AsyncClient(base_url=INTEGRATION_SERVICE_URL, timeout=10) as client:
        if tool_name == "customer_lookup":
            resp = await client.get(f"/customers/{validated.customer_id}")
        elif tool_name == "order_lookup":
            resp = await client.get(f"/orders/{validated.order_id}")
        elif tool_name == "ticket_lookup":
            resp = await client.get(f"/tickets/{validated.ticket_id}")
        resp.raise_for_status()
        return resp.json()
