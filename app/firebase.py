import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

cred = credentials.Certificate(FIREBASE_CREDENTIALS)

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

    db.collection("ocr_history").add({
        "raw_text": raw_text,
        "detected_products": detected_products,
        "childId": child_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })
