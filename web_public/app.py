from flask import Flask, request, jsonify, render_template
from datetime import datetime
import markdown

app = Flask(__name__)

newsletters = []

@app.route('/')
def home():
    return render_template('index.html', newsletters=newsletters)

@app.route('/api/publish', methods=['POST'])
def publish():
    data = request.json
    content_md = data.get('content', '')
    post_type = data.get('post_type', 'Newsletter') # Por defecto Newsletter si falla
    
    content_html = markdown.markdown(content_md)
    
    new_post = {
        "id": len(newsletters) + 1,
        "type": post_type, # Guardamos el tipo de publicación
        "content": content_html,
        "date": datetime.now().strftime("%d %b %Y, %H:%M"),
        "author": "GDG AI Editor"
    }
    
    newsletters.insert(0, new_post)
    return jsonify({"status": "success", "message": "Published!", "post": new_post}), 200


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
