import re
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

firebase_admin.initialize_app(cred, {
    "projectId": FIREBASE_PROJECT_ID
})

db = firestore.client()

SIMILARITY_THRESHOLD = 0.85  # fallback


# =========================
# 🔍 EXTRAER DATOS FACTURA
# =========================
def extract_invoice_data(raw_text: str):
    text = normalize(raw_text)

    # NRO factura (ej: 001-001-000123456 o números largos)
    nro_match = re.search(r'(\d{3}-\d{3}-\d{6,9}|\d{6,12})', text)
    nro = nro_match.group(0) if nro_match else None

    # Fecha (dd/mm/yyyy o dd-mm-yyyy)
    date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{2,4})', text)
    date = date_match.group(0) if date_match else None

    # Dirección (líneas comunes)
    direccion_match = re.search(r'(dir|direccion|av|calle)[^\n]*', text)
    direccion = direccion_match.group(0) if direccion_match else None

    return {
        "nro": nro,
        "date": date,
        "direccion": direccion
    }


# =========================
# 🚫 VALIDAR DUPLICADO
# =========================
def is_duplicate_invoice(raw_text: str) -> bool:
    data = extract_invoice_data(raw_text)

    # 1. Validación principal por NRO
    if data["nro"]:
        query = db.collection("ocr_history") \
                  .where("nro", "==", data["nro"]) \
                  .limit(1) \
                  .stream()

        for _ in query:
            return True

    # 2. Validación secundaria (NRO + Fecha)
    if data["nro"] and data["date"]:
        query = db.collection("ocr_history") \
                  .where("nro", "==", data["nro"]) \
                  .where("date", "==", data["date"]) \
                  .limit(1) \
                  .stream()

        for _ in query:
            return True

    # 3. Fallback (similaridad de texto)
    normalized_text = normalize(raw_text)
    docs = db.collection("ocr_history").stream()

    for doc in docs:
        existing_text = normalize(doc.to_dict().get("raw_text", ""))
        similarity = difflib.SequenceMatcher(None, normalized_text, existing_text).ratio()

        if similarity >= SIMILARITY_THRESHOLD:
            return True

    return False


# =========================
# 💾 GUARDAR HISTORIAL OCR
# =========================
def save_ocr_history(raw_text: str, detected_products: list, child_id: str):
    if not detected_products:
        return

    extracted = extract_invoice_data(raw_text)

    if is_duplicate_invoice(raw_text):
        print("Factura duplicada detectada, no se guarda")
        return

    db.collection("ocr_history").add({
        "raw_text": raw_text,
        "detected_products": detected_products,
        "childId": child_id,
        "nro": extracted["nro"],
        "date": extracted["date"],
        "direccion": extracted["direccion"],
        "created_at": firestore.SERVER_TIMESTAMP
    })

    print("Factura guardada correctamente")


# =========================
# 📦 MAPA OCR PRODUCTOS
# =========================
def get_ocr_map():
    docs = db.collection("ocr_map").stream()
    products = []
    for doc in docs:
        products.append(doc.to_dict())
    return products