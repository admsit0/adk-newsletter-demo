# 🎤 Instructor's Hands-On Script

**Total Duration:** 50 Minutes (Code) + 10 Minutes (Demo)
**Objective:** Live-code the agent in 3 iterations, demonstrating the evolution from simple bot to intelligent system.

---

## 🛑 Pre-Flight Check

- [ ] Screen sharing is ON.
- [ ] Font size in VS Code is 16px+.
- [ ] `.env` and `service_account.json` are hidden from view (security).
- [ ] Have a file named `event_poster.jpg` ready on your desktop.

---

## 🏁 Iteration 1: The "Smoke Test" (10 mins)

_Narrative: "Let's prove we can talk to Google's Brain."_

1.  **Create `main.py`** and type:

    ```python
    from dotenv import load_dotenv
    from google.adk.agents import LlmAgent

    load_dotenv()

    # 1. Define a basic agent
    agent = LlmAgent(
        model="gemini-1.5-flash-001",
        name="becario",  # Intern
        description="A simple chat assistant.",
        instruction="Greet the user and confirm connection to Vertex AI."
    )
    ```

2.  **Run:** `adk web main:agent`
3.  **Demo:** Type "Hello". Show the response.

---

## 🛠️ Iteration 2: The Custom Tool (15 mins)

_Narrative: "The AI is smart, but it doesn't know about OUR meetup schedule. Let's give it access to our private 'database' using Python."_

1.  **Add to `main.py`:**

    ```python
    # ... imports

    # 2. Define the 'Database' function
    def get_upcoming_events(month: str):
        """Fetches events from internal DB."""
        events_db = {
            "march": [{"day": 15, "title": "ADK Workshop"}, {"day": 28, "title": "Networking"}],
            "april": [{"day": 10, "title": "Google I/O Watchparty"}]
        }
        return events_db.get(month.lower().strip(), "No events found.")

    # 3. Create the Specialist Agent
    internal_agent = LlmAgent(
        model="gemini-1.5-flash-001",
        name="internal_data",
        instruction="Fetch events using 'get_upcoming_events'. Do not invent dates.",
        tools=[get_upcoming_events] # <--- CONNECTING THE TOOL
    )
    ```

2.  **Run:** `adk web main:internal_agent`
3.  **Demo:** Ask "What's happening in March?".
4.  **Highlight:** "Look! It returned data that exists _only_ in my Python dictionary. No hallucinations."

---

## 🧠 Iteration 3: The Orchestrator & Multimodality (25 mins)

_Narrative: "Now we build the full Newsroom. We add Internet Search, Vision, and a Boss to manage it all."_

1.  **Update `main.py` (Full Code):**

    ```python
    from google.adk.tools import google_search # New Import!

    # ... (Keep get_upcoming_events)

    # Tool for Human Approval
    def publish_to_web(content: str):
        return "✅ Published to Website!"

    # ... (Keep internal_agent)

    # 4. The Researcher (With Vision & Search)
    research_agent = LlmAgent(
        model="gemini-1.5-flash-001",
        name="researcher",
        instruction="""
        You are a Researcher.
        1. Search web with 'google_search'.
        2. VISION: If user uploads an image, extract event details from it.
        """,
        tools=[google_search]
    )

    # 5. The Boss
    editor_boss = LlmAgent(
        model="gemini-1.5-flash-001",
        name="editor_boss",
        instruction="""
        You are the Editor.
        1. Ask 'internal_data' for dates.
        2. Ask 'researcher' for news (or to read an uploaded poster).
        3. Draft the newsletter.
        4. STOP and ask user for approval.
        5. ONLY if approved, call 'publish_to_web'.
        """,
        tools=[internal_agent, research_agent, publish_to_web]
    )
    ```

---

## 🌟 The "Wow" Demo Sequence

**Run:** `adk web main:editor_boss`

### Moment 1: Multimodality 👁️

1.  **Action:** Drag your `event_poster.jpg` into the chat.
2.  **Prompt:** _"This is the poster for our sponsor event. Extract the details and include them in the newsletter draft along with our internal March events."_
3.  **Observation:** The agent will acknowledge the image, "read" the text inside the JPG, and combine it with the database data.

### Moment 2: Reasoning Traces 🕵️

1.  **Action:** While the agent is thinking (loading spinner), click the **"Debug/Trace"** button in the UI.
2.  **Speaker Note:** "Look at this JSON. We can see the 'Boss' deciding to call the 'Researcher' first because it saw an image, then calling 'Internal Data'. This is the Chain of Thought."

### Moment 3: Human-in-the-Loop 🛡️

1.  **Observation:** The agent outputs the draft but **stops**. It does not say "Published".
2.  **Speaker Note:** "See? It has the tool to publish, but my prompt forbade it from using it without permission. This is AI Safety."
3.  **Action:** Type "Looks great, publish it."
4.  **Result:** The agent calls `publish_to_web` and you see the success message.

---

## 🚀 Final: Deployment

1.  Open `DEPLOYMENT.md`.
2.  Show the `Dockerfile` and `.dockerignore`.
3.  Run `./deploy.sh`.
4.  Share the URL with the room.

```
