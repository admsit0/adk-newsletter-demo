# 🧠 Concept & Architecture: The GDG Newsroom Agent

## 1. The Core Problem

Community organizers spend disproportionate time synthesizing information from disparate sources to create simple newsletters. They need to aggregate:

- **Private Data:** Confirmed event dates (locked in internal spreadsheets/DBs).
- **Public Data:** Trending tech news (dynamic, web-based).
- **Creative Output:** Writing engaging copy in Markdown.
- **Safety:** Ensuring no "hallucinated" dates are published without approval.

## 2. The Solution: A Multi-Agent System

Instead of a single "God Prompt", we utilize a **Hub-and-Spoke (Orchestrator-Worker)** architecture. This separates concerns, reduces context pollution, and increases reliability.

### 🏛️ The Architecture Diagram

```mermaid
graph TD
    User((User)) -->|1. Request Newsletter + Optional Image| Boss[Orchestrator: Editor-in-Chief]

    subgraph "The Newsroom Team"
        Boss -->|2. Delegate: Dates?| Internal[Agent: Event Manager]
        Boss -->|3. Delegate: News/Vision?| Research[Agent: Researcher]

        Internal -->|2a. Tool Call| DB[(Internal DB)]
        Research -->|3a. Tool Call| Search(Google Search)
        Research -->|3b. Native Vision| Vision(Image Analysis)
    end

    Boss -->|4. Synthesis| Draft[Markdown Draft]
    Draft -->|5. Human-in-the-Loop| Approval{User Approves?}

    Approval -- Yes -->|6. Tool Call| Publish(Publish to Web)
    Approval -- No -->|6. Iterate| Boss
```

```

## 3. The Agents & Their Roles

### 🕵️ Agent A: The Internal Specialist (`internal_data`)

- **Persona:** A rigid, factual database administrator.
- **Superpower:** Deterministic access to private data.
- **Tool:** `get_upcoming_events(month)`.
- **Constraint:** It _cannot_ access the internet. It _must_ report "No events" if the database is empty.

### 🔬 Agent B: The Multimodal Researcher (`researcher`)

- **Persona:** A tech-savvy analyst who can read and see.
- **Superpowers:**
- **Web Search:** Uses `Google Search` to find real-time info (e.g., "Latest Gemini features").
- **Computer Vision:** Natively understands images uploaded by the user (e.g., reading a date from a JPG event poster).

- **Constraint:** It does not make decisions; it only gathers raw intelligence.

### 🎩 The Boss: Editor-in-Chief (`gdg_editor`)

- **Persona:** A creative leader and safety officer.
- **Superpower:** Orchestration and Tool Routing.
- **Responsibility:**
- Routes tasks (Text Search, Image Vision).
- Synthesizes the final Markdown.
- **Guardrail:** Enforces the "Human-in-the-Loop" protocol before calling the `publish_to_web` tool.

## 4. Key Concepts Demonstrated

1. **Code-First Agents:** We define behavior via Python objects (`LlmAgent`), not just strings.
2. **Tool Use (Function Calling):** bridging the gap between probabilistic AI and deterministic code.
3. **Multimodality:** Processing text and pixel data simultaneously.
4. **Reasoning Traces:** The ability to audit the "Chain of Thought" (CoT) as the agent selects tools.
```
