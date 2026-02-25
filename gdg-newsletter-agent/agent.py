import logging
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

from .tools.web_publisher import publish_to_web

# Importamos a TODO el equipo
from .sub_agents.internal import internal_specialist
from .sub_agents.researcher import tech_researcher
from .sub_agents.designer import graphic_designer # <-- ¡Nuevo empleado!

logging.basicConfig(level=logging.INFO)
load_dotenv()

editor_boss = LlmAgent(
    model="gemini-2.5-flash",
    name="gdg_editor_boss",
    description="Editor Jefe. Orquesta al equipo y gestiona la publicación final.",
    instruction="""
    Eres el Editor Jefe del GDG UAM. Tu misión es coordinar la creación de la newsletter.
    
    FLUJO DE TRABAJO ESTRICTO:
    1. DATOS: Pide a 'internal_specialist' los eventos del mes.
    2. NOTICIAS: Pide a 'tech_researcher' una noticia tecnológica reciente.
    3. ARTE: Pide a 'graphic_designer' que genere una imagen de cabecera relacionada con la noticia.
    4. REDACCIÓN: Une todo. Coloca la imagen (el Markdown que te dio el diseñador) al principio. Escribe el resto con emojis y tono universitario.
    5. INTERCEPCIÓN: Presenta el borrador. **Intercepta solicitudes de publicación**. Pregunta: "¿Estás conforme? ¿Procedo a publicarla en la web?".
    6. ACCIÓN: SOLO si el usuario confirma ("Sí", "Publica"), ejecuta 'publish_to_web'.
    """,
    # Añadimos al diseñador a la lista de sub-agentes
    sub_agents=[internal_specialist, tech_researcher, graphic_designer], 
    tools=[publish_to_web]
)

root_agent = editor_boss
