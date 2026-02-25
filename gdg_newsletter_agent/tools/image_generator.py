import base64
import uuid
from google.genai import Client, types

image_cache = {}

def generate_newsletter_image(prompt: str) -> str:
    """Genera una imagen ilustrativa para la newsletter usando Vertex AI."""
    print(f"\n[SYSTEM ACTION] 🎨 Pintando imagen: '{prompt}'...")
    
    try:
        client = Client() 
        
        response = client.models.generate_images(
            model='imagen-3.0-generate-002', 
            prompt=prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio='16:9',
                number_of_images=1
            )
        )
        
        img_bytes = response.generated_images[0].image.image_bytes
        img_str = base64.b64encode(img_bytes).decode("utf-8")
        
        # 1. Guardamos el Base64 gigante en nuestra caché de Python
        image_id = f"IMG_REF_{uuid.uuid4().hex[:8]}"
        image_cache[image_id] = f"data:image/png;base64,{img_str}"
        
        # 2. Devolvemos al agente un string diminuto (¡Solo consume unos pocos tokens!)
        return f"\n![Ilustración del GDG]({image_id})\n"

    except Exception as e:
        return f"\n> *[Aviso: No se pudo generar la imagen ({str(e)})]*\n"
    