"""Add WorkflowStatus enum

Revision ID: 004_add_workflow_status_enum
Revises: 003_convert_tender_skills
Create Date: 2025-04-02

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004_add_workflow_status_enum'
down_revision = '003_convert_tender_skills'
branch_labels = None
depends_on = None

# Création de l'enum temporairement
workflow_status_enum = postgresql.ENUM('running', 'success', 'error', 'cancelled', name='workflowstatus')

def upgrade():
    # Vérifier si l'enum existe déjà pour éviter l'erreur "déjà existe"
    connection = op.get_bind()
    
    # Méthode plus sûre pour vérifier si l'enum existe
    has_enum = False
    try:
        # Vérifier si l'enum existe dans pg_type
        result = connection.execute(sa.text(
            "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'workflowstatus')"
        ))
        has_enum = result.scalar()
    except Exception:
        pass
    
    # Créer l'enum s'il n'existe pas
    if not has_enum:
        workflow_status_enum.create(connection)
    
    # Vérifier si les tables existent déjà
    wf_exists = False
    wf_old_exists = False
    
    try:
        result = connection.execute(sa.text(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'workflow_executions')"
        ))
        wf_exists = result.scalar()
        
        result = connection.execute(sa.text(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'workflow_executions_old')"
        ))
        wf_old_exists = result.scalar()
    except Exception as e:
        print(f"Error checking tables: {e}")
        pass
    
    # Si la migration est déjà partiellement appliquée, on la nettoie
    if wf_old_exists and wf_exists:
        print("Cleaning up previous partial migration...")
        try:
            op.drop_table('workflow_executions')
        except Exception as e:
            print(f"Error dropping workflow_executions: {e}")
    
    # Si la table principale existe, on la renomme
    if wf_exists and not wf_old_exists:
        try:
            op.execute('ALTER TABLE workflow_executions RENAME TO workflow_executions_old')
            wf_old_exists = True
            wf_exists = False
        except Exception as e:
            print(f"Error renaming table: {e}")
    
    # Créer la nouvelle table seulement si elle n'existe pas déjà
    if not wf_exists:
        print("Creating workflow_executions table...")
        try:
            op.create_table('workflow_executions',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('workflow_id', sa.String(length=255), nullable=False),
                sa.Column('execution_id', sa.String(length=255), nullable=False),
                sa.Column('status', postgresql.ENUM('running', 'success', 'error', 'cancelled', name='workflowstatus', create_type=False), nullable=False),
                sa.Column('data', sa.JSON(), nullable=True),
                sa.Column('resume_id', sa.Integer(), nullable=True),
                sa.Column('match_id', sa.Integer(), nullable=True),
                sa.Column('portfolio_id', sa.Integer(), nullable=True),
                sa.Column('error_message', sa.Text(), nullable=True),
                sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
                sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
                sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ),
                sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
                sa.PrimaryKeyConstraint('id')
            )
        except Exception as e:
            print(f"Error creating table: {e}")
            # Check if table was created despite the error
            result = connection.execute(sa.text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'workflow_executions')"
            ))
            if not result.scalar():
                raise e
    
    # Check if index exists before creating it
    index_exists = False
    try:
        result = connection.execute(sa.text(
            "SELECT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_workflow_executions_id')"
        ))
        index_exists = result.scalar()
    except Exception:
        pass
    
    if not index_exists:
        op.create_index(op.f('ix_workflow_executions_id'), 'workflow_executions', ['id'], unique=False)
    
    # Vérifier si la table old existe et contient des données
    has_data = False
    if wf_old_exists:
        try:
            result = connection.execute(sa.text("SELECT COUNT(*) FROM workflow_executions_old"))
            count = result.scalar()
            has_data = count > 0
            print(f"workflow_executions_old has {count} rows.")
        except Exception as e:
            print(f"Error checking data count: {e}")
    
    # Copier les données seulement si la table existe et a des données
    if wf_old_exists and has_data:
        try:
            print("Copying data from workflow_executions_old to workflow_executions...")
            op.execute("""
                INSERT INTO workflow_executions (
                    id, workflow_id, execution_id, status, data, resume_id, match_id, portfolio_id,
                    error_message, started_at, finished_at, created_at, updated_at
                )
                SELECT
                    id, workflow_id, execution_id,
                    CASE
                        WHEN status = 'running' THEN 'running'::workflowstatus
                        WHEN status = 'success' THEN 'success'::workflowstatus
                        WHEN status = 'error' THEN 'error'::workflowstatus
                        ELSE 'cancelled'::workflowstatus
                    END,
                    data, resume_id, match_id, portfolio_id,
                    error_message, started_at, finished_at, created_at, updated_at
                FROM workflow_executions_old
            """)
            print("Data copied successfully.")
        except Exception as e:
            print(f"Error copying data: {e}")
        
        # Supprimer l'ancienne table seulement si elle existe
        try:
            print("Dropping workflow_executions_old table...")
            op.drop_table('workflow_executions_old')
            print("Old table dropped successfully.")
        except Exception as e:
            print(f"Error dropping old table: {e}")

def downgrade():
    connection = op.get_bind()
    
    # Vérifier si la table workflow_executions existe
    exists = False
    try:
        result = connection.execute(sa.text(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'workflow_executions')"
        ))
        exists = result.scalar()
    except Exception:
        pass
    
    # Si la table existe, procéder à la migration inverse
    if exists:
        # Créer une table temporaire pour la migration inverse
        op.execute('ALTER TABLE workflow_executions RENAME TO workflow_executions_new')
        
        # Recréer l'ancienne table avec string pour le statut
        op.create_table('workflow_executions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('workflow_id', sa.String(length=255), nullable=False),
            sa.Column('execution_id', sa.String(length=255), nullable=False),
            sa.Column('status', sa.String(length=50), nullable=False),
            sa.Column('data', sa.JSON(), nullable=True),
            sa.Column('resume_id', sa.Integer(), nullable=True),
            sa.Column('match_id', sa.Integer(), nullable=True),
            sa.Column('portfolio_id', sa.Integer(), nullable=True),
            sa.Column('error_message', sa.Text(), nullable=True),
            sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
            sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ),
            sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_workflow_executions_id'), 'workflow_executions', ['id'], unique=False)
        
        # Vérifier si la table temporaire a des données
        has_data = False
        try:
            result = connection.execute(sa.text("SELECT COUNT(*) FROM workflow_executions_new"))
            count = result.scalar()
            has_data = count > 0
        except Exception:
            pass
        
        # Copier les données si la table temporaire a des données
        if has_data:
            op.execute("""
                INSERT INTO workflow_executions (
                    id, workflow_id, execution_id, status, data, resume_id, match_id, portfolio_id,
                    error_message, started_at, finished_at, created_at, updated_at
                )
                SELECT
                    id, workflow_id, execution_id, status::text, data, resume_id, match_id, portfolio_id,
                    error_message, started_at, finished_at, created_at, updated_at
                FROM workflow_executions_new
            """)
        
        # Supprimer la nouvelle table
        op.drop_table('workflow_executions_new')
    
    # Vérifier si l'enum existe avant d'essayer de le supprimer
    has_enum = False
    try:
        result = connection.execute(sa.text(
            "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'workflowstatus')"
        ))
        has_enum = result.scalar()
    except Exception:
        pass
    
    # Supprimer l'enum s'il existe
    if has_enum:
        workflow_status_enum.drop(connection)
