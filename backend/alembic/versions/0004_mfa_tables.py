"""Add MFA tables

Revision ID: 0004_mfa_tables
Revises: 0003_more_models
Create Date: 2025-08-17

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.
revision = "0004_mfa_tables"
down_revision = "0003_more_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "mfa_secrets",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("totp_secret", sa.String(length=255)),
        sa.Column("totp_algorithm", sa.String(length=20), nullable=False, server_default="SHA1"),
        sa.Column("totp_digits", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("totp_period", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("backup_codes", pg.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("phone_number", sa.String(length=50)),
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("hardware_token_id", sa.String(length=255)),
        sa.Column("mfa_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mfa_method", sa.String(length=20), nullable=False, server_default="totp"),
        sa.Column("mfa_status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("require_mfa", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("grace_period_days", sa.Integer(), nullable=False, server_default="7"),
        sa.Column("max_failed_attempts", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("lockout_duration_minutes", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_used_at", sa.DateTime()),
    )

    op.create_table(
        "mfa_attempts",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("mfa_secret_id", pg.UUID(as_uuid=True), sa.ForeignKey("mfa_secrets.id"), nullable=False),
        sa.Column("method", sa.String(length=20), nullable=False),
        sa.Column("code", sa.String(length=255), nullable=False),
        sa.Column("failed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("ip_address", sa.String(length=45)),
        sa.Column("user_agent", sa.Text()),
        sa.Column("location", sa.String(length=255)),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "mfa_sessions",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("session_token", sa.String(length=255), nullable=False, unique=True),
        sa.Column("device_id", sa.String(length=255)),
        sa.Column("device_name", sa.String(length=255)),
        sa.Column("trusted_device", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("remember_device", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("ip_address", sa.String(length=45)),
        sa.Column("user_agent", sa.Text()),
        sa.Column("location", sa.String(length=255)),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("last_used_at", sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table("mfa_sessions")
    op.drop_table("mfa_attempts")
    op.drop_table("mfa_secrets")


