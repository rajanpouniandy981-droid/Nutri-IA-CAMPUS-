from pydantic import BaseModel
from typing import List, Optional

class ScanResponse(BaseModel):
    success: bool = True
    meal_title: str                  # Ex: "Plateau Steak Frites & Pomme"
    mascot_message: str              # La bulle de dialogue sympa de la mascotte
    foods_detected: List[str]        # Liste simple : ["Steak haché", "Frites", "Pomme"]
    estimated_calories: Optional[int] = None  # Ex: 650
    quick_verdict: str               # Ex: "Énergétique mais manque de verdure !"