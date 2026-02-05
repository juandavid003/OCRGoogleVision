import difflib
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
from app.matcher import normalize

load_dotenv()

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

cred = credentials.Certificate(FIREBASE_CREDENTIALS)
SIMILARITY_THRESHOLD = 0.85  # 85% de parecido

firebase_admin.initialize_app(cred, {
    "projectId": FIREBASE_PROJECT_ID
})

db = firestore.client()


def get_ocr_map():
    docs = db.collection("ocr_map").stream()
    products = []
    for doc in docs:
        products.append(doc.to_dict())
    return products


def save_ocr_history(raw_text: str, detected_products: list, child_id: str):
    if not detected_products:
        return

    if is_duplicate_invoice(raw_text):
        print("Factura duplicada detectada, no se guarda")
        return

    db.collection("ocr_history").add({
        "raw_text": raw_text,
        "detected_products": detected_products,
        "childId": child_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    print("Factura guardada correctamente")


def is_duplicate_invoice(raw_text: str) -> bool:
    """Retorna True si la factura ya existe según texto similar."""
    normalized_text = normalize(raw_text)

    # Traer facturas recientes
    docs = db.collection("ocr_history").stream()
    for doc in docs:
        existing_text = normalize(doc.to_dict().get("raw_text", ""))
        similarity = difflib.SequenceMatcher(None, normalized_text, existing_text).ratio()
        if similarity >= SIMILARITY_THRESHOLD:
            return True
    return False