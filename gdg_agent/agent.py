import os
import logging
from typing import Dict, Union, List, Any

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import Client # Usamos el cliente directo para los sub-agentes
import requests

# Configuración de logs para ver la "Traza de Razonamiento"
logging.basicConfig(level=logging.INFO)
load_dotenv()

# ==========================================
# 🛠️ NIVEL 1: HERRAMIENTAS DETERMINISTAS (IO TOOLS)
# ==========================================

def get_upcoming_events(month: str) -> str:
    """
    CONSULTA OBLIGATORIA para fechas de eventos.
    Accede a la base de datos privada del GDG UAM.
    
    Args:
        month (str): El mes a consultar (ej: 'Marzo', 'Abril').
    """
    # Base de datos simulada con sabor "GDG UAM"
    events_db = {
        "marzo": [
            {"dia": 14, "titulo": "Taller de Agentes con Google ADK", "speaker": "Tu (GDE)", "tipo": "Workshop"},
            {"dia": 21, "titulo": "Cervezas & Networking en la Cantina", "speaker": "Comunidad", "tipo": "Social"},
            {"dia": 28, "titulo": "Women Techmakers: Panel de Liderazgo", "speaker": "Invitadas Top", "tipo": "Panel"}
        ],
        "abril": [
            {"dia": 11, "titulo": "Google I/O Extended Watchparty", "speaker": "Sundar Pichai (Streaming)", "tipo": "Keynote"}
        ]
    }
    
    key = month.lower().strip()
    data = events_db.get(key)
    
    if not data:
        return f"INFO: No hay eventos confirmados en la base de datos interna para {month}."
    
    return str(data)

def publish_to_web(content: str) -> str:
    """
    ACCIÓN DE ALTO RIESGO: Publica contenido en la web pública.
    REQUIERE APROBACIÓN EXPLÍCITA DEL USUARIO (Human-in-the-Loop).
    
    Args:
        content (str): El contenido final en HTML o Markdown a publicar.
    """
    print(f"\n[SYSTEM ACTION] 🚀 Iniciando protocolo de publicación...")
    
    web_url = os.environ.get("PUBLIC_WEB_URL")
    if not web_url:
        return "❌ ERROR TÉCNICO: Variable PUBLIC_WEB_URL no configurada en el entorno."

    try:
        response = requests.post(
            f"{web_url}/api/publish",
            json={"content": content},
            timeout=10
        )
        if response.status_code == 200:
            return f"✅ ÉXITO: Newsletter publicada correctamente en {web_url}"
        else:
            return f"❌ ERROR API: El servidor web respondió {response.status_code}"
    except Exception as e:
        return f"❌ ERROR CONEXIÓN: {str(e)}"

# ==========================================
# 🕵️ NIVEL 2: AGENTES ESPECIALISTAS (AGENTS AS TOOLS)
# ==========================================
# Estrategia: Encapsulamos la "personalidad" del agente en una función.
# Esto evita errores de serialización y garantiza que el Jefe reciba texto limpio.

def consult_internal_specialist(question: str) -> str:
    """
    Llama al 'Especialista de Datos Internos'.
    Úsalo para interpretar fechas, horarios o detalles logísticos de eventos propios.
    NO tiene acceso a internet.
    
    Args:
        question (str): La pregunta sobre la agenda interna (ej: "¿Qué eventos hay en marzo y quién da la charla?").
    """
    try:
        # 1. Obtenemos datos crudos (RAG simplificado)
        raw_data = get_upcoming_events("marzo") + get_upcoming_events("abril")
        
        # 2. El sub-agente procesa los datos
        client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"""
            Eres el Gestor de Agenda del GDG. Tu trabajo es ser preciso y formal.
            DATOS DE LA DB: {raw_data}
            PREGUNTA DEL JEFE: {question}
            
            Instrucciones:
            - Extrae solo la info relevante.
            - Si no hay datos, dilo claramente.
            - No inventes nada que no esté en la DB.
            """
        )
        return f"[REPORTE INTERNO]: {response.text}"
    except Exception as e:
        return f"❌ Error en Especialista Interno: {str(e)}"

def consult_researcher(topic: str) -> str:
    """
    Llama al 'Investigador Tecnológico'.
    Úsalo para buscar noticias externas, tendencias o explicar conceptos técnicos.
    Tiene acceso a Google Search.
    
    Args:
        topic (str): El tema a investigar (ej: "Novedades de Gemini 1.5" o "Resumen de la imagen adjunta").
    """
    try:
        # Usamos el cliente con la herramienta de búsqueda integrada
        client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        
        # Configuramos la herramienta de búsqueda para este sub-agente
        # Nota: En versiones recientes de GenAI SDK, esto se configura así:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"""
            Eres un Investigador Tech para una newsletter universitaria.
            Tarea: Investiga sobre '{topic}'.
            
            Estilo:
            - Busca lo más reciente (2024-2025).
            - Resume en 3 puntos clave.
            - Sé breve, el Editor expandirá luego.
            """,
            config={
                'tools': [{'google_search': {}}] 
            }
        )
        return f"[REPORTE EXTERNO]: {response.text}"
    except Exception as e:
        return f"❌ Error en Investigador: {str(e)} (Verifica GOOGLE_API_KEY)"

# ==========================================
# 🎩 NIVEL 3: EL ORQUESTADOR (BOSS)
# ==========================================

editor_boss = LlmAgent(
    model="gemini-1.5-pro-002", # Usamos el modelo Pro para mejor razonamiento
    name="gdg_editor_in_chief",
    description="Orquestador principal de la GDG Newsroom.",
    instruction="""
    Eres el **Editor Jefe** de la Newsletter del GDG UAM (Universidad Autónoma de Madrid).
    
    🎯 **TU OBJETIVO:**
    Crear y publicar la newsletter mensual coordinando a tu equipo de especialistas.
    
    👥 **TU EQUIPO (HERRAMIENTAS):**
    1. `consult_internal_specialist`: Para fechas y eventos nuestros.
    2. `consult_researcher`: Para noticias del mundo tech (Google, AI, Web).
    3. `publish_to_web`: Para enviar el HTML final a la web (SOLO CON PERMISO).

    📝 **ESTRATEGIA DE COORDINACIÓN (Paso a Paso):**
    
    **FASE 1: INVESTIGACIÓN (Gathering)**
    - Primero, pregunta al especialista interno qué eventos tenemos este mes.
    - Segundo, pide al investigador una noticia "trending topic" para la intro.
    - *Nota:* Si el usuario sube una imagen, descríbela y pásale la descripción al investigador.
    
    **FASE 2: REDACCIÓN (Drafting)**
    - Escribe la newsletter en formato Markdown.
    - **TONO:** Universitario, energético, inclusivo, con emojis (🚀, 🐍, ☁️).
    - **ESTRUCTURA:**
      1. Intro ("¡Hola GDGers! 👋").
      2. La Noticia Tech de la semana (breve).
      3. 📅 AGENDA UAM (Usa los datos internos).
      4. Call to Action ("¡Apúntate ya!").
    
    **FASE 3: CONTROL DE CALIDAD (Human-in-the-Loop)**
    - Muestra el borrador al usuario.
    - 🛑 **DETENTE Y PREGUNTA:** "¿Te parece bien? ¿La publico?"
    - Si el usuario dice "SÍ" -> Llama a `publish_to_web`.
    - Si el usuario dice "NO" -> Pregunta qué cambiar y vuelve a la Fase 2.
    
    ⚠️ **REGLA DE ORO:** NUNCA llames a `publish_to_web` sin ver un "Sí" explícito del usuario.
    """,
    # Aquí pasamos las funciones wrapper que creamos arriba
    tools=[consult_internal_specialist, consult_researcher, publish_to_web]
)

# --- ADK ENTRY POINT ---
# Esta variable es la que busca el comando 'adk web'
root_agent = editor_boss