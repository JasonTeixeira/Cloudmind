"""Add project storage tables

Revision ID: 0005_project_storage
Revises: 0004_mfa_tables
Create Date: 2025-08-17

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.
revision = "0005_project_storage"
down_revision = "0004_mfa_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "project_files",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("file_path", sa.String(length=2048), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("directory_path", sa.String(length=1024), nullable=False),
        sa.Column("file_type", sa.String(length=50), nullable=False),
        sa.Column("mime_type", sa.String(length=100)),
        sa.Column("file_size", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("encoding", sa.String(length=20), nullable=False, server_default="utf-8"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("parent_version_id", pg.UUID(as_uuid=True), sa.ForeignKey("project_files.id")),
        sa.Column("is_latest", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("commit_message", sa.Text()),
        sa.Column("commit_author_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("content", sa.Text()),
        sa.Column("binary_content", pg.JSONB(astext_type=sa.Text())),
        sa.Column("storage_location", sa.String(length=500)),
        sa.Column("storage_metadata", pg.JSONB(astext_type=sa.Text())),
        sa.Column("language_detected", sa.String(length=50)),
        sa.Column("complexity_score", sa.Integer()),
        sa.Column("security_scan_results", pg.JSONB(astext_type=sa.Text())),
        sa.Column("ai_analysis", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("updated_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("is_public", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("permissions", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_accessed", sa.DateTime(timezone=True)),
    )
    op.create_index("idx_project_files_project_path", "project_files", ["project_id", "file_path"])
    op.create_index("idx_project_files_type", "project_files", ["file_type"])
    op.create_index("idx_project_files_created_by", "project_files", ["created_by"])
    op.create_index("idx_project_files_updated_at", "project_files", ["updated_at"])
    op.create_index("idx_project_files_content_hash", "project_files", ["content_hash"])
    op.create_unique_constraint("uq_project_file_version", "project_files", ["project_id", "file_path", "version"])

    op.create_table(
        "project_directories",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("directory_path", sa.String(length=1024), nullable=False),
        sa.Column("directory_name", sa.String(length=255), nullable=False),
        sa.Column("parent_directory_id", pg.UUID(as_uuid=True), sa.ForeignKey("project_directories.id")),
        sa.Column("total_files", sa.Integer(), server_default="0"),
        sa.Column("total_size", sa.BigInteger(), server_default="0"),
        sa.Column("file_types", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("is_public", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("permissions", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("idx_project_directories_project_path", "project_directories", ["project_id", "directory_path"])
    op.create_unique_constraint("uq_project_directory", "project_directories", ["project_id", "directory_path"])

    op.create_table(
        "project_templates",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("subcategory", sa.String(length=100)),
        sa.Column("tags", pg.JSONB(astext_type=sa.Text())),
        sa.Column("file_structure", pg.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("template_files", pg.JSONB(astext_type=sa.Text())),
        sa.Column("variables", pg.JSONB(astext_type=sa.Text())),
        sa.Column("dependencies", pg.JSONB(astext_type=sa.Text())),
        sa.Column("complexity_level", sa.String(length=20)),
        sa.Column("estimated_duration", sa.Integer()),
        sa.Column("technology_stack", pg.JSONB(astext_type=sa.Text())),
        sa.Column("architecture_pattern", sa.String(length=100)),
        sa.Column("template_version", sa.String(length=20), server_default="1.0.0"),
        sa.Column("is_validated", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("validation_results", pg.JSONB(astext_type=sa.Text())),
        sa.Column("test_coverage", sa.Integer()),
        sa.Column("usage_count", sa.Integer(), server_default="0"),
        sa.Column("rating", sa.Integer()),
        sa.Column("reviews", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("is_public", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_featured", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("shared_with", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("idx_project_templates_category", "project_templates", ["category"])
    op.create_index("idx_project_templates_created_by", "project_templates", ["created_by"])
    op.create_index("idx_project_templates_public", "project_templates", ["is_public"])
    op.create_index("idx_project_templates_featured", "project_templates", ["is_featured"])

    op.create_table(
        "project_documentation",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("doc_type", sa.String(length=50), nullable=False),
        sa.Column("doc_path", sa.String(length=1024)),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_format", sa.String(length=20), server_default="markdown"),
        sa.Column("table_of_contents", pg.JSONB(astext_type=sa.Text())),
        sa.Column("doc_metadata", pg.JSONB(astext_type=sa.Text())),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("parent_version_id", pg.UUID(as_uuid=True), sa.ForeignKey("project_documentation.id")),
        sa.Column("is_latest", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("change_log", pg.JSONB(astext_type=sa.Text())),
        sa.Column("created_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("updated_by", pg.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("reviewers", pg.JSONB(astext_type=sa.Text())),
        sa.Column("review_status", sa.String(length=20), server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("idx_project_docs_project_type", "project_documentation", ["project_id", "doc_type"])
    op.create_index("idx_project_docs_created_by", "project_documentation", ["created_by"])
    op.create_unique_constraint("uq_project_doc_version", "project_documentation", ["project_id", "doc_path", "version"])

    op.create_table(
        "file_collaboration",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("file_id", pg.UUID(as_uuid=True), sa.ForeignKey("project_files.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", sa.String(length=100), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("cursor_position", sa.Integer()),
        sa.Column("selection_start", sa.Integer()),
        sa.Column("selection_end", sa.Integer()),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("last_activity", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("idx_file_collaboration_file_session", "file_collaboration", ["file_id", "session_id"])
    op.create_index("idx_file_collaboration_user", "file_collaboration", ["user_id"])
    op.create_index("idx_file_collaboration_active", "file_collaboration", ["is_active"])

    op.create_table(
        "file_changes",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("file_id", pg.UUID(as_uuid=True), sa.ForeignKey("project_files.id", ondelete="CASCADE"), nullable=False),
        sa.Column("change_type", sa.String(length=20), nullable=False),
        sa.Column("change_hash", sa.String(length=64), nullable=False),
        sa.Column("old_content", sa.Text()),
        sa.Column("new_content", sa.Text()),
        sa.Column("diff", pg.JSONB(astext_type=sa.Text())),
        sa.Column("line_changes", pg.JSONB(astext_type=sa.Text())),
        sa.Column("change_size", sa.Integer()),
        sa.Column("complexity_change", sa.Integer()),
        sa.Column("author_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("commit_message", sa.Text()),
        sa.Column("branch_name", sa.String(length=100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("idx_file_changes_file_type", "file_changes", ["file_id", "change_type"])
    op.create_index("idx_file_changes_author", "file_changes", ["author_id"])
    op.create_index("idx_file_changes_created_at", "file_changes", ["created_at"])

    op.create_table(
        "project_backups",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("backup_name", sa.String(length=255), nullable=False),
        sa.Column("backup_type", sa.String(length=20), nullable=False),
        sa.Column("backup_reason", sa.String(length=100)),
        sa.Column("file_snapshots", pg.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("metadata_snapshot", pg.JSONB(astext_type=sa.Text())),
        sa.Column("storage_location", sa.String(length=500), nullable=False),
        sa.Column("backup_size", sa.BigInteger()),
        sa.Column("compression_ratio", sa.Float()),
        sa.Column("status", sa.String(length=20), server_default="in_progress"),
        sa.Column("error_message", sa.Text()),
        sa.Column("retention_days", sa.Integer(), server_default="30"),
        sa.Column("is_encrypted", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("encryption_key_id", sa.String(length=100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
    )
    op.create_index("idx_project_backups_project_status", "project_backups", ["project_id", "status"])
    op.create_index("idx_project_backups_created_at", "project_backups", ["created_at"])


def downgrade() -> None:
    op.drop_table("project_backups")
    op.drop_index("idx_file_changes_created_at", table_name="file_changes")
    op.drop_index("idx_file_changes_author", table_name="file_changes")
    op.drop_index("idx_file_changes_file_type", table_name="file_changes")
    op.drop_table("file_changes")
    op.drop_index("idx_file_collaboration_active", table_name="file_collaboration")
    op.drop_index("idx_file_collaboration_user", table_name="file_collaboration")
    op.drop_index("idx_file_collaboration_file_session", table_name="file_collaboration")
    op.drop_table("file_collaboration")
    op.drop_index("idx_project_docs_created_by", table_name="project_documentation")
    op.drop_index("idx_project_docs_project_type", table_name="project_documentation")
    op.drop_constraint("uq_project_doc_version", "project_documentation")
    op.drop_table("project_documentation")
    op.drop_index("idx_project_templates_featured", table_name="project_templates")
    op.drop_index("idx_project_templates_public", table_name="project_templates")
    op.drop_index("idx_project_templates_created_by", table_name="project_templates")
    op.drop_index("idx_project_templates_category", table_name="project_templates")
    op.drop_table("project_templates")
    op.drop_index("idx_project_directories_project_path", table_name="project_directories")
    op.drop_constraint("uq_project_directory", "project_directories")
    op.drop_table("project_directories")
    op.drop_index("idx_project_files_content_hash", table_name="project_files")
    op.drop_index("idx_project_files_updated_at", table_name="project_files")
    op.drop_index("idx_project_files_created_by", table_name="project_files")
    op.drop_index("idx_project_files_type", table_name="project_files")
    op.drop_index("idx_project_files_project_path", table_name="project_files")
    op.drop_constraint("uq_project_file_version", "project_files")
    op.drop_table("project_files")


