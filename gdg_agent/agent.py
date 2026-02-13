import os
import logging
from typing import Dict, Union, List

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
import requests

# Configuración de logs para ver la orquestación en la consola
logging.basicConfig(level=logging.INFO)
load_dotenv()

# ==========================================
# 🛠️ NIVEL 1: HERRAMIENTAS I/O (Tus "Manos")
# ==========================================

def get_upcoming_events(month: str) -> str:
    """
    Consulta la 'Base de Datos' interna del GDG UAM.
    Fuente de verdad única para fechas y salas.
    
    Args:
        month (str): Mes a consultar (ej: "Marzo").
    """
    # Simulamos datos de la universidad
    events_db = {
        "marzo": [
            {"dia": 14, "titulo": "Workshop ADK: De Python a Producción", "sala": "Lab 4", "speaker": "Tú (GDE)"},
            {"dia": 21, "titulo": "Pizza & Networking", "sala": "Cafetería Ciencias", "speaker": "Comunidad"}
        ],
        "abril": [
            {"dia": 11, "titulo": "Google I/O Extended Watchparty", "sala": "Salón de Actos", "speaker": "Streaming"}
        ]
    }
    
    key = month.lower().strip()
    data = events_db.get(key)
    if not data:
        return f"INFO: No constan eventos en la DB interna para {month}."
    return str(data)

def publish_to_web(content: str) -> str:
    """
    Publica la newsletter en la web del GDG.
    ⚠️ CRÍTICO: REQUIERE APROBACIÓN EXPLÍCITA DEL USUARIO.
    """
    print(f"\n[SYSTEM ACTION] 🚀 Conectando con CMS del GDG...")
    web_url = os.environ.get("PUBLIC_WEB_URL")
    
    if not web_url: 
        return "❌ ERROR: Variable PUBLIC_WEB_URL no configurada."

    try:
        # Simulamos latencia de red real
        response = requests.post(f"{web_url}/api/publish", json={"content": content}, timeout=5)
        if response.status_code == 200:
            return f"✅ PUBLICADO: La newsletter ya está visible en {web_url}"
        return f"❌ Error del Servidor Web: {response.status_code}"
    except Exception as e:
        return f"❌ Error de Conexión: {str(e)}"

# ==========================================
# 🤖 NIVEL 2: AGENTES ESPECIALISTAS (Objetos ADK)
# ==========================================

# AGENTE 1: EL ORGANIZADOR (Datos Internos)
internal_agent = LlmAgent(
    model="gemini-2.5-flash",  # <--- MODELO ACTUALIZADO
    name="internal_specialist",
    description="Gestor de la agenda interna de la universidad.",
    instruction="""
    Eres el **Secretario del GDG UAM**.
    Tu única misión es consultar la herramienta `get_upcoming_events` y reportar fechas exactas.
    - No inventes eventos.
    - No asumas horarios si no están en la herramienta.
    - Sé preciso y breve (formato JSON o lista).
    """,
    tools=[get_upcoming_events]
)

# AGENTE 2: EL CAZADOR DE TENDENCIAS (Búsqueda Web)
research_agent = LlmAgent(
    model="gemini-2.5-flash",  # <--- MODELO ACTUALIZADO
    name="tech_researcher",
    description="Investigador de noticias tecnológicas y tendencias.",
    instruction="""
    Eres el **Investigador Tech** del campus.
    Tu misión es traer contenido fresco usando `Google Search`.
    - Busca noticias de ÚLTIMA HORA (esta semana).
    - Prioriza temas: IA Generativa, Google Cloud, Python.
    - Si te dan una imagen, descríbela y busca contexto sobre ella.
    """,
    tools=[google_search]
)

# ==========================================
# 🔗 NIVEL 2.5: FUNCIONES PUENTE (Orquestación)
# ==========================================
# Estas funciones envuelven a los agentes para evitar errores de serialización
# y permitir que el Jefe los use como herramientas robustas.

def ask_internal_data(query: str) -> str:
    """
    Pregunta al especialista interno sobre la agenda del GDG.
    Args: query (str): La pregunta (ej: "¿Qué hay en marzo?").
    """
    print(f"\n[ORCHESTRATOR] 📞 Llamando a Internal Agent...")
    try:
        return internal_agent.run(query)
    except Exception as e:
        return f"❌ Error interno: {str(e)}"

def ask_researcher(topic: str) -> str:
    """
    Pregunta al investigador sobre noticias externas o análisis.
    Args: topic (str): El tema a investigar.
    """
    print(f"\n[ORCHESTRATOR] 📞 Llamando a Researcher Agent...")
    try:
        return research_agent.run(topic)
    except Exception as e:
        return f"❌ Error investigador: {str(e)}"

# ==========================================
# 🎩 NIVEL 3: EL JEFE (ORQUESTADOR)
# ==========================================

editor_boss = LlmAgent(
    model="gemini-2.5-flash", # <--- MODELO ACTUALIZADO (Rápido y capaz)
    name="gdg_editor_boss",
    description="Editor Jefe que coordina la newsletter.",
    instruction="""
    Eres el **Community Lead & Editor** del GDG UAM. 
    Tu objetivo: Crear la newsletter mensual más *hypeante* del campus.

    🛠️ **TU EQUIPO:**
    1. `ask_internal_data`: Para saber CUÁNDO y DÓNDE son nuestros eventos.
    2. `ask_researcher`: Para saber QUÉ está pasando en el mundo tech.
    3. `publish_to_web`: Para enviar el email (SOLO AL FINAL).

    📋 **TU FLUJO DE TRABAJO (Síguelo estrictamente):**

    1. **RECOPILACIÓN (Gathering):**
       - Pregunta a `ask_internal_data` por los eventos del mes actual.
       - Pregunta a `ask_researcher` por 1 noticia "Bombazo" de la semana.

    2. **REDACCIÓN (Drafting):**
       - Escribe en **Markdown** atractivo.
       - Usa muchos emojis: 🚀, 🐍, ☁️, 🍕.
       - Estructura:
         - **Intro:** Saludo con energía ("¡Hola GDGers!").
         - **La News:** Resumen de lo que trajo el researcher.
         - **Agenda UAM:** Lista bonita de eventos (Día - Título - Sala).
         - **Outro:** "¡Nos vemos en el código!".

    3. **VERIFICACIÓN (Human-in-the-Loop):**
       - Muestra el borrador resultante.
       - 🛑 **DETENTE.** Pregunta al usuario: *"¿Mola? ¿La publico?"*.
       - **NO llames a `publish_to_web` todavía.**

    4. **ACCIÓN (Execution):**
       - SOLO si el usuario dice "SÍ/Dale/Publish", llama a `publish_to_web`.
       - Si dice que no, pide feedback y reescribe.
    """,
    # El jefe usa los "Puentes" y la herramienta de publicación
    tools=[ask_internal_data, ask_researcher, publish_to_web]
)

# --- ENTRY POINT ---
root_agent = editor_boss