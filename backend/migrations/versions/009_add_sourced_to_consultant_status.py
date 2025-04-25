"""Add SOURCED value to consultant status enum

Revision ID: 009_add_sourced_to_consultant_status
Revises: 008_add_consultant_status_enum
Create Date: 2025-04-23 23:43:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '009_add_sourced_to_consultant_status'
down_revision = '008_add_consultant_status_enum'
branch_labels = None
depends_on = None


def upgrade():
    # PostgreSQL permet d'ajouter facilement une valeur à un enum existant
    # Cela ne nécessite pas de recréer l'enum ou de reconvertir les données
    op.execute("ALTER TYPE public.consultantstatus ADD VALUE IF NOT EXISTS 'SOURCED'")


def downgrade():
    # PostgreSQL ne permet pas de supprimer directement une valeur d'un enum
    # Pour descendre, nous devrions recréer l'enum sans la valeur SOURCED,
    # mais cela pourrait être dangereux si des données utilisent cette valeur
    op.execute("""
    DO $$
    BEGIN
        RAISE NOTICE 'ATTENTION: La valeur SOURCED de consultantstatus ne peut pas être supprimée directement.';
        RAISE NOTICE 'Pour supprimer cette valeur, vous devrez créer un nouvel enum sans cette valeur et migrer les données.';
        RAISE NOTICE 'Les entrées utilisant SOURCED devront être converties manuellement vers un autre statut.';
    END $$;
    """)