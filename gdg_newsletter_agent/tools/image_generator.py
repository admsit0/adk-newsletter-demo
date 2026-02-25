import base64
from google.genai import Client, types

def generate_newsletter_image(prompt: str) -> str:
    """
    Genera una imagen ilustrativa para la newsletter usando Vertex AI.
    Args:
        prompt: Descripción detallada de lo que quieres que aparezca en la imagen.
    """
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
        
        return f"\n![Ilustración del GDG](data:image/png;base64,{img_str})\n"

    except Exception as e:
        return f"\n> *[Aviso: No se pudo generar la imagen ({str(e)})]*\n"
    