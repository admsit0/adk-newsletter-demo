# 📘 ADK Standards & GDG Newsroom Architecture

This document combines the technical deployment standards for **Google ADK (Agent Development Kit)** with the conceptual architecture of the **GDG Newsroom Agent**. It serves as a comprehensive guide for building, structuring, and deploying multi-agent systems to **Cloud Run**.

---

## 1. 🧠 Concept: The GDG Newsroom Agent

Community organizers often struggle to synthesize disparate data sources. This system replaces "God Prompts" with a **Hub-and-Spoke (Orchestrator-Worker)** architecture to increase reliability and separate concerns.

### 🏛️ System Architecture

The system uses an **Editor-in-Chief** to coordinate specialized agents:

```mermaid
graph TD
    User((User)) -->|1. Request| Boss[Orchestrator: Editor-in-Chief]

    subgraph "The Newsroom Team"
        Boss -->|2. Delegate| Internal[Agent: Event Manager]
        Boss -->|3. Delegate| Research[Agent: Researcher]

        Internal -->|2a. Tool| DB[(Internal DB)]
        Research -->|3a. Tool| Search(Google Search)
        Research -->|3b. Vision| Vision(Image Analysis)
    end

    Boss -->|4. Synthesis| Draft[Markdown Draft]
    Draft -->|5. Loop| Approval{User Approves?}

    Approval -- Yes -->|6. Tool| Publish(Web)
    Approval -- No -->|6. Iterate| Boss

```

- **Agent A (Internal Specialist):** A factual DBA with deterministic access to private event data via `get_upcoming_events(month)`.
- **Agent B (Multimodal Researcher):** A tech analyst using **Google Search** and **Computer Vision** to gather real-time web info and analyze uploaded images.
- **The Boss (Editor-in-Chief):** The lead orchestrator who synthesizes Markdown and enforces "Human-in-the-Loop" protocols before publishing.

---

## 2. 🏗️ "Workspace" Directory Structure

ADK is designed to scan **Python packages**, not loose scripts. To ensure your agent is detected in production, follow this hierarchy:

### ✅ Correct Structure

```text
/ (root)
├── Dockerfile
├── requirements.txt
└── gdg_agent/          <-- 1. PACKAGE FOLDER (Your agent's name)
    ├── __init__.py     <-- 2. EMPTY FILE (Required for Python packages)
    └── agent.py        <-- 3. ENTRY POINT (Must be named 'agent.py')

```

- **Note:** Using a flat structure (e.g., `main.py` in root) will cause ADK to fail during the scanning process.

---

## 3. 🐍 Coding Conventions & Rules

Within `gdg_agent/agent.py`, you must adhere to specific ADK "hooks":

### Rule 1: The Magic Variable

You **must** assign your primary orchestrator to a variable named `root_agent` at the end of your file.

```python
# gdg_agent/agent.py
editor_boss = LlmAgent(...)
root_agent = editor_boss  # <--- MANDATORY

```

### Rule 2: Agents as Tools (The Wrapper Pattern)

ADK requires `tools` to be **callables** (functions), not objects. You cannot pass an agent object directly into another agent's tool list.

- **Incorrect ❌:** `tools = [research_agent]`
- **Correct ✅:** ```python
  def ask_researcher(query: str):
  return research_agent.route(query)
  tools = [ask_researcher]

```


```

---

## 4. 🐳 Docker Deployment (Cloud Run)

The ADK container requires specific permissions and network binding to function in Cloud Run.

### "Golden Master" Dockerfile

```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# CRITICAL: Permissions for .adk/ and logs
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=8080
ENV HOST=0.0.0.0

# Start command: "adk web ." scans for the gdg_agent package
CMD ["sh", "-c", "adk web . --host 0.0.0.0 --port ${PORT}"]

```

---

## 5. 🌍 Environment & IAM Configuration

A successful deployment requires the following Cloud Run environment variables:

| Variable                            | Purpose                                                                               |
| ----------------------------------- | ------------------------------------------------------------------------------------- |
| `GOOGLE_GENAI_USE_VERTEXAI=true`    | Enables the Google Cloud backend.                                                     |
| `GOOGLE_CLOUD_PROJECT=your-id`      | Identifies the billing project.                                                       |
| `GOOGLE_CLOUD_LOCATION=us-central1` | **Vital.** Routes inference to regions supporting specific models (e.g., Gemini 2.0). |

**Required IAM Roles:**

- **Vertex AI User:** To invoke models.
- **Storage Object Admin:** For build operations and logging.

---

## 🚦 Troubleshooting Summary

| Error                       | Real Meaning                       | Solution                                               |
| --------------------------- | ---------------------------------- | ------------------------------------------------------ |
| `Container failed to start` | Permissions or missing `agent.py`. | Use `chown` in Dockerfile and proper folder structure. |
| `No root_agent found`       | Missing the mandatory variable.    | Add `root_agent = your_agent` in `agent.py`.           |
| `Input should be callable`  | Passed an agent object as a tool.  | Wrap the agent in a `def` function.                    |
| `404 Model not found`       | Regional mismatch.                 | Set `GOOGLE_CLOUD_LOCATION` to `us-central1`.          |

Would you like me to generate a starter `agent.py` file based on this architecture?
