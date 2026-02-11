````markdown
# 🛠️ Setup & Usage Guide

This guide covers everything from zero to "Hello World" with Vertex AI.

## 1. Google Cloud Environment Setup

### 🛑 Prerequisites

- A Google Cloud Account (or a workshop credit link).
- A project created in the console.

### Option A: Using Workshop Credits

1.  Open an **Incognito Window**.
2.  Navigate to your event URL (e.g., `trygcp.dev/...`).
3.  Sign in with your **Personal Gmail**.
4.  Click **"Access Credits"** and verify the balance.
5.  **Critical Step:** When creating the project in Google Cloud Console, ensure you select **"No Organization"** for the location.

### Option B: Enable APIs

You must enable these APIs for the code to work. Click the links or search in the console:

1.  [**Vertex AI API**](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com) (The Brain)
2.  [**Cloud Run Admin API**](https://console.cloud.google.com/marketplace/product/google/run.googleapis.com) (The Hosting)
3.  [**Cloud Build API**](https://console.cloud.google.com/marketplace/product/google/cloudbuild.googleapis.com) (The Builder)

---

## 2. Authentication (Service Account)

The ADK needs permission to talk to Vertex AI. We use a **Service Account** for this.

1.  Go to **IAM & Admin** > **Service Accounts**.
2.  Click **+ CREATE SERVICE ACCOUNT**.
    - **Name:** `adk-agent-sa`
    - **Role:** `Vertex AI User` (This is crucial! Without this, you get 403 Errors).
3.  **Generate Key:**
    - Click the new Service Account email.
    - Go to **KEYS** > **Add Key** > **Create new key** > **JSON**.
4.  **Install:**
    - Rename the downloaded file to `service_account.json`.
    - Move it to the root of this project folder.

---

## 3. Local Configuration

1.  **Create `.env` file:**
    Copy the `.env.template` file and rename it to `.env`.

    ```bash
    cp .env.template .env
    ```

2.  **Edit `.env`:**
    Fill in your specific details:

    ```ini
    GOOGLE_APPLICATION_CREDENTIALS="./service_account.json"
    GOOGLE_CLOUD_PROJECT="your-project-id-here" # Check your console URL for the ID
    GOOGLE_CLOUD_LOCATION="us-central1"
    GOOGLE_GENAI_USE_VERTEXAI="true"
    ```

---

## 4. Running the Agent

We use the ADK CLI tool to launch the visual interface.

```bash
# Syntax: adk web <filename>:<agent_variable>
adk web main:editor_boss
```
````

- **Success:** You should see `INFO: Uvicorn running on http://127.0.0.1:3000`.
- **Access:** Open your browser to `http://localhost:3000`.

### 🐛 Troubleshooting Common Errors

- **Error: "Quota exceeded" or "429"**
- _Cause:_ You are sending too many requests too fast, or have a brand new account.
- _Fix:_ Wait 1 minute and try again.

- **Error: "PermissionDenied: 403"**
- _Cause:_ Your Service Account is missing the `Vertex AI User` role.
- _Fix:_ Go back to IAM & Admin and add the role to the email address in your JSON file.

- **Error: "DefaultCredentialsError"**
- _Cause:_ Python can't find your JSON key.
- _Fix:_ Check the path in your `.env` file. It must match the actual file name exactly.
