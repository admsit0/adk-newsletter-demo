from google.adk.agents import LlmAgent
from gdg_newsletter_agent.tools.internal_db import get_upcoming_events

internal_specialist = LlmAgent(
    model="gemini-2.5-flash",
    name="internal_specialist",
    description="Especialista en la agenda interna. Llámalo SIEMPRE para conocer las fechas y eventos del GDG.",
    instruction="""
    Eres el Secretario del GDG. Usa la herramienta 'get_upcoming_events' para recuperar la agenda exacta del mes que te pidan.
    Devuelve la información de forma estructurada y concisa. No inventes absolutamente nada.
    """,
    tools=[get_upcoming_events]
)