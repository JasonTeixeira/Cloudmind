"""Add more core tables

Revision ID: 0003_more_models
Revises: 0002_core_models
Create Date: 2025-08-17

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.
revision = "0003_more_models"
down_revision = "0002_core_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # notifications
    op.create_table(
        "notifications",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=True),
        sa.Column("type", sa.String(length=20), nullable=False, server_default="system"),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("data", pg.JSONB(astext_type=sa.Text())),
        sa.Column("email_sent", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("push_sent", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("in_app_sent", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True)),
        sa.Column("read_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
    )

    # project_members
    op.create_table(
        "project_members",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("invited_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="viewer"),
        sa.Column("permissions", sa.Text()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_active", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("invitation_token", sa.String(length=255), unique=True),
        sa.Column("invitation_expires_at", sa.DateTime(timezone=True)),
        sa.Column("invitation_accepted_at", sa.DateTime(timezone=True)),
    )

    # infrastructures
    op.create_table(
        "infrastructures",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("environment", sa.String(length=50), nullable=False, server_default="production"),
        sa.Column("cloud_provider", sa.String(length=50), nullable=False),
        sa.Column("region", sa.String(length=100), nullable=False),
        sa.Column("account_id", sa.String(length=255)),
        sa.Column("infrastructure_as_code", pg.JSONB(astext_type=sa.Text())),
        sa.Column("tags", pg.JSONB(astext_type=sa.Text())),
        sa.Column("cost_center", sa.String(length=100)),
        sa.Column("monitoring_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("alerting_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("health_status", sa.String(length=20), nullable=False, server_default="healthy"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_sync", sa.DateTime(timezone=True)),
    )

    # resources
    op.create_table(
        "resources",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("infrastructure_id", pg.UUID(as_uuid=True), sa.ForeignKey("infrastructures.id"), nullable=False),
        sa.Column("resource_id", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("resource_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("instance_type", sa.String(length=100)),
        sa.Column("size", sa.String(length=100)),
        sa.Column("availability_zone", sa.String(length=100)),
        sa.Column("private_ip", sa.String(length=45)),
        sa.Column("public_ip", sa.String(length=45)),
        sa.Column("vpc_id", sa.String(length=255)),
        sa.Column("subnet_id", sa.String(length=255)),
        sa.Column("hourly_cost", sa.Float()),
        sa.Column("monthly_cost", sa.Float()),
        sa.Column("cost_currency", sa.String(length=3), nullable=False, server_default="USD"),
        sa.Column("cpu_utilization", sa.Float()),
        sa.Column("memory_utilization", sa.Float()),
        sa.Column("disk_utilization", sa.Float()),
        sa.Column("network_throughput", sa.Float()),
        sa.Column("configuration", pg.JSONB(astext_type=sa.Text())),
        sa.Column("tags", pg.JSONB(astext_type=sa.Text())),
        sa.Column("resource_metadata", pg.JSONB(astext_type=sa.Text())),
        sa.Column("security_groups", pg.JSONB(astext_type=sa.Text())),
        sa.Column("encryption_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("backup_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_updated", sa.DateTime(timezone=True)),
    )

    # ai models
    op.create_table(
        "ai_models",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("provider", sa.String(length=100), nullable=False),
        sa.Column("model_type", sa.String(length=100), nullable=False),
        sa.Column("parameters", pg.JSONB(astext_type=sa.Text())),
        sa.Column("capabilities", pg.JSONB(astext_type=sa.Text())),
        sa.Column("limitations", pg.JSONB(astext_type=sa.Text())),
        sa.Column("accuracy_score", sa.Float()),
        sa.Column("latency_ms", sa.Integer()),
        sa.Column("cost_per_token", sa.Float()),
        sa.Column("total_requests", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("successful_requests", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_requests", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_used", sa.DateTime(timezone=True)),
    )

    # ai insights
    op.create_table(
        "ai_insights",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("insight_type", sa.String(length=50), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("ai_model_id", pg.UUID(as_uuid=True), sa.ForeignKey("ai_models.id"), nullable=True),
        sa.Column("confidence_score", sa.Float()),
        sa.Column("ai_model_version", sa.String(length=50)),
        sa.Column("analysis_data", pg.JSONB(astext_type=sa.Text())),
        sa.Column("recommendations", pg.JSONB(astext_type=sa.Text())),
        sa.Column("impact_analysis", pg.JSONB(astext_type=sa.Text())),
        sa.Column("implementation_steps", pg.JSONB(astext_type=sa.Text())),
        sa.Column("affected_resources", pg.JSONB(astext_type=sa.Text())),
        sa.Column("tags", pg.JSONB(astext_type=sa.Text())),
        sa.Column("categories", pg.JSONB(astext_type=sa.Text())),
        sa.Column("is_implemented", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_acknowledged", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_dismissed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("implemented_at", sa.DateTime(timezone=True)),
        sa.Column("implemented_by", sa.String(length=255)),
        sa.Column("implementation_notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ai_insights")
    op.drop_table("ai_models")
    op.drop_table("resources")
    op.drop_table("infrastructures")
    op.drop_table("project_members")
    op.drop_table("notifications")


