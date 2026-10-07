"""Central RBAC definitions -- roles map to a fixed permission set."""

PERMISSIONS = {
    "workflow:create",
    "workflow:read",
    "workflow:execute",
    "workflow:approve",
    "workflow:delete",
    "audit:read",
    "admin:manage",
}

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "ADMIN": [
        "workflow:create", "workflow:read", "workflow:execute",
        "workflow:approve", "workflow:delete", "audit:read", "admin:manage",
    ],
    "OPERATOR": ["workflow:create", "workflow:read", "workflow:execute"],
    "APPROVER": ["workflow:read", "workflow:approve"],
    "USER": ["workflow:read", "workflow:create"],
}


def permissions_for_role(role: str) -> list[str]:
    return ROLE_PERMISSIONS.get(role, [])
