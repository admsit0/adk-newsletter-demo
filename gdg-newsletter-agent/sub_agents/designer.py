from google.adk.agents import LlmAgent
from tools.image_generator import generate_newsletter_image

graphic_designer = LlmAgent(
    model="gemini-2.5-flash",
    name="graphic_designer",
    description="Diseñador gráfico. Llámalo EXCLUSIVAMENTE cuando necesites crear una imagen visual para ilustrar la newsletter.",
    instruction="""
    Eres el Diseñador Gráfico del GDG UAM. 
    Usa la herramienta 'generate_newsletter_image' para crear una imagen espectacular basada en el tema principal del mes.
    Tu única tarea es devolver el texto Markdown exacto que te devuelva la herramienta. No añadas comentarios extra.
    """,
    tools=[generate_newsletter_image]
)