"""Add consultant status enum

Revision ID: 008_add_consultant_status_enum
Revises: 007_add_first_last_name_to_consultants
Create Date: 2025-04-22 11:28:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '008_add_consultant_status_enum'
down_revision = '007_add_first_last_name_to_consultants'
branch_labels = None
depends_on = None


def upgrade():
    # Créer une nouvelle énumération temporaire avec les nouveaux statuts
    op.execute("ALTER TYPE public.consultantstatus RENAME TO consultantstatus_old")
    op.execute("CREATE TYPE public.consultantstatus AS ENUM ('PROCESS', 'QUALIFIED', 'MISSION', 'INTERCO', 'AVAILABLE', 'PARTIALLY_AVAILABLE', 'UNAVAILABLE', 'ON_MISSION', 'LEAVING')")
    
    # Convertir les statuts existants vers les nouveaux
    op.execute("""
    ALTER TABLE consultants
    ALTER COLUMN status TYPE public.consultantstatus USING
    CASE
        WHEN status::text = 'AVAILABLE'::text THEN 'QUALIFIED'::public.consultantstatus
        WHEN status::text = 'PARTIALLY_AVAILABLE'::text THEN 'QUALIFIED'::public.consultantstatus
        WHEN status::text = 'UNAVAILABLE'::text THEN 'QUALIFIED'::public.consultantstatus
        WHEN status::text = 'ON_MISSION'::text THEN 'MISSION'::public.consultantstatus
        WHEN status::text = 'LEAVING'::text THEN 'QUALIFIED'::public.consultantstatus
        ELSE 'PROCESS'::public.consultantstatus
    END
    """)
    
    # Supprimer l'ancienne énumération
    op.execute("DROP TYPE public.consultantstatus_old")


def downgrade():
    # Récrée l'ancienne énumération
    op.execute("ALTER TYPE public.consultantstatus RENAME TO consultantstatus_new")
    op.execute("CREATE TYPE public.consultantstatus AS ENUM ('AVAILABLE', 'MISSION', 'UNAVAILABLE', 'LEAVING')")
    
    # Convertir les nouveaux statuts vers les anciens
    op.execute("""
    ALTER TABLE consultants
    ALTER COLUMN status TYPE public.consultantstatus USING
    CASE
        WHEN status::text = 'PROCESS'::text THEN 'AVAILABLE'::public.consultantstatus
        WHEN status::text = 'QUALIFIED'::text THEN 'AVAILABLE'::public.consultantstatus
        WHEN status::text = 'MISSION'::text THEN 'MISSION'::public.consultantstatus
        WHEN status::text = 'INTERCO'::text THEN 'AVAILABLE'::public.consultantstatus
        ELSE 'AVAILABLE'::public.consultantstatus
    END
    """)
    
    # Supprimer la nouvelle énumération
    op.execute("DROP TYPE public.consultantstatus_new")