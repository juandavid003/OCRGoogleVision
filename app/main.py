from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.ocr import extract_text_from_base64
from app.matcher import detect_products
from app.firebase import get_ocr_map, save_ocr_history
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "OcrGoogleVisionFirebaseKey.json"

app = FastAPI(title="Invoice OCR Microservice")

class InvoiceBase64Request(BaseModel):
    image_base64: str

@app.post("/analyze-invoice-base64")
async def analyze_invoice_base64(payload: InvoiceBase64Request):
    try:
        ocr_text = extract_text_from_base64(payload.image_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    products = get_ocr_map()
    found_products = detect_products(ocr_text, products)

    save_ocr_history(ocr_text, found_products)

    return {
        "raw_text": ocr_text,
        "detected_products": found_products
    }
