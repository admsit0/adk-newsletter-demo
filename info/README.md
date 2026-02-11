# 📰 GDG Newsroom Agent: From Python to Production

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Stack](https://img.shields.io/badge/Stack-Google%20ADK%20%7C%20Vertex%20AI%20%7C%20Cloud%20Run-blue)

> **A production-grade Multi-Agent System built with the Google Agent Development Kit (ADK).**

This project demonstrates the engineering behind building intelligent agents. It goes beyond simple chatbots to create a system that acts, sees, and integrates with private business logic.

## ⚡ Key Features

| Feature                          | Description                                                                        |
| :------------------------------- | :--------------------------------------------------------------------------------- |
| **🤖 Multi-Agent Orchestration** | A "Boss" agent coordinates specialized sub-agents for research and data retrieval. |
| **🛠️ Custom Tooling**            | Connects LLMs to a local Python "Database" function (Deterministic output).        |
| **👁️ Multimodality**             | The agent can "see" event posters and extract details using Gemini Vision.         |
| **🛡️ Human-in-the-Loop**         | Implements safety guardrails requiring explicit user approval before publishing.   |
| **☁️ Serverless Deployment**     | Runs on Google Cloud Run, scaling to zero when not in use.                         |

## 📂 Project Structure

```text
gdg-newsroom/
├── .dockerignore           # Security configurations for container build
├── .env.template           # Template for environment variables
├── Dockerfile              # Production container definition
├── GUIDE.md                # Step-by-step workshop script
├── README.md               # This file
├── USAGE.md                # Setup and troubleshooting guide
├── deploy.sh               # One-click deployment script
├── main.py                 # The Application Logic (Agents & Tools)
└── requirements.txt        # Python dependencies

```

## 🚀 Getting Started

1. **Prerequisites:** Python 3.11+, Google Cloud Project with Vertex AI enabled.
2. **Installation:**

```bash
pip install -r requirements.txt

```

3. **Configuration:** Copy `.env.template` to `.env` and fill in your credentials.
4. **Run Locally:**

```bash
adk web main:editor_boss

```

## 📚 Workshop Resources

- **[Concept & Architecture](https://www.google.com/search?q=./concept.md)**: Deep dive into the agent design pattern.
- **[Deployment Guide](https://www.google.com/search?q=./DEPLOYMENT.md)**: How to ship this to Google Cloud Run.

## 📄 License

MIT License. Created for the GDG Community.
