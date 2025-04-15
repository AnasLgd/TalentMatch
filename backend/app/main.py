from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.api.v1 import consultants, companies, tenders, matches, collaborations, cv_analysis, n8n, rag, upload, users
from app.infrastructure.database.session import get_db
from app.infrastructure.database.session import get_db

app = FastAPI(
    title="TalentMatch API",
    description="API pour la plateforme TalentMatch - Solution SaaS pour ESN",
    version="0.1.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # URL spécifique du frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
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

# Création d'un routeur API avec préfixe commun
api_router = APIRouter(prefix="/api")

# Inclusion des routers API dans le routeur commun
api_router.include_router(consultants.router)
api_router.include_router(companies.router)
api_router.include_router(tenders.router)
api_router.include_router(matches.router)
api_router.include_router(collaborations.router)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cv_analysis.router)
api_router.include_router(n8n.router)
api_router.include_router(rag.router)
api_router.include_router(upload.router)

# Ajout du routeur API à l'application
app.include_router(api_router)
