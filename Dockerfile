FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos curl por si necesitamos debug
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usuario de seguridad
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Cloud Run inyecta esta variable (8080)
ENV PORT=8080

# --- EL CAMBIO: Usamos modo shell para garantizar que pilla los flags ---
# Forzamos host 0.0.0.0 (para que Cloud Run entre) y el puerto correcto
CMD adk web --host 0.0.0.0 --port $PORT main:editor_boss
