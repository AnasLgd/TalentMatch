"""Convert tender_skills to model

Revision ID: 003_convert_tender_skills
Revises: 002_n8n_ia_maison
Create Date: 2025-04-02

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_convert_tender_skills'
down_revision = '002_n8n_ia_maison'
branch_labels = None
depends_on = None


def upgrade():
    # Renommer la table existante pour sauvegarder les données
    op.rename_table('tender_skills', 'tender_skills_old')

    # Créer la nouvelle table avec structure mise à jour
    op.create_table('tender_skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tender_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('importance', sa.String(length=50), nullable=True, default="required"),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ),
        sa.ForeignKeyConstraint(['tender_id'], ['tenders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tender_id', 'skill_id', name='uix_tender_skill')
    )
    op.create_index(op.f('ix_tender_skills_id'), 'tender_skills', ['id'], unique=False)
    
    # Migration des données
    op.execute("""
        INSERT INTO tender_skills (tender_id, skill_id, importance, details)
        SELECT tender_id, skill_id, 
            CASE 
                WHEN is_required THEN 'required' 
                ELSE 'preferred' 
            END, 
            NULL
        FROM tender_skills_old
    """)
    
    # Suppression de l'ancienne table
    op.drop_table('tender_skills_old')


def downgrade():
    # Renommer la table existante pour sauvegarder les données
    op.rename_table('tender_skills', 'tender_skills_new')
    
    # Recréer l'ancienne structure
    op.create_table('tender_skills',
        sa.Column('tender_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=True, default=True),
        sa.Column('minimum_years', sa.Integer(), nullable=True, default=0),
        sa.Column('importance', sa.Float(), nullable=True, default=1.0),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ),
        sa.ForeignKeyConstraint(['tender_id'], ['tenders.id'], ),
        sa.PrimaryKeyConstraint('tender_id', 'skill_id')
    )
    
    # Migration des données vers l'ancienne structure
    op.execute("""
        INSERT INTO tender_skills (tender_id, skill_id, is_required)
        SELECT tender_id, skill_id, 
            CASE 
                WHEN importance = 'required' THEN true 
                ELSE false 
            END
        FROM tender_skills_new
    """)
    
    # Suppression de la nouvelle table
    op.drop_table('tender_skills_new')
