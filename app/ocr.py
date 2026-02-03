import base64
from google.cloud import vision

def extract_text_from_base64(base64_image: str) -> str:
    image_bytes = base64.b64decode(base64_image)

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    return response.full_text_annotation.text or ""
