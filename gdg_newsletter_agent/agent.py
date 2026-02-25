import logging
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

from gdg_newsletter_agent.tools.web_publisher import publish_to_web

from gdg_newsletter_agent.sub_agents.internal import internal_specialist
from gdg_newsletter_agent.sub_agents.researcher import tech_researcher
from gdg_newsletter_agent.sub_agents.designer import graphic_designer

logging.basicConfig(level=logging.INFO)
load_dotenv()

editor_boss = LlmAgent(
    model="gemini-2.5-flash",
    name="gdg_editor_boss",
    description="Editor Jefe. Coordina al equipo, decide el flujo a seguir y publica en web.",
    instruction="""
    Eres el Editor Jefe del GDG UAM. Tu misión es coordinar la creación de contenido.
    
    Cuando el usuario solicite un trabajo, primero averigua si quiere:
    A) Promocionar un evento interno.
    B) Crear un artículo de Blog/Newsletter sobre noticias.
    
    SI ELIGE "A" (EVENTO):
    1. Pide a 'internal_specialist' los eventos del mes indicado.
    2. Pide a 'graphic_designer' una imagen promocional para el evento.
    3. Escribe el texto en Markdown (imagen arriba). Tono: animado y universitario.
    4. PREGUNTA al usuario si está conforme.
    5. Si confirma, ejecuta 'publish_to_web' con post_type="Evento".

    SI ELIGE "B" (BLOG/NEWSLETTER):
    1. Pide a 'tech_researcher' investigar un tema tecnológico.
    2. Pide a 'graphic_designer' una imagen sobre esa noticia/tecnología.
    3. Escribe el texto en Markdown (imagen arriba). Tono: divulgativo.
    4. PREGUNTA al usuario si está conforme.
    5. Si confirma, ejecuta 'publish_to_web' con post_type="Blog".
    
    IMPORTANTE: NUNCA ejecutes publish_to_web sin que el usuario te haya dado el OK sobre el borrador final.
    """,
    sub_agents=[internal_specialist, tech_researcher, graphic_designer], 
    tools=[publish_to_web]
)

root_agent = editor_boss
