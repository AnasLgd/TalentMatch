"""
Script de migration pour ajouter les tables et champs nécessaires à l'intégration avec n8n et les agents IA maison
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, ENUM
import enum

# revision identifiers, used by Alembic
revision = '002_n8n_ia_maison'
down_revision = '001_initial'
branch_labels = None
depends_on = None

# Définition des énumérations
class WorkflowStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentType(enum.Enum):
    CV = "cv"
    PORTFOLIO = "portfolio"
    TENDER = "tender"
    KNOWLEDGE_BASE = "knowledge_base"
    OTHER = "other"

def upgrade():
    # Créer les énumérations
    workflow_status_enum = sa.Enum(WorkflowStatus, name='workflow_status')
    workflow_status_enum.create(op.get_bind())
    
    document_type_enum = sa.Enum(DocumentType, name='document_type')
    document_type_enum.create(op.get_bind())
    
    # Ajouter des champs aux tables existantes
    op.add_column('resumes', sa.Column('analysis_result', JSONB, nullable=True))
    op.add_column('matches', sa.Column('match_details', JSONB, nullable=True))
    op.add_column('skill_portfolios', sa.Column('generation_details', JSONB, nullable=True))
    
    # Créer la table workflow_executions
    op.create_table(
        'workflow_executions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workflow_id', sa.String(length=255), nullable=False),
        sa.Column('workflow_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', name='workflow_status'), nullable=False),
        sa.Column('execution_id', sa.String(length=255), nullable=True),
        sa.Column('input_data', JSONB, nullable=True),
        sa.Column('output_data', JSONB, nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('resume_id', sa.Integer(), nullable=True),
        sa.Column('match_id', sa.Integer(), nullable=True),
        sa.Column('portfolio_id', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
        sa.ForeignKeyConstraint(['portfolio_id'], ['skill_portfolios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Créer la table rag_documents
    op.create_table(
        'rag_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.String(length=255), nullable=False),
        sa.Column('document_type', sa.Enum('CV', 'PORTFOLIO', 'TENDER', 'KNOWLEDGE_BASE', 'OTHER', name='document_type'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('metadata', JSONB, nullable=True),
        sa.Column('file_path', sa.String(length=255), nullable=True),
        sa.Column('chunk_count', sa.Integer(), nullable=False, default=0),
        sa.Column('indexed_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('document_id')
    )
    
    # Créer la table rag_queries
    op.create_table(
        'rag_queries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('filters', JSONB, nullable=True),
        sa.Column('result', JSONB, nullable=True),
        sa.Column('document_ids', JSONB, nullable=True),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['document_id'], ['rag_documents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Créer des index
    op.create_index(op.f('ix_workflow_executions_workflow_id'), 'workflow_executions', ['workflow_id'], unique=False)
    op.create_index(op.f('ix_workflow_executions_status'), 'workflow_executions', ['status'], unique=False)
    op.create_index(op.f('ix_rag_documents_document_type'), 'rag_documents', ['document_type'], unique=False)
    op.create_index(op.f('ix_rag_documents_document_id'), 'rag_documents', ['document_id'], unique=True)

def downgrade():
    # Supprimer les index
    op.drop_index(op.f('ix_rag_documents_document_id'), table_name='rag_documents')
    op.drop_index(op.f('ix_rag_documents_document_type'), table_name='rag_documents')
    op.drop_index(op.f('ix_workflow_executions_status'), table_name='workflow_executions')
    op.drop_index(op.f('ix_workflow_executions_workflow_id'), table_name='workflow_executions')
    
    # Supprimer les tables
    op.drop_table('rag_queries')
    op.drop_table('rag_documents')
    op.drop_table('workflow_executions')
    
    # Supprimer les colonnes ajoutées
    op.drop_column('skill_portfolios', 'generation_details')
    op.drop_column('matches', 'match_details')
    op.drop_column('resumes', 'analysis_result')
    
    # Supprimer les énumérations
    sa.Enum(name='document_type').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='workflow_status').drop(op.get_bind(), checkfirst=False)
