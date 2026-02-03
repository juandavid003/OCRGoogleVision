from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel


class Product(BaseModel):
    id: str
    brand: str
    category: str
    aliases: List[str]


class InvoiceBase64Request(BaseModel):
    image_base64: str
