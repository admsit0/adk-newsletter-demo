import os
import logging
from typing import Dict, Union, List

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
import requests

# Configure logging for "Reasoning Traces" visibility in terminal
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# ==========================================
# 🛠️ CUSTOM TOOLS (The "Hands")
# ==========================================

def get_upcoming_events(month: str) -> Union[List[Dict], str]:
    """
    Retrieves confirmed events from the internal GDG database.
    Deterministic source of truth.
    
    Args:
        month (str): The target month (e.g., "March").
    """
    # Simulated Internal Database
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
    return events_db.get(key, f"No events found in the internal DB for {month}.")

def publish_to_web(content: str) -> str:
    """
    Publishes the final content to the GDG website UI.
    CRITICAL: This tool must ONLY be called after explicit user approval.
    """
    print(f"\n[SYSTEM ACTION] 🚀 Sending to Public Web...")
    
    # Obtenemos la URL de la variable de entorno (inyectada en el deploy)
    web_url = os.environ.get("PUBLIC_WEB_URL")
    
    if not web_url:
        return "❌ ERROR: No PUBLIC_WEB_URL configured."

    try:
        # Hacemos la llamada real a la API que acabamos de crear
        response = requests.post(
            f"{web_url}/api/publish",
            json={"content": content},
            timeout=10
        )
        
        if response.status_code == 200:
            return f"✅ SUCCESS: Published! View it at: {web_url}"
        else:
            return f"❌ ERROR: Web returned {response.status_code}"
            
    except Exception as e:
        return f"❌ ERROR: Connection failed: {str(e)}"

# ==========================================
# 🤖 SPECIALIST AGENTS (The "Team")
# ==========================================

# Agent 1: The Internal Data Specialist
internal_agent = LlmAgent(
    model="gemini-1.5-flash-001",
    name="internal_data_specialist",
    description="Has access to the private GDG calendar.",
    instruction=(
        "You are the Internal Data Specialist. "
        "Your ONLY job is to fetch event dates using 'get_upcoming_events'. "
        "Do not invent events. If the tool returns nothing, state that."
    ),
    tools=[get_upcoming_events]
)

# Agent 2: The Researcher (Multimodal + Search)
research_agent = LlmAgent(
    model="gemini-1.5-flash-001",
    name="research_specialist",
    description="Can search the web and analyze images.",
    instruction=(
        "You are the Tech Researcher. You have two capabilities:\n"
        "1. Search the internet using 'google_search' for trending news.\n"
        "2. VISION: If the user provides an image (like an event poster), "
        "analyze it visually to extract details (dates, speakers, titles)."
    ),
    tools=[google_search]
)

# ==========================================
# 🧠 THE ORCHESTRATOR (The "Boss")
# ==========================================

editor_boss = LlmAgent(
    model="gemini-1.5-flash-001",
    name="editor_in_chief",
    description="Orchestrates the newsletter creation.",
    instruction=(
        "You are the Editor-in-Chief of the GDG Newsletter.\n"
        "Your goal is to produce a high-quality Markdown newsletter.\n\n"
        "EXECUTION PIPELINE:\n"
        "1. Gather Data: Ask 'internal_data_specialist' for events and 'research_specialist' for news.\n"
        "   (Note: If the user uploaded an image, pass it to the researcher).\n"
        "2. Draft: Compile the information into a fun, emoji-rich Markdown format.\n"
        "3. REVIEW PAUSE: Show the draft to the user and ask: 'Ready to publish?'\n"
        "4. ACTION: ONLY if the user explicitly agrees (e.g., 'Yes', 'Go ahead'), "
        "call the 'publish_to_web' tool. If they disagree, ask for feedback."
    ),
    # The Boss uses the other agents AND the final action tool
    tools=[internal_agent, research_agent, publish_to_web]
)
