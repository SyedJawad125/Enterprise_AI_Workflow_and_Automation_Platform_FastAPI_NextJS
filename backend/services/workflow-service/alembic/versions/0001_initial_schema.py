"""initial workflow schema

Revision ID: 0001
Revises:
Create Date: 2026-09-21

Hand-written to exactly match app/models.py at the time this was cut, since
this is the FIRST migration (no live database was available to autogenerate
against in the environment this was authored in). Future migrations should
use `alembic revision --autogenerate -m "..."` against a running Postgres
so they're generated from a real schema diff, not hand-written like this one.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "workflows",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(1000), nullable=False, server_default=""),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        schema="workflow",
    )

    op.create_table(
        "workflow_executions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workflow_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("workflow.workflows.id"), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=False),
        sa.Column("idempotency_key", sa.String(255), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="CREATED"),
        sa.Column("current_step", sa.String(64), nullable=False, server_default=""),
        sa.Column("input_data", postgresql.JSON(), nullable=False, server_default="{}"),
        sa.Column("result_data", postgresql.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("workflow_id", "idempotency_key", name="uq_execution_workflow_idempotency_key"),
        schema="workflow",
    )
    op.create_index("ix_workflow_executions_correlation_id", "workflow_executions", ["correlation_id"], schema="workflow")
    op.create_index("ix_workflow_executions_idempotency_key", "workflow_executions", ["idempotency_key"], schema="workflow")

    op.create_table(
        "step_executions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("execution_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("workflow.workflow_executions.id"), nullable=False),
        sa.Column("step_name", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="RUNNING"),
        sa.Column("result", postgresql.JSON(), nullable=False, server_default="{}"),
        sa.Column("error", sa.String(2000), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        schema="workflow",
    )
    op.create_index("ix_step_executions_execution_id", "step_executions", ["execution_id"], schema="workflow")

    op.create_table(
        "approvals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("execution_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("workflow.workflow_executions.id"), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("recommendation", postgresql.JSON(), nullable=False, server_default="{}"),
        sa.Column("risk_level", sa.String(16), nullable=False, server_default="low"),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("decided_by", sa.String(64), nullable=True),
        schema="workflow",
    )
    op.create_index("ix_approvals_execution_id", "approvals", ["execution_id"], schema="workflow")

    op.create_table(
        "execution_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("execution_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("payload", postgresql.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        schema="workflow",
    )
    op.create_index("ix_execution_events_execution_id", "execution_events", ["execution_id"], schema="workflow")


def downgrade() -> None:
    op.drop_table("execution_events", schema="workflow")
    op.drop_table("approvals", schema="workflow")
    op.drop_table("step_executions", schema="workflow")
    op.drop_table("workflow_executions", schema="workflow")
    op.drop_table("workflows", schema="workflow")
