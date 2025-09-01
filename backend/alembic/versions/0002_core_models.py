"""Create core models tables

Revision ID: 0002_core_models
Revises: 0001_initial
Create Date: 2025-08-17

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.
revision = "0002_core_models"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        "users",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="viewer"),
        sa.Column("is_master_user", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("avatar_url", sa.String(length=500)),
        sa.Column("bio", sa.Text()),
        sa.Column("company", sa.String(length=255)),
        sa.Column("job_title", sa.String(length=255)),
        sa.Column("phone", sa.String(length=50)),
        sa.Column("location", sa.String(length=255)),
        sa.Column("timezone", sa.String(length=50), server_default="UTC"),
        sa.Column("preferences", pg.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("notification_settings", pg.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("ui_settings", pg.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("last_login", sa.DateTime()),
        sa.Column("last_activity", sa.DateTime()),
        sa.Column("failed_login_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("locked_until", sa.DateTime()),
        sa.Column("password_changed_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("username", name="uq_users_username"),
        sa.Index("ix_users_email", "email"),
        sa.Index("ix_users_username", "username"),
    )

    # Projects table
    op.create_table(
        "projects",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("owner_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("cloud_providers", pg.JSONB(astext_type=sa.Text())),
        sa.Column("regions", pg.JSONB(astext_type=sa.Text())),
        sa.Column("tags", pg.JSONB(astext_type=sa.Text())),
        sa.Column("monthly_budget", sa.Integer()),
        sa.Column("cost_alerts_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("cost_alert_threshold", sa.Integer(), nullable=False, server_default="80"),
        sa.Column("security_scan_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("compliance_frameworks", pg.JSONB(astext_type=sa.Text())),
        sa.Column("ai_insights_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("ai_model_preferences", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("slug", name="uq_projects_slug"),
        sa.Index("ix_projects_name", "name"),
    )

    # Cost analyses table
    op.create_table(
        "cost_analyses",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("analysis_type", sa.String(length=50), nullable=False, server_default="comprehensive"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("cloud_provider", sa.String(length=50), nullable=False),
        sa.Column("regions", pg.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("services", pg.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("accounts", pg.JSONB(astext_type=sa.Text())),
        sa.Column("date_from", sa.DateTime(), nullable=False),
        sa.Column("date_to", sa.DateTime(), nullable=False),
        sa.Column("analysis_period", sa.String(length=20), nullable=False, server_default="30d"),
        sa.Column("total_cost", sa.Float(), nullable=False, server_default="0"),
        sa.Column("total_cost_formatted", sa.String(length=50)),
        sa.Column("cost_breakdown", pg.JSONB(astext_type=sa.Text())),
        sa.Column("cost_by_service", pg.JSONB(astext_type=sa.Text())),
        sa.Column("cost_by_region", pg.JSONB(astext_type=sa.Text())),
        sa.Column("cost_by_account", pg.JSONB(astext_type=sa.Text())),
        sa.Column("cost_by_tag", pg.JSONB(astext_type=sa.Text())),
        sa.Column("unit_economics", pg.JSONB(astext_type=sa.Text())),
        sa.Column("cost_efficiency_score", sa.Float()),
        sa.Column("cost_optimization_potential", sa.Float()),
        sa.Column("budget_variance", sa.Float()),
        sa.Column("forecast_accuracy", sa.Float()),
        sa.Column("cost_trends", pg.JSONB(astext_type=sa.Text())),
        sa.Column("anomaly_detection", pg.JSONB(astext_type=sa.Text())),
        sa.Column("seasonal_patterns", pg.JSONB(astext_type=sa.Text())),
        sa.Column("growth_projections", pg.JSONB(astext_type=sa.Text())),
        sa.Column("recommendations_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("savings_potential", sa.Float(), nullable=False, server_default="0"),
        sa.Column("implemented_savings", sa.Float(), nullable=False, server_default="0"),
        sa.Column("data_quality_score", sa.Float()),
        sa.Column("data_completeness", sa.Float()),
        sa.Column("last_data_refresh", sa.DateTime()),
        sa.Column("data_sources", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("started_at", sa.DateTime()),
        sa.Column("completed_at", sa.DateTime()),
        sa.Column("error_message", sa.Text()),
    )

    # Security scans table
    op.create_table(
        "security_scans",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("scan_type", sa.String(length=50), nullable=False),
        sa.Column("scan_method", sa.String(length=50), nullable=False, server_default="automated"),
        sa.Column("target_resources", pg.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("scan_config", pg.JSONB(astext_type=sa.Text())),
        sa.Column("compliance_frameworks", pg.JSONB(astext_type=sa.Text())),
        sa.Column("scan_rules", pg.JSONB(astext_type=sa.Text())),
        sa.Column("exclusions", pg.JSONB(astext_type=sa.Text())),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("current_step", sa.String(length=100)),
        sa.Column("estimated_completion", sa.DateTime()),
        sa.Column("vulnerabilities_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("critical_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("high_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("medium_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("low_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("info_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("compliance_score", sa.Float()),
        sa.Column("compliance_status", sa.String(length=20)),
        sa.Column("controls_total", sa.Integer()),
        sa.Column("controls_passed", sa.Integer()),
        sa.Column("controls_failed", sa.Integer()),
        sa.Column("controls_partial", sa.Integer()),
        sa.Column("security_score", sa.Float()),
        sa.Column("risk_score", sa.Float()),
        sa.Column("threat_level", sa.String(length=20)),
        sa.Column("attack_surface", pg.JSONB(astext_type=sa.Text())),
        sa.Column("scan_duration", sa.Integer()),
        sa.Column("resources_scanned", sa.Integer()),
        sa.Column("scan_coverage", sa.Float()),
        sa.Column("false_positive_rate", sa.Float()),
        sa.Column("data_quality_score", sa.Float()),
        sa.Column("scan_accuracy", sa.Float()),
        sa.Column("validation_status", sa.String(length=20)),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("started_at", sa.DateTime()),
        sa.Column("completed_at", sa.DateTime()),
        sa.Column("error_message", sa.Text()),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("security_scans")
    op.drop_table("cost_analyses")
    op.drop_table("projects")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")


