# Use slim image for smaller footprint
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Cloud Run injects PORT (default 8080)
ENV PORT=8080

# Run with Gunicorn (Production WSGI) wrapping ADK's app factory
# Syntax: "google.adk.web.app:create_app(agent_module='FILENAME:AGENT_VARIABLE')"
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 \
    "google.adk.web.app:create_app(agent_module='main:editor_boss')"
    