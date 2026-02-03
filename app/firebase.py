import firebase_admin
from firebase_admin import credentials, firestore
import os

cred = credentials.Certificate("OcrFirebaseKey.json")
firebase_admin.initialize_app(cred, {
    "projectId": "odontobbapp"
})

db = firestore.client()

def get_ocr_map():
    docs = db.collection("ocr_map").stream()
    products = []
    for doc in docs:
        products.append(doc.to_dict())
    return products

def save_ocr_history(raw_text: str, detected_products: list):
    if not detected_products:
        return

    db.collection("ocr_history").add({
        "raw_text": raw_text,
        "detected_products": detected_products,
        "created_at": firestore.SERVER_TIMESTAMP
    })
