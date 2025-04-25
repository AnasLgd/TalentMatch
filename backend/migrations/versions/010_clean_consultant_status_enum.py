"""Clean consultant status enum

Revision ID: 010_clean_consultant_status_enum
Revises: 009_add_sourced_to_consultant_status
Create Date: 2025-04-24

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '010_clean_consultant_status_enum'
down_revision = '009_add_sourced_to_consultant_status'
branch_labels = None
depends_on = None

def upgrade():
    # Commentaire explicatif
    op.execute("""
    -- Cette migration nettoie l'énumération consultant_status pour ne conserver que 5 valeurs :
    -- SOURCED, QUALIFIED, MISSION, INTERCO, ARCHIVED
    -- Les autres valeurs sont supprimées et converties selon le mapping suivant :
    -- PROCESS -> SOURCED
    -- AVAILABLE, PARTIALLY_AVAILABLE, UNAVAILABLE -> QUALIFIED 
    -- ON_MISSION -> MISSION
    -- LEAVING -> ARCHIVED
    """)
    
    # 1. Créer le nouvel enum avec uniquement les 5 statuts validés
    op.execute("ALTER TYPE public.consultantstatus RENAME TO consultantstatus_old")
    op.execute("CREATE TYPE public.consultantstatus AS ENUM ('SOURCED', 'QUALIFIED', 'MISSION', 'INTERCO', 'ARCHIVED')")
    
    # 2. Mettre à jour les valeurs existantes
    op.execute("""
    ALTER TABLE consultants
    ALTER COLUMN status TYPE public.consultantstatus USING
    CASE
        WHEN status::text = 'PROCESS'::text THEN 'SOURCED'::public.consultantstatus
        WHEN status::text = 'AVAILABLE'::text THEN 'QUALIFIED'::public.consultantstatus
        WHEN status::text = 'PARTIALLY_AVAILABLE'::text THEN 'QUALIFIED'::public.consultantstatus
        WHEN status::text = 'UNAVAILABLE'::text THEN 'QUALIFIED'::public.consultantstatus
        WHEN status::text = 'ON_MISSION'::text THEN 'MISSION'::public.consultantstatus
        WHEN status::text = 'LEAVING'::text THEN 'ARCHIVED'::public.consultantstatus
        WHEN status::text = 'INTERCONTRACT'::text THEN 'INTERCO'::public.consultantstatus
        ELSE status::text::public.consultantstatus
    END
    """)
    
    # 3. Supprimer l'ancien enum
    op.execute("DROP TYPE public.consultantstatus_old")

def downgrade():
    # Cette opération n'est pas réversible de manière sécurisée une fois déployée
    op.execute("""
    DO $$
    BEGIN
        RAISE NOTICE 'ATTENTION: Cette migration ne peut pas être annulée automatiquement.';
        RAISE NOTICE 'Pour revenir en arrière, vous devriez créer une nouvelle migration qui restaure les anciens statuts.';
        RAISE NOTICE 'Les données ont déjà été converties vers les nouveaux statuts.';
    END $$;
    """)