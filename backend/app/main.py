from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.scan import router as scan_router

app = FastAPI(
    title="Nutr'IA Campus API",
    description="API Backend pour l'analyse des plateaux CROUS avec mascotte IA",
    version="1.0.0"
)

# Configuration CORS pour autoriser le frontend d'Arthur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En développement, on autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# On enregistre notre routeur avec le préfixe /api
app.include_router(scan_router, prefix="/api", tags=["Analyse Plateau"])

@app.get("/")
def home():
    return {
        "message": "Bienvenue sur l'API de Nutr'IA Campus ! 🌱",
        "documentation": "Rendez-vous sur /docs pour tester l'analyse d'image."
    }