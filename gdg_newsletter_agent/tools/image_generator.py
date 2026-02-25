import base64
import io
from google.genai import Client

def generate_newsletter_image(prompt: str) -> str:
    """
    Genera una imagen ilustrativa para la newsletter usando Vertex AI.
    Args:
        prompt: Descripción detallada de lo que quieres que aparezca en la imagen.
    """
    print(f"\n[SYSTEM ACTION] 🎨 Pintando imagen: '{prompt}'...")
    
    try:
        # El cliente recoge las credenciales de tu .env automáticamente
        client = Client() 
        
        # Usamos el modelo de generación de imágenes de Google (Imagen 3)
        response = client.models.generate_image(
            model='imagen-4.0-generate-001', 
            prompt=prompt,
            config={'aspect_ratio': '16:9'}
        )
        
        # Extraemos la imagen generada
        image_pil = response.images[0]
        
        # TRUCO MÁGICO: Guardamos en memoria RAM y pasamos a Base64
        buffered = io.BytesIO()
        image_pil.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Devolvemos Markdown puro. ¡La web lo renderizará automáticamente!
        return f"\n![Ilustración del GDG](data:image/png;base64,{img_str})\n"

    except Exception as e:
        return f"\n> *[Aviso: No se pudo generar la imagen ({str(e)})]*\n"