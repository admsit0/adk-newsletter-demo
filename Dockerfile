FROM python:3.11-slim

# Variables para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos curl para debug y limpieza
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Instalamos librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY . .

# Usuario de seguridad (importante en producción)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# --- CONFIGURACIÓN DE RED ---
# Cloud Run inyecta PORT=8080, pero lo definimos por si acaso.
ENV PORT=8080

# Truco: Muchas herramientas Python (como Uvicorn) leen estas variables automáticamente
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8080
ENV HOST=0.0.0.0

# --- COMANDO DE ARRANQUE ---
# Usamos "sh -c" explícito para asegurar que las variables se expanden bien.
# Ponemos los flags AL FINAL, que suele ser más seguro para el parser.
CMD ["sh", "-c", "adk web main:editor_boss --host 0.0.0.0 --port ${PORT}"]
