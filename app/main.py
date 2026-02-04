from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

load_dotenv() 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

from app.models import InvoiceBase64Request
from app.ocr import extract_text_from_base64
from app.matcher import detect_products
from app.firebase import get_ocr_map, save_ocr_history

app = FastAPI(title="Invoice OCR Microservice")


@app.post("/analyze-invoice-base64")
async def analyze_invoice_base64(payload: InvoiceBase64Request):
    try:
        ocr_text = extract_text_from_base64(payload.image_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    products = get_ocr_map()
    found_products = detect_products(ocr_text, products)

    save_ocr_history(ocr_text, found_products, payload.childId)

    return {
        "raw_text": ocr_text,
        "detected_products": found_products
    }
