import unicodedata

def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

def detect_products(ocr_text: str, products: list):
    found = []
    text = normalize(ocr_text)

    for product in products:
        for alias in product.get("aliases", []):
            if normalize(alias) in text:
                found.append({
                    "id": product["id"],
                    "brand": product["brand"],
                    "category": product["category"]
                })
                break

    return found
