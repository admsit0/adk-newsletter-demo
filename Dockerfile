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

# Creamos el usuario
RUN adduser --disabled-password --gecos '' appuser

# --- CORRECCIÓN CRÍTICA ---
# Cambiamos el dueño de la carpeta /app al usuario appuser
# para que 'adk web' pueda escribir sus archivos temporales.
RUN chown -R appuser:appuser /app

# Ahora sí cambiamos de usuario
USER appuser

# --- CONFIGURACIÓN DE RED ---
ENV PORT=8080
ENV HOST=0.0.0.0

# --- COMANDO DE ARRANQUE ---
# Usamos el modo shell explícito y aseguramos host 0.0.0.0
CMD ["sh", "-c", "adk web . --host 0.0.0.0 --port ${PORT}"]
