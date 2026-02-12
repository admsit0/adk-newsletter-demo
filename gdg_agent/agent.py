import os
import logging
from typing import Dict, Union, List

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
import requests

# ==========================================
# CONFIG
# ==========================================

logging.basicConfig(level=logging.INFO)
load_dotenv()

# ==========================================
# INTERNAL DATABASE TOOL
# ==========================================

def get_upcoming_events(month: str) -> Union[List[Dict], str]:
    """
    Deterministic internal calendar database.
    """

    events_db = {
        "march": [
            {"day": 15, "title": "ADK Hands-on Workshop", "speaker": "GDE Expert"},
            {"day": 28, "title": "Women Techmakers Dinner", "speaker": "Community"}
        ],
        "april": [
            {"day": 10, "title": "Google I/O Extended Watchparty", "speaker": "All"}
        ]
    }

    key = month.lower().strip()
    result = events_db.get(key)

    if not result:
        return f"No events found in internal DB for {month}."

    return result


# ==========================================
# PUBLISH TOOL (DETERMINISTIC)
# ==========================================

def publish_to_web(content: str) -> str:
    """
    CRITICAL TOOL.
    Only callable after explicit user approval.
    """

    print("\n[SYSTEM ACTION] 🚀 Publishing...")

    web_url = os.environ.get("PUBLIC_WEB_URL")

    if not web_url:
        return "❌ ERROR: No PUBLIC_WEB_URL configured."

    try:
        response = requests.post(
            f"{web_url}/api/publish",
            json={"content": content},
            timeout=10
        )

        if response.status_code == 200:
            return f"✅ SUCCESS: Published at {web_url}"
        else:
            return f"❌ ERROR: Web returned {response.status_code}"

    except Exception as e:
        return f"❌ ERROR: Connection failed: {str(e)}"


# ==========================================
# SPECIALIST AGENTS
# ==========================================

internal_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="internal_data_specialist",
    description="Read-only access to internal GDG calendar.",
    instruction="""
You are a deterministic internal data specialist.

RULES:
- Always use 'get_upcoming_events' when asked about events.
- Never invent data.
- Return clean structured output.
- No marketing tone.
- No commentary.
""",
    tools=[get_upcoming_events]
)


research_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="research_specialist",
    description="Performs structured web research.",
    instruction="""
You are a research specialist.

RULES:
- Use 'google_search' for external information.
- Summarize clearly.
- Do not fabricate information.
- If search fails, report failure explicitly.
- Keep output concise and factual.
""",
    tools=[google_search]
)


# ==========================================
# SUPERVISOR / ORCHESTRATOR
# ==========================================

editor_boss = LlmAgent(
    model="gemini-2.0-flash-001",
    name="editor_in_chief",
    description="Supervises specialist agents to build the newsletter.",
    instruction="""
You are the Editor-in-Chief supervising two specialist agents:

- internal_data_specialist
- research_specialist

You must coordinate them.

=====================
PHASE 1 — PLANNING
=====================
Analyze the user request.
Decide which specialist to delegate to.

If events → delegate to internal_data_specialist.
If external news/trends → delegate to research_specialist.

Never answer directly if delegation is required.

=====================
PHASE 2 — SYNTHESIS
=====================
After receiving specialist outputs, compose a Markdown newsletter:

# GDG Monthly Newsletter
## Upcoming Events
## Community & Tech News
## Closing Notes

Professional, clean, structured.

=====================
PHASE 3 — CONFIRMATION
=====================
Ask:
Ready to publish?

Do NOT publish yet.

=====================
PHASE 4 — PUBLICATION
=====================
Only if user explicitly says YES:
Call publish_to_web with the exact Markdown.
Never modify after approval.

=====================
STRICT RULES
=====================
- Never invent data.
- Always delegate when required.
- Never publish without approval.
- Specialists are the source of truth.
""",
    tools=[publish_to_web],
    sub_agents=[internal_agent, research_agent]   # 🔥 THIS is the correct multi-agent pattern
)


# ADK ENTRY POINT
root_agent = editor_boss
