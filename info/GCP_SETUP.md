1. go to gcp and create account

2. go to link and activate billing account (tarjeta; vale una sin dinero)
   https://console.cloud.google.com/billing

3. meterse al proyecto. Te crea un 'My First Project', ese te vale.

4.

# 1. Dar permiso para construir (Cloud Build)

gcloud projects add-iam-policy-binding project-c809664c-efec-464a-9ea \
 --member=serviceAccount:937925299175-compute@developer.gserviceaccount.com \
 --role=roles/cloudbuild.builds.builder

# 2. Dar permiso para escribir archivos temporales (Storage)

gcloud projects add-iam-policy-binding project-c809664c-efec-464a-9ea \
 --member=serviceAccount:937925299175-compute@developer.gserviceaccount.com \
 --role=roles/storage.objectAdmin

# 3. Activar vertex api y darle permiso

gcloud services enable aiplatform.googleapis.com --project project-c809664c-efec-464a-9ea

gcloud projects add-iam-policy-binding project-c809664c-efec-464a-9ea \
 --member=serviceAccount:937925299175-compute@developer.gserviceaccount.com \
 --role=roles/aiplatform.user

5. desplegar en cloud run! (a mi me gusta con un deploy.sh desde consola por facilidad)
