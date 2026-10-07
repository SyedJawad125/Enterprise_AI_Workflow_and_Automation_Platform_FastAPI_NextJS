import uuid

from fastapi import FastAPI, Header
from typing import Optional

from shared.exceptions import NotFoundError, ValidationAppError, install_exception_handlers
from shared.logging.logger import RequestContextMiddleware, get_logger

from app.mock_data import CUSTOMERS, ORDERS, TICKETS, PAYMENTS, IDEMPOTENCY_STORE
from app.schemas import RefundRequest, RefundResponse

logger = get_logger("integration-service")

app = FastAPI(title="Integration Service")
app.add_middleware(RequestContextMiddleware)
install_exception_handlers(app)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "integration-service"}


@app.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        raise NotFoundError(f"Customer {customer_id} not found")
    return customer


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise NotFoundError(f"Order {order_id} not found")
    return order


@app.get("/customers/{customer_id}/orders")
async def get_customer_orders(customer_id: str):
    return [o for o in ORDERS.values() if o["customer_id"] == customer_id]


@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        raise NotFoundError(f"Ticket {ticket_id} not found")
    return ticket


@app.get("/customers/{customer_id}/tickets")
async def get_customer_tickets(customer_id: str):
    return [t for t in TICKETS.values() if t["customer_id"] == customer_id]


@app.post("/payments/refund", response_model=RefundResponse)
async def refund(payload: RefundRequest, idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key")):
    """
    Idempotent by design (spec section 20): the same Idempotency-Key returns
    the previously computed result instead of executing the refund again.
    This is what prevents a Celery retry (or a network blip that causes the
    caller to retry) from double-refunding a customer.
    """
    if not idempotency_key:
        raise ValidationAppError("Idempotency-Key header is required for payment operations")

    if idempotency_key in IDEMPOTENCY_STORE:
        cached = IDEMPOTENCY_STORE[idempotency_key]
        logger.info("idempotent replay", extra={"idempotency_key": idempotency_key})
        return RefundResponse(**cached, idempotent_replay=True)

    order = ORDERS.get(payload.order_id)
    if not order:
        raise NotFoundError(f"Order {payload.order_id} not found")

    payment_id = f"pay_{uuid.uuid4().hex[:10]}"
    PAYMENTS[payment_id] = {
        "id": payment_id,
        "order_id": payload.order_id,
        "amount": payload.amount,
        "reason": payload.reason,
        "status": "refunded",
    }

    result = {
        "payment_id": payment_id,
        "order_id": payload.order_id,
        "amount": payload.amount,
        "status": "refunded",
    }
    IDEMPOTENCY_STORE[idempotency_key] = result
    logger.info("refund executed", extra={"payment_id": payment_id, "order_id": payload.order_id})
    return RefundResponse(**result)
