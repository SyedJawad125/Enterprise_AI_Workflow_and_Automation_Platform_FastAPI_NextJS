"""
In-memory mock enterprise systems so the whole platform runs without any
paid external API. This is the ONLY place that "knows about" customers,
orders, tickets and payments -- everything else (AI Service's tools,
workers) must go through this service's HTTP API, never the dict directly.
"""
from __future__ import annotations

CUSTOMERS = {
    "cust_1001": {
        "id": "cust_1001",
        "name": "Amina Raza",
        "email": "amina.raza@example.com",
        "tier": "gold",
        "since": "2021-03-14",
    },
    "cust_1002": {
        "id": "cust_1002",
        "name": "Daniyal Khan",
        "email": "daniyal.khan@example.com",
        "tier": "standard",
        "since": "2023-07-02",
    },
}

ORDERS = {
    "ord_5001": {
        "id": "ord_5001",
        "customer_id": "cust_1001",
        "product": "Wireless Headphones - Model X",
        "amount": 149.99,
        "currency": "USD",
        "status": "delivered",
        "delivered_at": "2026-09-10",
    },
    "ord_5002": {
        "id": "ord_5002",
        "customer_id": "cust_1002",
        "product": "Smart Blender Pro",
        "amount": 89.50,
        "currency": "USD",
        "status": "delivered",
        "delivered_at": "2026-09-05",
    },
}

TICKETS = {
    "tick_9001": {
        "id": "tick_9001",
        "customer_id": "cust_1001",
        "subject": "Wrong item received",
        "status": "open",
        "history": ["Customer reports receiving a different headphone color than ordered."],
    },
}

# Populated at runtime as refunds are executed
PAYMENTS: dict[str, dict] = {}

# Idempotency store: idempotency_key -> stored response
IDEMPOTENCY_STORE: dict[str, dict] = {}
