from flask import Flask, request, jsonify, render_template
from datetime import datetime
import markdown

app = Flask(__name__)

# Memoria volátil (lista simple)
newsletters = []

@app.route('/')
def home():
    return render_template('index.html', newsletters=newsletters)

@app.route('/api/publish', methods=['POST'])
def publish():
    data = request.json
    content_md = data.get('content', '')
    
    # Convertimos Markdown a HTML para que se vea bonito
    content_html = markdown.markdown(content_md)
    
    new_post = {
        "id": len(newsletters) + 1,
        "content": content_html, # Guardamos el HTML renderizado
        "date": datetime.now().strftime("%d %b %Y, %H:%M"),
        "author": "GDG AI Editor"
    }
    
    # Insertamos al principio para que salga la primera
    newsletters.insert(0, new_post)
    return jsonify({"status": "success", "message": "Published!"}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
