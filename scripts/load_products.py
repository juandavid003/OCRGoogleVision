# from firebase_admin import credentials, firestore
# import firebase_admin

# # Inicializar Firebase
# cred = credentials.Certificate("OcrFirebaseKey.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# challenges_ref = db.collection("challenges")
# docs = challenges_ref.stream()

# count = 0

# for doc in docs:
#     data = doc.to_dict()

#     product_id = data.get("id")
#     title = data.get("title", "")
#     category = data.get("category", "unknown")

#     if not product_id:
#         continue  # saltar si no tiene id

#     # Generar aliases automáticos básicos
#     aliases = []
#     if title:
#         title_lower = title.lower()
#         aliases.append(title_lower)
#         aliases.append(title_lower.replace(" ", ""))
    
#     ocr_map_item = {
#         "id": product_id,
#         "brand": title.split(" ")[0] if title else "",  # ejemplo: "Pasta" de "Pasta Dental GINGIVIT"
#         "category": category,
#         "aliases": aliases
#     }

#     db.collection("ocr_map").document(product_id).set(ocr_map_item)
#     print(f"✔ OCR map creado para: {product_id}")
#     count += 1

# print(f"\n🔥 Total productos cargados en ocr_map: {count}")
