from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.v1 import consultants, companies, tenders, matches, collaborations, cv_analysis, n8n, rag
from app.infrastructure.database.session import get_db

app = FastAPI(
    title="TalentMatch API",
    description="API pour la plateforme TalentMatch - Solution SaaS pour ESN",
    version="0.1.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À remplacer par les domaines autorisés en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route principale
@app.get("/")
async def root():
    return {
        "title": "TalentMatch API",
        "version": "0.1.0",
        "description": "Plateforme SaaS pour ESN - Gestion des talents et des appels d'offres"
    }

# Vérification de la santé de l'API
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Vérifier la connexion à la base de données
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service indisponible: {str(e)}")

# Inclusion des routers API
app.include_router(consultants.router)
app.include_router(companies.router)
app.include_router(tenders.router)
app.include_router(matches.router)
app.include_router(collaborations.router)
app.include_router(cv_analysis.router)
app.include_router(n8n.router)
app.include_router(rag.router)
