from flask import Flask, Response, request
import requests
import os

app = Flask(__name__)

# Новый URL ChatKit — не заблокирован в РФ
CHATKIT_URL = "https://cdn.oaistatic.com/assets/chat/chat.js"

@app.route("/chatkit.js")
def chatkit_proxy():
    """Проксируем ChatKit JS через Render"""
    try:
        r = requests.get(CHATKIT_URL, timeout=10)
        if r.status_code != 200:
            return Response(f"// Ошибка: статус {r.status_code}", mimetype="application/javascript")

        resp = Response(r.content, mimetype="application/javascript")
        resp.headers["Cache-Control"] = "no-cache"
        return resp

    except Exception as e:
        return Response(f"// Ошибка запроса: {e}", mimetype="application/javascript")

@app.route("/")
def index():
    """Тестовая страница"""
    return """
    <html>
      <head><meta charset='UTF-8'><title>Buildeco Chat</title></head>
      <body style='height:100vh;display:flex;align-items:center;justify-content:center;'>
        <script src='/chatkit.js'
          data-workflow='wf_695907dc48308190b1541b47d9b71a0e0c3ff92ed5dbce97'
          data-version='2'
          data-theme='light'>
        </script>
      </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
