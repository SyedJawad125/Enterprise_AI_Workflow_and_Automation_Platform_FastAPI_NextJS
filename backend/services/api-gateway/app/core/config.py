import os

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth-service:8001")
WORKFLOW_SERVICE_URL = os.environ.get("WORKFLOW_SERVICE_URL", "http://workflow-service:8002")
AUDIT_SERVICE_URL = os.environ.get("AUDIT_SERVICE_URL", "http://audit-service:8006")
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

RATE_LIMITS = {
    # (requests, window_seconds)
    "auth": (10, 60),
    "workflow_create": (30, 60),
    "workflow_execute": (20, 60),
    "default": (100, 60),
}
