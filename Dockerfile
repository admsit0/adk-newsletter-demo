FROM python:3.11-slim

# Variables para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos curl para debug
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Instalamos librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY . .

# Creamos usuario appuser
RUN adduser --disabled-password --gecos '' appuser

# --- PERMISOS (Vital para que no falle al arrancar) ---
RUN chown -R appuser:appuser /app

USER appuser

# --- CONFIGURACIÓN DE RED ---
ENV PORT=8080
ENV HOST=0.0.0.0

# --- EL CAMBIO DE SINTAXIS ---
# Antes: adk web main:editor_boss ... (Fallaba porque no es un directorio)
# Ahora: adk web . ... (Le pasamos el punto '.' que significa "directorio actual")
CMD ["sh", "-c", "adk web . --host 0.0.0.0 --port ${PORT}"]