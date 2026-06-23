import requests as req
import io
import openpyxl
from flask import request, jsonify, render_template, session, send_file
from google import genai as gg

SB_URL = "https://mquuvzrwrimrlpgjdnjv.supabase.co"
SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAwNzMwMTIsImV4cCI6MjA5NTY0OTAxMn0.P0AJ-H5rjpoQTmYIrUxMA6t6oWNK2ljvshey3MjpIW4"
GEMINI_KEY = open("/tmp/keys.txt").read().splitlines()[1].strip()

STOP = {"ME","TRAGA","OS","AS","DO","DA","DE","NO","NA","EM","E","A","O","UM","UMA","QUE","COM","POR","PARA","QUANTOS","QUANTAS","LISTA","LISTAR","BOXES","GARAGENS","UNIDADES","TOTAL","QUAIS","TEM","HA","SAO","QUAL","NOME","EDIFICIO","CONDOMINIO","IMOVEL","IMOVEIS","CPF","CNPJ","PROPRIETARIOS","PROPRIETARIO","APARTAMENTOS","EXPORTE","EXPORTAR","DADOS","TODOS","TODAS","EXCEL","PLANILHA","LISTE","MOSTRE","NAO","SIM","FOI","QUE","PERGUNTEI","QUERO","SOMENTE","APENAS"}

def s(v): return str(v or "").strip()

def buscar_todos(palavra, h):
    todos = []
    offset = 0
    while True:
        url = SB_URL + "/rest/v1/imoveis?select=nomeEdificio,NomeContribuinte,CPF_CNPJ,incompl,nomeBairro&nomeEdificio=ilike." + palavra + "*&limit=500&offset=" + str(offset)
        r = req.get(url, headers=h, timeout=15)
        batch = r.json() if isinstance(r.json(), list) else []
        if not batch: break
        todos.extend(batch)
        if len(batch) < 500: break
        offset += 500
    return todos

def is_apt(v): return s(v).upper().startswith("AP")
def is_sala(v): return s(v).upper().startswith("SALA") or s(v).upper().startswith("LOJA") or s(v).upper().startswith("COMER")
def is_box(v): return s(v).upper().startswith("BOX") or s(v).upper().startswith("SS") or s(v).upper().startswith("ESC") or s(v).upper().startswith("DEP") or s(v).upper().startswith("GAR")

def processar(dados_ed):
    apts = [i for i in dados_ed if is_apt(i.get("incompl"))]
    salas = [i for i in dados_ed if is_sala(i.get("incompl"))]
    boxes = [i for i in dados_ed if is_box(i.get("incompl"))]
    nomes_ed = sorted(set(s(i.get("nomeEdificio")) for i in dados_ed if i.get("nomeEdificio")))
    bairros = sorted(set(s(i.get("nomeBairro")) for i in dados_ed if i.get("nomeBairro")))
    props_unicos = {}
    for i in dados_ed:
        cpf = s(i.get("CPF_CNPJ"))
        if cpf and cpf not in props_unicos:
            props_unicos[cpf] = s(i.get("NomeContribuinte"))
    return apts, salas, boxes, nomes_ed, bairros, props_unicos

def register_lisa(app):
    @app.route("/assistente")
    def assistente():
        session.pop("ultimo_edificio", None)
        return render_template("assistente.html")

    @app.route("/api/assistente/nova", methods=["POST"])
    def nova_consulta():
        session.pop("ultimo_edificio", None)
        return jsonify({"ok": True})

    @app.route("/api/assistente/exportar", methods=["GET"])
    def exportar_excel():
        edificio = request.args.get("edificio", session.get("ultimo_edificio",""))
        filtro = request.args.get("filtro", "todos")
        if not edificio:
            return jsonify({"error": "Sem edificio"}), 400
        h = {"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY}
        dados = buscar_todos(edificio, h)
        if filtro == "apts":
            dados = [i for i in dados if is_apt(i.get("incompl"))]
        elif filtro == "salas":
            dados = [i for i in dados if is_sala(i.get("incompl"))]
        elif filtro == "boxes":
            dados = [i for i in dados if is_box(i.get("incompl"))]
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Dados"
        ws.append(["Edificio", "Bairro", "Unidade", "Proprietario", "CPF/CNPJ"])
        for i in dados:
            ws.append([s(i.get("nomeEdificio")), s(i.get("nomeBairro")), s(i.get("incompl")), s(i.get("NomeContribuinte")), s(i.get("CPF_CNPJ"))])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        nome = edificio.replace(" ","_") + "_" + filtro + ".xlsx"
        return send_file(buf, as_attachment=True, download_name=nome, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    @app.route("/api/assistente", methods=["POST"])
    def api_assistente():
        data = request.get_json()
        pergunta = data.get("pergunta", "").strip()
        if not pergunta:
            return jsonify({"error": "Pergunta vazia"}), 400
        h = {"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY}
        ctx = ""
        edificio_atual = ""
        try:
            palavras = [p for p in pergunta.upper().split() if p not in STOP and len(p) > 2]
            dados_ed = []
            for palavra in palavras:
                resultado = buscar_todos(palavra, h)
                if resultado:
                    dados_ed = resultado
                    edificio_atual = palavra
                    session["ultimo_edificio"] = palavra
                    break
            if not dados_ed and session.get("ultimo_edificio"):
                dados_ed = buscar_todos(session["ultimo_edificio"], h)
                edificio_atual = session["ultimo_edificio"]
            if dados_ed:
                apts, salas, boxes, nomes_ed, bairros, props_unicos = processar(dados_ed)
                ctx = "EDIFICIO: " + str(nomes_ed) + ". BAIRRO: " + str(bairros) + ". TOTAL: " + str(len(dados_ed)) + ". APARTAMENTOS: " + str(len(apts)) + ". SALAS/LOJAS: " + str(len(salas)) + ". BOXES/GARAGENS: " + str(len(boxes)) + ". PROPRIETARIOS UNICOS: " + str(len(props_unicos)) + ". AMOSTRA APTS (max 30): " + str([{"unidade":s(i.get("incompl")),"prop":s(i.get("NomeContribuinte")),"cpf":s(i.get("CPF_CNPJ"))} for i in apts[:30]])
            else:
                ctx = "Nenhum edificio encontrado para: " + str(palavras)
        except Exception as e:
            ctx = "Erro: " + str(e)
        try:
            gc = gg.Client(api_key=GEMINI_KEY)
            prompt = "Voce e Lisa, assistente de dados da BrokerImob Goiania. Inteligente, direta, descontraida. Regras: portugues brasileiro, sem emojis, sem Prezado, sem Atenciosamente, sem assinar nome. Responda APENAS com base nos dados abaixo. NUNCA invente dados. Para listas use tabela: Unidade | Proprietario | CPF.\n\nDADOS:\n" + ctx + "\n\nPERGUNTA: " + pergunta
            resp = gc.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            return jsonify({"resposta": resp.text, "edificio": edificio_atual or session.get("ultimo_edificio","")})
        except Exception as e:
            return jsonify({"resposta": ctx + "\nErro Gemini: " + str(e), "edificio": edificio_atual})


def register_upload_log(app):
    import requests as req
    from flask import request, jsonify

    SB_URL = "https://mquuvzrwrimrlpgjdnjv.supabase.co"

    def get_key():
        return open('/tmp/keys.txt').read().strip().split('\n')[0]

    @app.route("/api/upload_log", methods=["POST"])
    def salvar_upload_log():
        data = request.get_json()
        key = get_key()
        h = {"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json"}
        payload = {
            "nome_arquivo": data.get("nome_arquivo", ""),
            "registros": data.get("registros", 0),
            "condominios": data.get("condominios", []),
            "usuario": data.get("usuario", "sistema")
        }
        r = req.post(SB_URL + "/rest/v1/upload_log", headers=h, json=payload)
        return jsonify({"ok": r.status_code in (200, 201)})

    @app.route("/api/upload_log", methods=["GET"])
    def listar_upload_log():
        key = get_key()
        h = {"apikey": key, "Authorization": "Bearer " + key}
        r = req.get(SB_URL + "/rest/v1/upload_log?order=enviado_em.desc&limit=100", headers=h)
        return jsonify(r.json() if isinstance(r.json(), list) else [])

    @app.route("/historico")
    def historico():
        from flask import render_template
        return render_template("historico.html")
