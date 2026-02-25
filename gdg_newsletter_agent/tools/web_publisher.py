import os
import requests
from gdg_newsletter_agent.tools.image_generator import image_cache

def publish_to_web(content: str, post_type: str) -> str:
    """
    Publica el contenido final en la web. SOLO EJECUTAR CON PERMISO EXPLICITO DEL USUARIO.
    """
    print(f"\n[SYSTEM ACTION] 🚀 Ejecutando publicación en web (Tipo: {post_type})...")
    
    # MAGIA: Intercambiamos el ID ligero por el Base64 real antes de mandarlo a la web
    for img_id, base64_data in image_cache.items():
        if img_id in content:
            content = content.replace(img_id, base64_data)
            
    web_url = os.environ.get("PUBLIC_WEB_URL")
    
    if not web_url:
        return f"✅ MODO LOCAL: Publicación [{post_type}] simulada con éxito."

    try:
        payload = {"content": content, "post_type": post_type}
        response = requests.post(f"{web_url}/api/publish", json=payload, timeout=5)
        if response.status_code == 200:
            return f"✅ PUBLICADO EN WEB EXITOSAMENTE. Código {response.status_code}"
        else:
            return f"❌ Error del servidor web: Código {response.status_code}"
    except Exception as e:
        return f"❌ Error de conexión de red: {str(e)}"
    