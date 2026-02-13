# 📰 GDG Newsroom Agent: From Python to Production

**A production-grade Multi-Agent System built with the Google Agent Development Kit (ADK).**

This project demonstrates how to build an intelligent "Newsroom" where a **Boss Agent** orchestrates a team of specialists to research, draft, and publish a newsletter for a Google Developer Group (GDG).

---

## 📂 Repository Structure: What is everything?

This repository contains all the moving parts needed to deploy a full agentic system. Here is what each file does:

| Component                   | Description                                                                                                                                                                              |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`gdg-newsletter-agent/`** | **The Brain.** Contains the ADK agent logic (`agent.py`), the specific prompts, and the tools definition.                                                                                |
| **`web_public/`**           | **The Frontend (Simulation).** A simple web application that simulates the GDG's public website. It exists so the Agent has a real destination to "publish" the newsletter to (via API). |
| **`gcp_setup.sh`**          | **⚡ RUN THIS FIRST.** A script that automatically enables all required Google Cloud APIs (Vertex AI, Cloud Run, Build) and sets up the IAM permissions.                                 |
| **`deploy.sh`**             | **The Deployment Script.** Automates the build and deploy process for both the `web_public` frontend and the `gdg-newsletter-agent` backend to Cloud Run.                                |
| **`Dockerfile`**            | **The Container.** Tells Google Cloud how to package the agent application (Python 3.11, dependencies, Gunicorn server) for production.                                                  |

---

## 🏗 Architecture

The system consists of two services running on **Google Cloud Run**:

1. **The Public Web (`gdg-public-web`):**

- A simple website visible to the world.
- Exposes an API endpoint `/api/publish` that the Agent calls.

2. **The Agent Service (`gdg-newsroom-agent`):**

- Hosts the ADK Agent.
- **Orchestrator:** "Editor-in-Chief" (Gemini 1.5 Pro).
- **Tools:** Google Search (Public info), Internal DB (Private info), and `publish_to_web` (Action).

---

## 🚀 Setup Guide

Follow these steps to deploy the entire system from scratch.

### 1. Prerequisites & Free Credits 🎁

To deploy this project, you need a Google Cloud Project with billing enabled.

**Using Workshop Credits (Free Account):**
If you are attending a workshop, you don't need to use your credit card. Follow these steps to activate your pass:

1. **Open an Incognito Window** in your browser.
2. **Go to the Event URL:** Navigate to **[https://trygcp.dev/e/YOUR_EVENT_ID](https://trygcp.dev)** (Replace `YOUR_EVENT_ID` with the code provided by the instructor).
3. **Sign In:** Log in with your **personal Gmail account** (avoid corporate/university emails if they have firewalls).
4. **Claim Credits:** Click the button **"Click Here to Access Your Credits!"**. You should see a confirmation (e.g., $10 USD added).
5. **Create Project:** When creating the project in the Google Cloud Console, select **"No Organization"** for the location.
6. **Link Billing:** Associate the project with the **"Google Cloud Platform Trial Billing Account"** (the one with the credits).

### 2. Initial Configuration (The "One-Time" Setup)

You need to prepare your GCP project to handle AI and Containers. We have a script for that.

1. **Open your terminal.**
2. **Set your project ID:**

```bash
gcloud config set project YOUR_PROJECT_ID

```

3. **Run the Setup Script:**
   This will enable APIs (Vertex AI, Cloud Build, etc.) and create the necessary Service Accounts.

```bash
bash gcp_setup.sh

```

_(Wait for the script to finish successfully before moving on)._

### 3. Deployment

We will deploy both the Frontend (Web) and the Backend (Agent) and connect them automatically.

1. **Run the Deployment Script:**

```bash
bash deploy.sh

```

2. **What happens next?**

- The script detects your project ID.
- It deploys the `web_public` service first and grabs its URL.
- It deploys the `gdg-newsletter-agent` service, injecting the Web URL as an environment variable (`PUBLIC_WEB_URL`) so the agent knows where to publish.

---

## 🤖 Usage

Once deployed, you will see two URLs in your terminal.

1. **Open the Agent URL:** This is the ADK chat interface.
2. **Interact with the Agent:**

- Type: _"Create the newsletter for this month."_
- **Observe:** The agent will check internal dates, search for news, and draft a text.

3. **The "Human-in-the-Loop":**

- The agent will **STOP** and ask: _"Ready to publish?"_
- If you say **"Yes"**, it will trigger the tool.

4. **Verify:**

- Open the **Public Web URL**.
- You should see your new newsletter live on the site!

---

## 🛠 Local Development (Optional)

If you want to run the agent locally before deploying:

1. **Install dependencies:**

```bash
pip install -r requirements.txt

```

2. **Configure Environment:**
   Create a `.env` file with your credentials:

```ini
GOOGLE_APPLICATION_CREDENTIALS="service_account.json"
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_GENAI_USE_VERTEXAI="true"
PUBLIC_WEB_URL="http://localhost:8080" # For local testing

```

3. **Run the Agent:**

```bash
adk web gdg-newsletter-agent/agent.py:root_agent

```

---

## 📄 License

MIT License. Created for the GDG on Campus UAM Workshop.
