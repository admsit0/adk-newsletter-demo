from google.adk.agents import LlmAgent
from gdg_newsletter_agent.tools.search import search_tech_news


tech_researcher = LlmAgent(
    model="gemini-2.5-flash",
    name="tech_researcher",
    description="Investigador tecnológico. Llámalo para buscar noticias, actualidad en internet o analizar tendencias.",
    instruction="""
    Eres el Investigador Tech del GDG. Usa 'google_search' para buscar la noticia más importante y reciente de la semana sobre IA o Google Cloud. 
    Resume los detalles clave en 2 o 3 puntos para que el Editor pueda utilizarlos.
    """,
    tools=[search_tech_news]
)
