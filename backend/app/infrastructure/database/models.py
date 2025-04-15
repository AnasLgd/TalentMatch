from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, Enum, JSON, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum
from datetime import datetime
from typing import List, Optional

# Base declarative pour tous les modèles
Base = declarative_base()

# Enumération pour le niveau de compétence
class ProficiencyLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

# Remplace la table d'association simple par un modèle complet pour les skills des consultants
class ConsultantSkill(Base):
    __tablename__ = "consultant_skills"
    
    consultant_id = Column(Integer, ForeignKey('consultants.id'), primary_key=True)
    skill_id = Column(Integer, ForeignKey('skills.id'), primary_key=True)
    proficiency_level = Column(Enum(ProficiencyLevel), default=ProficiencyLevel.INTERMEDIATE)
    years_experience = Column(Integer, default=0)
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    consultant = relationship("Consultant", back_populates="consultant_skills")
    skill = relationship("Skill", back_populates="consultant_skills")

# Remplace la table d'association simple par un modèle complet pour les skills des appels d'offres
class TenderSkill(Base):
    __tablename__ = "tender_skills"
    
    # Id unique géré automatiquement
    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey('tenders.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    importance = Column(String(50), default="required")  # "required", "preferred", "nice_to_have"
    details = Column(Text)                                # Détails supplémentaires sur la compétence requise
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Création d'un index unique pour éviter les doublons
    __table_args__ = (UniqueConstraint('tender_id', 'skill_id', name='uix_tender_skill'),)
    
    tender = relationship("Tender", back_populates="tender_skills")
    skill = relationship("Skill", back_populates="tender_skills")

# Table d'association pour la relation many-to-many entre consultants et portfolios
consultant_portfolios = Table(
    'consultant_portfolios',
    Base.metadata,
    Column('consultant_id', Integer, ForeignKey('consultants.id'), primary_key=True),
    Column('portfolio_id', Integer, ForeignKey('portfolios.id'), primary_key=True)
)

# Énumération des statuts possibles pour un Consultant
class ConsultantStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    MISSION = "ON_MISSION"
    UNAVAILABLE = "UNAVAILABLE"
    LEAVING = "LEAVING"

# Énumération des statuts possibles pour un Appel d'Offres
class TenderStatus(enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    CANCELLED = "cancelled"

# Énumération des statuts possibles pour un Match
class MatchStatus(enum.Enum):
    PENDING = "pending"
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

# Énumération des statuts possibles pour une Collaboration
class CollaborationStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Énumération des rôles d'utilisateur
class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CONSULTANT = "consultant"
    CLIENT = "client"

# Énumération des types de document pour RAG
class DocumentType(enum.Enum):
    CV = "cv"
    TENDER = "tender"
    SKILL = "skill"
    PORTFOLIO = "portfolio"

# Énumération des statuts possibles pour un Workflow
class WorkflowStatus(enum.Enum):
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    company = relationship("Company", back_populates="users")
    consultant = relationship("Consultant", back_populates="user", uselist=False)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    website = Column(String(255))
    address = Column(String(255))
    logo_url = Column(String(255))
    is_esn = Column(Boolean, default=False)  # Indique si c'est une ESN ou un client
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    users = relationship("User", back_populates="company")
    consultants = relationship("Consultant", back_populates="company")
    tenders = relationship("Tender", back_populates="company")
    portfolios = relationship("Portfolio", back_populates="company")

class Consultant(Base):
    __tablename__ = "consultants"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String(255))
    bio = Column(Text)
    years_experience = Column(Integer, default=0)
    hourly_rate = Column(Float)
    daily_rate = Column(Float)
    availability_date = Column(DateTime(timezone=True))
    status = Column(Enum(ConsultantStatus), default=ConsultantStatus.AVAILABLE)
    cv_url = Column(String(255))
    linkedin_url = Column(String(255))
    github_url = Column(String(255))
    photo_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="consultant")
    company = relationship("Company", back_populates="consultants")
    skills = relationship("Skill", secondary="consultant_skills", back_populates="consultants")
    consultant_skills = relationship("ConsultantSkill", back_populates="consultant")
    portfolios = relationship("Portfolio", secondary=consultant_portfolios, back_populates="consultants")
    matches = relationship("Match", back_populates="consultant")
    collaborations = relationship("Collaboration", back_populates="consultant")
    resumes = relationship("Resume", back_populates="consultant")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))  # ex: "programming", "language", "soft skill"
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    consultants = relationship("Consultant", secondary="consultant_skills", back_populates="skills")
    tenders = relationship("Tender", secondary="tender_skills", back_populates="skills")
    consultant_skills = relationship("ConsultantSkill", back_populates="skill")
    tender_skills = relationship("TenderSkill", back_populates="skill")

class Tender(Base):
    __tablename__ = "tenders"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    location = Column(String(255))
    remote_allowed = Column(Boolean, default=False)
    status = Column(Enum(TenderStatus), default=TenderStatus.DRAFT)
    budget_min = Column(Float)
    budget_max = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    company = relationship("Company", back_populates="tenders")
    skills = relationship("Skill", secondary="tender_skills", back_populates="tenders")
    matches = relationship("Match", back_populates="tender")
    collaborations = relationship("Collaboration", back_populates="tender")
    tender_skills = relationship("TenderSkill", back_populates="tender")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    score = Column(Float, default=0.0)  # Score du match (0-100)
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    consultant = relationship("Consultant", back_populates="matches")
    tender = relationship("Tender", back_populates="matches")
    workflow_executions = relationship("WorkflowExecution", back_populates="match")
    collaboration = relationship("Collaboration", back_populates="match", uselist=False)

class Collaboration(Base):
    __tablename__ = "collaborations"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), unique=True, nullable=False)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    hourly_rate = Column(Float)
    daily_rate = Column(Float)
    status = Column(Enum(CollaborationStatus), default=CollaborationStatus.DRAFT)
    contract_url = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    match = relationship("Match", back_populates="collaboration")
    consultant = relationship("Consultant", back_populates="collaborations")
    tender = relationship("Tender", back_populates="collaborations")

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    image_url = Column(String(255))
    project_url = Column(String(255))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    company = relationship("Company", back_populates="portfolios")
    consultants = relationship("Consultant", secondary=consultant_portfolios, back_populates="portfolios")
    workflow_executions = relationship("WorkflowExecution", back_populates="portfolio")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)  # Chemin vers le fichier dans MinIO/S3
    file_type = Column(String(50))  # ex: "pdf", "docx"
    file_size = Column(Integer)  # taille en bytes
    parsed_data = Column(JSON)  # Données extraites du CV
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    consultant = relationship("Consultant", back_populates="resumes")
    workflow_executions = relationship("WorkflowExecution", back_populates="resume")

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String(255), nullable=False)  # ID du workflow dans n8n
    execution_id = Column(String(255), nullable=False)  # ID de l'exécution dans n8n
    status = Column(Enum(WorkflowStatus), nullable=False, default=WorkflowStatus.RUNNING)  # Statut de l'exécution
    data = Column(JSON)  # Données d'entrée et de sortie
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=True)
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    resume = relationship("Resume", back_populates="workflow_executions")
    match = relationship("Match", back_populates="workflow_executions")
    portfolio = relationship("Portfolio", back_populates="workflow_executions")

class RAGDocument(Base):
    __tablename__ = "rag_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(255), unique=True, nullable=False)  # UUID du document
    document_type = Column(Enum(DocumentType), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)  # Contenu textuel du document
    document_metadata = Column(JSON)  # Métadonnées du document (renommé pour éviter le conflit)
    file_path = Column(String(255))  # Chemin du fichier original
    chunk_count = Column(Integer, default=0)  # Nombre de chunks créés
    indexed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    chunks = relationship("RAGChunk", back_populates="document")
    queries = relationship("RAGQuery", back_populates="documents", secondary="rag_query_documents")

class RAGChunk(Base):
    __tablename__ = "rag_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(255), unique=True, nullable=False)  # UUID du chunk
    document_id = Column(Integer, ForeignKey("rag_documents.id"), nullable=False)
    content = Column(Text, nullable=False)  # Contenu du chunk
    embedding = Column(Text)  # Représentation vectorielle stockée sous forme de texte
    chunk_index = Column(Integer)  # Position du chunk dans le document
    token_count = Column(Integer)  # Nombre de tokens dans le chunk
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    document = relationship("RAGDocument", back_populates="chunks")

class RAGQuery(Base):
    __tablename__ = "rag_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text, nullable=False)  # Texte de la requête
    embedding = Column(Text)  # Représentation vectorielle de la requête
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    generated_response = Column(Text)  # Réponse générée
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    documents = relationship("RAGDocument", back_populates="queries", secondary="rag_query_documents")

# Table d'association pour la relation many-to-many entre queries et documents
rag_query_documents = Table(
    'rag_query_documents',
    Base.metadata,
    Column('query_id', Integer, ForeignKey('rag_queries.id'), primary_key=True),
    Column('document_id', Integer, ForeignKey('rag_documents.id'), primary_key=True),
    Column('relevance_score', Float),  # Score de pertinence
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)
