"""Make consultant user_id nullable

Revision ID: 006
Revises: 005_add_photo_url_to_consultant
Create Date: 2025-04-15 11:25:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'  # Correction: le format de la révision précédente est juste le numéro
branch_labels = None
depends_on = None


def upgrade():
    # Rendre la colonne user_id nullable
    op.alter_column('consultants', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade():
    # Remettre la colonne user_id non nullable
    op.alter_column('consultants', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)