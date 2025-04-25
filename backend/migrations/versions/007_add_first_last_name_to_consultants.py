"""Add first_name and last_name to consultants

Revision ID: 007_add_first_last_name_to_consultants
Revises: 006_make_consultant_user_id_nullable
Create Date: 2025-04-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '007_add_first_last_name_to_consultants'
down_revision = '006_make_consultant_user_id_nullable'  # Corrigé: utiliser uniquement l'ID de révision, pas le nom du fichier
branch_labels = None
depends_on = None

def upgrade():
    # Ajout des colonnes first_name et last_name à la table consultants
    op.add_column('consultants', sa.Column('first_name', sa.String(255), nullable=True))
    op.add_column('consultants', sa.Column('last_name', sa.String(255), nullable=True))
    
    # Note: Nous ne pouvons pas initialiser les données depuis les utilisateurs car
    # la structure est différente (users utilise full_name au lieu de first_name/last_name)

def downgrade():
    # Suppression des colonnes ajoutées
    op.drop_column('consultants', 'first_name')
    op.drop_column('consultants', 'last_name')