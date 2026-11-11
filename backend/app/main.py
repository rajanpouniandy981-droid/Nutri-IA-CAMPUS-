from fastapi import FastAPI  ## sert à importer fast api qui est nous permettera de recuperer les requetes via Uvicorn 

# On initialise notre application web
app =  FastAPI(title="Nutr'IA Campus API")

# On définit notre toute première route vers requête (l'accueil)
@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de Nutr'IA Campus !"}