#!/bin/bash
PROJECT_ID=$(gcloud config get-value project)
REGION="europe-southwest1"
SERVICE_NAME_WEB="gdg-public-web"
SERVICE_NAME_AGENT="gdg-newsroom-agent"

# Colores para logs
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}--- 1. DESPLEGANDO LA WEB PÚBLICA (Frontend) ---${NC}"
gcloud run deploy $SERVICE_NAME_WEB \
  --source ./web_public \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --quiet

# Capturamos la URL del servicio web recién desplegado
WEB_URL=$(gcloud run services describe $SERVICE_NAME_WEB --platform managed --region $REGION --format 'value(status.url)' --project $PROJECT_ID)

echo -e "${GREEN}--- WEB LISTA EN: $WEB_URL ---${NC}"
echo -e "${GREEN}--- 2. DESPLEGANDO EL AGENTE (Conectado a la Web) ---${NC}"

# Desplegamos el agente pasándole la URL como variable de entorno
gcloud run deploy $SERVICE_NAME_AGENT \
  --source . \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=true \
  --set-env-vars PUBLIC_WEB_URL=$WEB_URL \
  --quiet

echo -e "${GREEN}--- ¡TODO LISTO! ---${NC}"
echo -e "1. Abre la web pública en una pestaña: $WEB_URL"
echo -e "2. Abre el chat del agente en otra: (URL que salga arriba)"
