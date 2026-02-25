import urllib.request
import urllib.parse
import json

def search_tech_news(topic: str) -> str:
    """
    Busca información y noticias tecnológicas sobre un tema en Wikipedia.
    Alternativa a Google Search que no da problemas de compatibilidad de herramientas.
    Args:
        topic: El concepto o noticia tecnológica a buscar.
    """
    print(f"\n[SYSTEM ACTION] 🔍 Investigando en la web sobre: '{topic}'...")
    try:
        url = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(topic)}&utf8=&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            results = data.get('query', {}).get('search', [])
            if not results:
                return "No se encontraron resultados relevantes."
            
            snippets = [f"- {res['title']}: {res['snippet']}" for res in results[:3]]
            return "\n".join(snippets).replace('<span class="searchmatch">', '').replace('</span>', '')
    except Exception as e:
        return f"Error en la búsqueda: {str(e)}"