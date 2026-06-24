from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
import requests, json, os, csv, io
from functools import wraps

app = Flask(__name__)
app.secret_key = "brokerimobai2025xK9mNpQr"
CORS(app)

ACCESS_PASSWORD = "robo2025"
SB_URL = open("/tmp/keys.txt").read().splitlines()[2].strip()
SB_KEY = open("/tmp/keys.txt").read().splitlines()[0].strip()

def sb_headers():
    return {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("autenticado"):
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/check_session")
def check_session():
    return jsonify({"ok": bool(session.get("autenticado"))})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("password") == ACCESS_PASSWORD:
        session["autenticado"] = True
        return jsonify({"ok": True})
    return jsonify({"error": "Senha incorreta"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})

@app.route("/api/imoveis")
@require_login
def imoveis():
    params = request.query_string.decode()
    r = requests.get(f"{SB_URL}/rest/v1/imoveis?{params}", headers=sb_headers())
    return jsonify(r.json())

@app.route("/api/upload_log", methods=["GET"])
@require_login
def listar_upload_log():
    r = requests.get(f"{SB_URL}/rest/v1/upload_log?order=enviado_em.desc&limit=100", headers=sb_headers())
    return jsonify(r.json() if isinstance(r.json(), list) else [])

@app.route("/api/upload_log", methods=["POST"])
@require_login
def salvar_upload_log():
    data = request.get_json()
    h = {**sb_headers(), "Prefer": "return=minimal"}
    r = requests.post(f"{SB_URL}/rest/v1/upload_log", headers=h, json=data)
    return jsonify({"ok": r.status_code in (200, 201)})

@app.route("/historico")
@require_login
def historico():
    return render_template("historico.html")

from lisa import register_lisa
register_lisa(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
