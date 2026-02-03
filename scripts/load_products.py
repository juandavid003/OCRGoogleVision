from firebase_admin import credentials, firestore
import firebase_admin

cred = credentials.Certificate("OcrFirebaseKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

products = [
    {
        "id": "topident_infantil",
        "brand": "TOPIDENT",
        "category": "Tópico Bucal",
        "aliases": ["topident infantil", "topident inf", "topident niño", "topident nino"]
    },
    {
        "id": "soral_stop",
        "brand": "SORAL",
        "category": "Pasta Dental",
        "aliases": ["soral stop", "soral sensibilidad", "soral stop pasta"]
    }
]

for p in products:
    db.collection("ocr_map").document(p["id"]).set(p)

print("Catálogo OCR cargado con éxito ✅")
