from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.models.schemas import ScanResponse
from backend.app.services.gemini_service import analyze_tray_with_mascot

router = APIRouter()

@router.post("/scan", response_model=ScanResponse)
async def scan_meal(image: UploadFile = File(...)):
    """
    Reçoit la photo du plateau CROUS, l'envoie à Gemini
    et renvoie la réponse vivante de la mascotte !
    """
    # 1. Vérification du type de fichier
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="Le fichier envoyé doit être une image (JPEG, PNG, WebP)."
        )

    # 2. Lecture des données brutes de l'image
    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="L'image reçue est vide.")

    # 3. Appel de notre expert Gemini
    try:
        result = await analyze_tray_with_mascot(
            image_bytes=image_bytes, 
            mime_type=image.content_type
        )
        return ScanResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de l'analyse avec Gemini : {str(e)}"
        )