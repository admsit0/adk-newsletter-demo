# ☁️ Deployment Guide: Google Cloud Run

We are deploying to **Cloud Run**, Google's fully managed serverless platform.

## Why Cloud Run for Agents?

- **Statelessness:** Agents process a request and finish. They don't need persistent servers.
- **Security:** We use Identity-Based Access (IAM) instead of uploading keys.
- **Scale:** It handles 0 to 1000 concurrent users automatically.

---

## 1. The Container Strategy (`Dockerfile`)

We use a multi-stage optimized Dockerfile.

```dockerfile
# Use a lightweight, official Python image
FROM python:3.11-slim

# Security & Performance flags
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies layer (Cached for speed)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Create a non-root user (Security Best Practice)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Cloud Run injects the PORT environment variable
ENV PORT=8080

# Run Gunicorn server
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 \
    "google.adk.web.app:create_app(agent_module='main:editor_boss')"

```

---

## 2. Security: The `.dockerignore`

**WARNING:** Failing to include this file will upload your private keys to the cloud registry, creating a massive security vulnerability.

Ensure `.dockerignore` contains:

```text
.env
service_account.json
venv/
__pycache__
.git

```

---

## 3. Deploying (The Easy Way)

We have included a `deploy.sh` script.

1. **Edit the script:** Open `deploy.sh` and replace `YOUR_PROJECT_ID_HERE` with your actual ID.
2. **Make executable:** `chmod +x deploy.sh`
3. **Run:** `./deploy.sh`

### What happens behind the scenes?

The script executes this `gcloud` command:

```bash
gcloud run deploy gdg-newsroom \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account adk-agent-sa@YOUR-PROJECT.iam.gserviceaccount.com \
  --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=true,...

```

- **`--source .`**: Builds the container using Cloud Build (no local Docker needed).
- **`--service-account`**: Assigns the identity we created earlier. The container uses this identity to talk to Vertex AI **without** needing the `service_account.json` file inside the image. This is the **Secure Production Standard**.

---

## 4. Verification

1. Wait for the green checkmark: `Service [gdg-newsroom] has been deployed`.
2. Click the generated URL (e.g., `https://gdg-newsroom-xyz.a.run.app`).
3. Test the agent. Note that the first request might take 3-4 seconds (Cold Start), but subsequent ones will be instant.
