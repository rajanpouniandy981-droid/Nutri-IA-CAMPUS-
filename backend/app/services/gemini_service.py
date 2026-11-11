import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Chargement robuste du .env
dossier_actuel = Path(__file__).resolve()
load_dotenv(dossier_actuel.parents[2] / ".env")
load_dotenv(dossier_actuel.parents[3] / ".env")
load_dotenv()

PROMPT_MASCOTTE = """
Tu es 'Nutri-Pote', la mascotte bienveillante, dynamique et complice des étudiants du CROUS sur les campus universitaires en France.
Regarde attentivement la photo de ce plateau repas étudiant.

Ton rôle :
1. Identifie le titre général du plat (ex: "Steak haché, Frites & Salade").
2. Liste les aliments reconnus sous forme d'une liste simple de textes.
3. Donne une estimation globale des calories (un simple nombre entier, ex: 650).
4. Donne un verdict rapide en 4-5 mots (ex: "Énergétique mais manque de fruits !").
5. ET SURTOUT : Rédige un message court (2-3 phrases max) pour la bulle de dialogue de la mascotte :
   - Parle directement à l'étudiant comme un pote de promo sympa et encourageant.
   - Ton : humoristique, bienveillant, zéro culpabilisation.
   - Donne un conseil concret pour son après-midi de cours (ex: prendre un fruit, boire de l'eau, ou féliciter un bon équilibre).

Réponds STRICTEMENT sous ce format JSON (aucun texte avant ou après) :
{
  "meal_title": "Titre du plateau",
  "mascot_message": "Message sympa de la mascotte...",
  "foods_detected": ["Aliment 1", "Aliment 2"],
  "estimated_calories": 650,
  "quick_verdict": "Verdict court"
}
"""

def get_best_available_model(api_key: str) -> str:
    """
    Interroge Google pour trouver le meilleur modèle Vision actif pour cette clé.
    """
    url_list = "https://generativelanguage.googleapis.com/v1beta/models"
    req = urllib.request.Request(url_list, headers={"x-goog-api-key": api_key})
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = data.get("models", [])
            # On cherche un modèle flash qui supporte generateContent
            for m in models:
                methods = m.get("supportedGenerationMethods", [])
                name = m.get("name", "")
                if "flash" in name.lower() and "generateContent" in methods:
                    return name  # ex: "models/gemini-2.0-flash" ou "models/gemini-1.5-flash-8b"
    except Exception:
        pass
    
    # Modèle par défaut standard
    return "models/gemini-2.0-flash"

async def analyze_tray_with_mascot(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    api_key = os.getenv("GEMINI_API_KEY", "")
    api_key = api_key.strip().strip('"').strip("'")

    if not api_key:
        raise ValueError("Clé GEMINI_API_KEY introuvable dans le fichier .env !")

    # 1. Détection du modèle disponible
    target_model = "models/gemini-3.8-flash"

    # 2. Préparation de l'image
    img_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # 3. Requête à Google
    url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT_MASCOTTE},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": img_b64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise ValueError(f"Erreur Google API ({e.code}) sur {target_model} : {err_body}")

    generated_text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(generated_text)