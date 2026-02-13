import os
import logging
from typing import Dict, Union, List

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
import requests

# Configuración de logs
logging.basicConfig(level=logging.INFO)
load_dotenv()

# ==========================================
# 🛠️ NIVEL 1: HERRAMIENTAS I/O (Tus "Manos")
# ==========================================

def get_upcoming_events(month: str) -> str:
    """
    Consulta la 'Base de Datos' interna del GDG UAM.
    Args:
        month (str): Mes a consultar (ej: "Marzo").
    """
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
    
    # Fallback para desarrollo local si no hay URL
    if not web_url: 
        print(f"⚠️ MODO DEBUG: Simulating publish because PUBLIC_WEB_URL is missing.")
        return "✅ MODO LOCAL: Publicación simulada con éxito (Falta variable PUBLIC_WEB_URL)."

    try:
        response = requests.post(f"{web_url}/api/publish", json={"content": content}, timeout=5)
        if response.status_code == 200:
            return f"✅ PUBLICADO: La newsletter ya está visible en {web_url}"
        return f"❌ Error del Servidor Web: {response.status_code}"
    except Exception as e:
        return f"❌ Error de Conexión: {str(e)}"

# ==========================================
# 🤖 NIVEL 2: AGENTES ESPECIALISTAS (Objetos ADK)
# ==========================================

# 1. Agente Interno
internal_agent = LlmAgent(
    model="gemini-2.5-flash",  # Modelo estable y rápido
    name="internal_specialist",
    description="Gestor de la agenda interna.",
    instruction="""
    Eres el **Secretario del GDG UAM**.
    Tu misión es consultar `get_upcoming_events` y reportar fechas exactas.
    Sé preciso, breve y devuelve los datos limpios.
    """,
    tools=[get_upcoming_events]
)

# 2. Agente Investigador
research_agent = LlmAgent(
    model="gemini-2.5-flash", # Modelo estable y rápido
    name="tech_researcher",
    description="Investigador de noticias tecnológicas.",
    instruction="""
    Eres el **Investigador Tech**.
    Usa `Google Search` para buscar noticias de ESTA SEMANA sobre IA y Google Cloud.
    Si te dan una imagen, descríbela.
    """,
    tools=[google_search]
)

# ==========================================
# 🔗 NIVEL 2.5: FUNCIONES PUENTE (Blindadas)
# ==========================================

def ask_internal_data(query: str) -> str:
    """Pregunta al especialista interno sobre la agenda."""
    print(f"\n[ORCHESTRATOR] 📞 Llamando a Internal Agent...")
    try:
        # Usamos .run() que es el método estándar para ejecutar una cadena
        response = internal_agent.run(query)
        # Aseguramos que devolvemos string, no objeto
        return getattr(response, 'text', str(response))
    except Exception as e:
        print(f"❌ Error en Internal: {e}")
        return f"Error consultando agenda interna: {str(e)}"

def ask_researcher(topic: str) -> str:
    """Pregunta al investigador sobre noticias externas."""
    print(f"\n[ORCHESTRATOR] 📞 Llamando a Researcher Agent...")
    try:
        # Usamos .run()
        response = research_agent.run(topic)
        # Aseguramos que devolvemos string, no objeto
        return getattr(response, 'text', str(response))
    except Exception as e:
        print(f"❌ Error en Researcher: {e}")
        return f"Error consultando noticias externas: {str(e)}"

# ==========================================
# 🎩 NIVEL 3: EL JEFE (ORQUESTADOR)
# ==========================================

editor_boss = LlmAgent(
    model="gemini-2.5-flash", # Modelo muy capaz para orquestar
    name="gdg_editor_boss",
    description="Editor Jefe que coordina la newsletter.",
    instruction="""
    Eres el **Community Lead & Editor** del GDG UAM. 
    Tu objetivo: Crear la newsletter mensual más *hypeante* del campus.

    🛠️ **TU EQUIPO:**
    1. `ask_internal_data`: Para saber nuestros eventos.
    2. `ask_researcher`: Para noticias tech.
    3. `publish_to_web`: Para publicar (SOLO AL FINAL).

    📋 **TU FLUJO DE TRABAJO (Estricto):**

    1. **RECOPILACIÓN:**
       - Llama a `ask_internal_data` para eventos del mes.
       - Llama a `ask_researcher` para una noticia top.

    2. **REDACCIÓN:**
       - Escribe en **Markdown** con emojis (🚀, 🐍, ☁️).
       - Estructura: Intro -> News Tech -> Agenda UAM -> Outro.

    3. **VERIFICACIÓN (Human-in-the-Loop):**
       - Muestra el borrador.
       - 🛑 **DETENTE Y PREGUNTA:** *"¿La publico?"*
       - **NO llames a `publish_to_web` todavía.**

    4. **ACCIÓN:**
       - SOLO si el usuario dice "SÍ" explícitamente, llama a `publish_to_web`.
    """,
    tools=[ask_internal_data, ask_researcher, publish_to_web]
)

# --- ENTRY POINT ---
root_agent = editor_boss
