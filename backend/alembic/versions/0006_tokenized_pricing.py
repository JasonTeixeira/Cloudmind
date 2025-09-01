"""Tokenized pricing system

Revision ID: 0006_tokenized_pricing
Revises: 0005_project_storage
Create Date: 2024-08-19 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0006_tokenized_pricing'
down_revision: Union[str, None] = '0005_project_storage'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE unittype AS ENUM ('per_resource', 'per_hour', 'flat_rate', 'percentage_savings', 'per_gb', 'per_api_call')")
    op.execute("CREATE TYPE servicecategory AS ENUM ('scanning', 'optimization', 'documentation', 'implementation', 'monitoring', 'consulting', 'training')")
    op.execute("CREATE TYPE engagementstatus AS ENUM ('draft', 'proposed', 'approved', 'in_progress', 'completed', 'cancelled', 'on_hold')")

    # Create service_tokens table
    op.create_table('service_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('base_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('unit_type', postgresql.ENUM('per_resource', 'per_hour', 'flat_rate', 'percentage_savings', 'per_gb', 'per_api_call', name='unittype'), nullable=False),
        sa.Column('category', postgresql.ENUM('scanning', 'optimization', 'documentation', 'implementation', 'monitoring', 'consulting', 'training', name='servicecategory'), nullable=False),
        sa.Column('minimum_quantity', sa.Integer(), nullable=True, default=1),
        sa.Column('maximum_quantity', sa.Integer(), nullable=True),
        sa.Column('volume_discount_threshold', sa.Integer(), nullable=True),
        sa.Column('volume_discount_rate', sa.Numeric(precision=5, scale=4), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('requires_approval', sa.Boolean(), nullable=True, default=False),
        sa.Column('estimated_duration_hours', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create client_engagements table
    op.create_table('client_engagements',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', postgresql.ENUM('draft', 'proposed', 'approved', 'in_progress', 'completed', 'cancelled', 'on_hold', name='engagementstatus'), nullable=True, default='draft'),
        sa.Column('total_cost', sa.Numeric(precision=12, scale=2), nullable=True, default=0),
        sa.Column('estimated_cost', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('approved_budget', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('progress_percentage', sa.Integer(), nullable=True, default=0),
        sa.Column('resources_discovered', sa.Integer(), nullable=True, default=0),
        sa.Column('resources_analyzed', sa.Integer(), nullable=True, default=0),
        sa.Column('optimizations_identified', sa.Integer(), nullable=True, default=0),
        sa.Column('projected_monthly_savings', sa.Numeric(precision=12, scale=2), nullable=True, default=0),
        sa.Column('actual_monthly_savings', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('roi_percentage', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('payback_months', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('estimated_completion_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('actual_completion_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('github_repo_url', sa.String(length=500), nullable=True),
        sa.Column('github_repo_created', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create engagement_items table
    op.create_table('engagement_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('engagement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('service_token_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, default=1),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('discount_applied', sa.Numeric(precision=5, scale=4), nullable=True, default=0),
        sa.Column('is_completed', sa.Boolean(), nullable=True, default=False),
        sa.Column('completion_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('estimated_hours', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('actual_hours', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['engagement_id'], ['client_engagements.id'], ),
        sa.ForeignKeyConstraint(['service_token_id'], ['service_tokens.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create progress_events table
    op.create_table('progress_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('engagement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('event_description', sa.Text(), nullable=False),
        sa.Column('progress_percentage', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('resources_processed', sa.Integer(), nullable=True),
        sa.Column('cost_incurred', sa.Numeric(precision=10, scale=2), nullable=True, default=0),
        sa.Column('savings_identified', sa.Numeric(precision=12, scale=2), nullable=True, default=0),
        sa.Column('event_data', sa.Text(), nullable=True),
        sa.Column('visible_to_client', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['engagement_id'], ['client_engagements.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create invoices table
    op.create_table('invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('engagement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('tax_amount', sa.Numeric(precision=10, scale=2), nullable=True, default=0),
        sa.Column('discount_amount', sa.Numeric(precision=10, scale=2), nullable=True, default=0),
        sa.Column('status', sa.String(length=50), nullable=True, default='draft'),
        sa.Column('issue_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('paid_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('payment_method', sa.String(length=100), nullable=True),
        sa.Column('payment_reference', sa.String(length=255), nullable=True),
        sa.Column('pdf_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['engagement_id'], ['client_engagements.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invoice_number')
    )

    # Create pricing_rules table
    op.create_table('pricing_rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('condition_expression', sa.Text(), nullable=False),
        sa.Column('modifier_type', sa.String(length=50), nullable=False),
        sa.Column('modifier_value', sa.Numeric(precision=10, scale=4), nullable=False),
        sa.Column('applies_to_categories', sa.Text(), nullable=True),
        sa.Column('minimum_engagement_value', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('maximum_engagement_value', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('priority', sa.Integer(), nullable=True, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better performance
    op.create_index('ix_service_tokens_category', 'service_tokens', ['category'])
    op.create_index('ix_service_tokens_is_active', 'service_tokens', ['is_active'])
    op.create_index('ix_client_engagements_client_id', 'client_engagements', ['client_id'])
    op.create_index('ix_client_engagements_status', 'client_engagements', ['status'])
    op.create_index('ix_engagement_items_engagement_id', 'engagement_items', ['engagement_id'])
    op.create_index('ix_progress_events_engagement_id', 'progress_events', ['engagement_id'])
    op.create_index('ix_progress_events_created_at', 'progress_events', ['created_at'])
    op.create_index('ix_invoices_engagement_id', 'invoices', ['engagement_id'])
    op.create_index('ix_invoices_status', 'invoices', ['status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_invoices_status')
    op.drop_index('ix_invoices_engagement_id')
    op.drop_index('ix_progress_events_created_at')
    op.drop_index('ix_progress_events_engagement_id')
    op.drop_index('ix_engagement_items_engagement_id')
    op.drop_index('ix_client_engagements_status')
    op.drop_index('ix_client_engagements_client_id')
    op.drop_index('ix_service_tokens_is_active')
    op.drop_index('ix_service_tokens_category')

    # Drop tables
    op.drop_table('pricing_rules')
    op.drop_table('invoices')
    op.drop_table('progress_events')
    op.drop_table('engagement_items')
    op.drop_table('client_engagements')
    op.drop_table('service_tokens')

    # Drop enum types
    op.execute("DROP TYPE engagementstatus")
    op.execute("DROP TYPE servicecategory")
    op.execute("DROP TYPE unittype")
