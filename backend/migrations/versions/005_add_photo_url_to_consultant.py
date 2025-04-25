"""add photo_url to consultant

Revision ID: 005_add_photo_url_to_consultant
Revises: 004_add_workflow_status_enum
Create Date: 2025-04-14

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '005_add_photo_url_to_consultant'
down_revision = '004_add_workflow_status_enum'
branch_labels = None
depends_on = None

def upgrade():
    # Ajout de la colonne photo_url à la table consultants
    op.add_column('consultants', sa.Column('photo_url', sa.String(255), nullable=True))

def downgrade():
    # Suppression de la colonne photo_url de la table consultants
    op.drop_column('consultants', 'photo_url')