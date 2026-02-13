#!/bin/bash
# =================================================================
# INSTRUCCIONES PREVIAS (LEER ANTES DE EJECUTAR)
# 1. Crear cuenta en GCP y activar facturación: https://console.cloud.google.com/billing
# 2. Si es una cuenta nueva, asegúrate de tener un proyecto seleccionado.
# 3. Ir a la consola de GCP y abrir Cloud Shell(icono de consola arriba a la dcha).
# =================================================================

# Obtener automáticamente el ID del proyecto actual
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    echo "ERROR: No se detectó ningún proyecto activo. Ejecuta 'gcloud config set project NOMBRE_DE_TU_PROYECTO' primero."
    exit 1
fi

# Obtener el número del proyecto para identificar la Service Account por defecto
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT_EMAIL="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

echo "Configurando proyecto: $PROJECT_ID"
echo "Usando Service Account: $SERVICE_ACCOUNT_EMAIL"

# --- Configuración de gcloud ---
gcloud config set project $PROJECT_ID

# --- Habilitar Servicios Necesarios ---
echo "Habilitando APIs de Google Cloud..."
gcloud services enable \
    aiplatform.googleapis.com \
    logging.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    iam.googleapis.com \
    --project $PROJECT_ID

# --- Asignación de Roles IAM ---
echo "Asignando permisos a la Service Account..."

# Rol para Cloud Build
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role=roles/cloudbuild.builds.builder

# Rol para Storage (Administrador de objetos)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role=roles/storage.objectAdmin

# Rol para Vertex AI (aiplatform.user)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role=roles/aiplatform.user

