"""
Script de migration initial pour créer les tables de base de données TalentMatch
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Table des utilisateurs
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Table des entreprises (ESN)
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('postal_code', sa.String(length=20), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('logo_url', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Table des consultants
    op.create_table(
        'consultants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('experience_years', sa.Integer(), nullable=True),
        sa.Column('daily_rate', sa.Float(), nullable=True),
        sa.Column('availability_status', sa.String(length=50), nullable=True),
        sa.Column('availability_date', sa.Date(), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('remote_work', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Table des compétences
    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Table d'association consultant-compétence
    op.create_table(
        'consultant_skills',
        sa.Column('consultant_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('years_experience', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['consultant_id'], ['consultants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('consultant_id', 'skill_id')
    )
    
    # Table des CV
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('consultant_id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('extracted_data', JSONB, nullable=True),
        sa.Column('is_current', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['consultant_id'], ['consultants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Table des appels d'offres
    op.create_table(
        'tenders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('client_name', sa.String(length=255), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('remote_work', sa.Boolean(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('duration_months', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Table d'association appel d'offres-compétence
    op.create_table(
        'tender_skills',
        sa.Column('tender_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=False, default=True),
        sa.Column('weight', sa.Float(), nullable=False, default=1.0),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['tender_id'], ['tenders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('tender_id', 'skill_id')
    )
    
    # Table des correspondances (matches)
    op.create_table(
        'matches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tender_id', sa.Integer(), nullable=False),
        sa.Column('consultant_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('details', JSONB, nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['consultant_id'], ['consultants.id'], ),
        sa.ForeignKeyConstraint(['tender_id'], ['tenders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tender_id', 'consultant_id')
    )
    
    # Table des dossiers de compétences
    op.create_table(
        'skill_portfolios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('consultant_id', sa.Integer(), nullable=False),
        sa.Column('tender_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['consultant_id'], ['consultants.id'], ),
        sa.ForeignKeyConstraint(['tender_id'], ['tenders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Table des collaborations inter-ESN
    op.create_table(
        'collaborations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('requester_company_id', sa.Integer(), nullable=False),
        sa.Column('provider_company_id', sa.Integer(), nullable=False),
        sa.Column('tender_id', sa.Integer(), nullable=False),
        sa.Column('consultant_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('terms', JSONB, nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['consultant_id'], ['consultants.id'], ),
        sa.ForeignKeyConstraint(['provider_company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['requester_company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['tender_id'], ['tenders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('collaborations')
    op.drop_table('skill_portfolios')
    op.drop_table('matches')
    op.drop_table('tender_skills')
    op.drop_table('tenders')
    op.drop_table('resumes')
    op.drop_table('consultant_skills')
    op.drop_table('skills')
    op.drop_table('consultants')
    op.drop_table('companies')
    op.drop_table('users')
