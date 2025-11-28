"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create audit_log table
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dispute_id', sa.String(length=255), nullable=False),
        sa.Column('node_name', sa.String(length=100), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('state_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('reasoning', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('supporting_evidence', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_log_dispute_id', 'audit_log', ['dispute_id'])
    op.create_index('idx_audit_log_timestamp', 'audit_log', ['timestamp'])
    op.create_index('idx_audit_log_node_name', 'audit_log', ['node_name'])

    # Create human_review_queue table
    op.create_table(
        'human_review_queue',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dispute_id', sa.String(length=255), nullable=False),
        sa.Column('confidence_score', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('decision', sa.String(length=50), nullable=False),
        sa.Column('reasoning', sa.Text(), nullable=False),
        sa.Column('supporting_rules', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending_review'),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('reviewed_by', sa.String(length=255), nullable=True),
        sa.Column('reviewed_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dispute_id')
    )
    op.create_index('idx_human_review_status', 'human_review_queue', ['status'])
    op.create_index('idx_human_review_created_at', 'human_review_queue', ['created_at'])

    # Create dispute_history table
    op.create_table(
        'dispute_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dispute_id', sa.String(length=255), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('final_decision', sa.String(length=50), nullable=True),
        sa.Column('confidence_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('actions_taken', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('completed_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dispute_id')
    )
    op.create_index('idx_dispute_history_dispute_id', 'dispute_history', ['dispute_id'])
    op.create_index('idx_dispute_history_status', 'dispute_history', ['status'])
    op.create_index('idx_dispute_history_created_at', 'dispute_history', ['created_at'])


def downgrade() -> None:
    op.drop_index('idx_dispute_history_created_at', table_name='dispute_history')
    op.drop_index('idx_dispute_history_status', table_name='dispute_history')
    op.drop_index('idx_dispute_history_dispute_id', table_name='dispute_history')
    op.drop_table('dispute_history')
    
    op.drop_index('idx_human_review_created_at', table_name='human_review_queue')
    op.drop_index('idx_human_review_status', table_name='human_review_queue')
    op.drop_table('human_review_queue')
    
    op.drop_index('idx_audit_log_node_name', table_name='audit_log')
    op.drop_index('idx_audit_log_timestamp', table_name='audit_log')
    op.drop_index('idx_audit_log_dispute_id', table_name='audit_log')
    op.drop_table('audit_log')
