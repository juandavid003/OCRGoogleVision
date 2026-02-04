FROM python:3.11-slim

# Instalar dependencias del sistema (necesarias para vision y grpc)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos requirements primero (mejor cache de Docker)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Variables de entorno dentro del contenedor
ENV FIREBASE_CREDENTIALS=/app/OcrFirebaseKey.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/OcrGoogleVisionFirebaseKey.json
ENV FIREBASE_PROJECT_ID=odontobbapp

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
