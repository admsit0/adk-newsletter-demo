FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias y curl (útil para debug)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Creamos usuario seguro
RUN adduser --disabled-password --gecos '' appuser
USER appuser

ENV PORT=8080

# --- EL CAMBIO IMPORTANTE ---
# Usamos el CLI de ADK directamente.
# Le forzamos a escuchar en 0.0.0.0 para que Cloud Run lo detecte.
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080", "main:editor_boss"]

