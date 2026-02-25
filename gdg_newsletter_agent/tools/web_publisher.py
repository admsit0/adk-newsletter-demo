import os
import requests

def publish_to_web(content: str) -> str:
    """Publica el contenido final en la web. SOLO EJECUTAR CON PERMISO EXPLICITO DEL USUARIO."""
    print(f"\n[SYSTEM ACTION] 🚀 Ejecutando publicación en la web...")
    web_url = os.environ.get("PUBLIC_WEB_URL")
    
    if not web_url:
        return "✅ MODO LOCAL: Publicación simulada con éxito (PUBLIC_WEB_URL no definida)."

    try:
        response = requests.post(f"{web_url}/api/publish", json={"content": content}, timeout=5)
        if response.status_code == 200:
            return f"✅ PUBLICADO EN WEB EXITOSAMENTE. Código {response.status_code}"
        else:
            return f"❌ Error del servidor web: Código {response.status_code}"
    except Exception as e:
        return f"❌ Error de conexión de red: {str(e)}"
    