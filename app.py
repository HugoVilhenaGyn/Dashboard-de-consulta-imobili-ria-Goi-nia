from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
from supabase import create_client
import sqlite3
import json
import os
from datetime import datetime
from functools import wraps
import io
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import hashlib
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Supabase config
SUPABASE_URL = "https://mquuvzrwrimrlpgjdnjv.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# SQLite for local user/permission management
DB_PATH = "dashboard.db"

def init_db():
    """Inicializar banco de dados de usuários"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        email TEXT,
        role TEXT DEFAULT 'viewer',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT 1
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY,
        role TEXT UNIQUE,
        can_view BOOLEAN DEFAULT 1,
        can_export BOOLEAN DEFAULT 0,
        can_manage_users BOOLEAN DEFAULT 0,
        max_records INTEGER DEFAULT 10000
    )''')
    
    # Permissões padrão
    c.execute('''INSERT OR IGNORE INTO permissions 
                 (role, can_view, can_export, can_manage_users, max_records) 
                 VALUES (?, ?, ?, ?, ?)''',
              ('admin', True, True, True, -1))
    c.execute('''INSERT OR IGNORE INTO permissions 
                 (role, can_view, can_export, can_manage_users, max_records) 
                 VALUES (?, ?, ?, ?, ?)''',
              ('editor', True, True, False, 50000))
    c.execute('''INSERT OR IGNORE INTO permissions 
                 (role, can_view, can_export, can_manage_users, max_records) 
                 VALUES (?, ?, ?, ?, ?)''',
              ('viewer', True, False, False, 10000))
    
    # Usuário admin padrão (senha: admin123)
    admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
    c.execute('''INSERT OR IGNORE INTO users (username, password_hash, email, role)
                 VALUES (?, ?, ?, ?)''',
              ('admin', admin_hash, 'admin@imoveis.local', 'admin'))
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_permissions(username):
    """Obter permissões do usuário"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''SELECT users.role, permissions.* 
                 FROM users 
                 JOIN permissions ON users.role = permissions.role 
                 WHERE users.username = ?''', (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            'role': result[0],
            'can_view': bool(result[2]),
            'can_export': bool(result[3]),
            'can_manage_users': bool(result[4]),
            'max_records': result[5]
        }
    return None

def require_login(f):
    """Decorator para exigir login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Não autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_permission(permission):
    """Decorator para verificar permissões"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return jsonify({'error': 'Não autenticado'}), 401
            
            perms = get_user_permissions(session['username'])
            if not perms or not perms.get(permission):
                return jsonify({'error': 'Permissão negada'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    # dashboard.html already contains the login UI and logic
    username = session.get('username')
    return render_template('dashboard.html', username=username)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Usuário e senha obrigatórios'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT id, password_hash, active, role FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if not user or user[2] == 0:
        return jsonify({'error': 'Usuário ou senha inválidos'}), 401
    
    if hash_password(password) != user[1]:
        return jsonify({'error': 'Usuário ou senha inválidos'}), 401
    
    session['username'] = username
    session['role'] = user[3]
    
    return jsonify({'success': True, 'role': user[3]})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/change-password', methods=['POST'])
@require_login
def change_password():
    data = request.json
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')

    if not current_password or not new_password:
        return jsonify({'error': 'Preencha todos os campos'}), 400

    if len(new_password) < 6:
        return jsonify({'error': 'Nova senha deve ter pelo menos 6 caracteres'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT password_hash FROM users WHERE username = ?', (session['username'],))
    user = c.fetchone()

    if not user or hash_password(current_password) != user[0]:
        conn.close()
        return jsonify({'error': 'Senha atual incorreta'}), 401

    c.execute('UPDATE users SET password_hash = ? WHERE username = ?',
              (hash_password(new_password), session['username']))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Senha alterada com sucesso'})

@app.route('/api/me', methods=['GET'])
@require_login
def get_me():
    perms = get_user_permissions(session['username'])
    return jsonify({
        'username': session['username'],
        'role': session.get('role'),
        'permissions': perms
    })

@app.route('/api/dados', methods=['GET'])
@require_login
def get_dados():
    """Consultar dados com filtros"""
    try:
        # Parâmetros de filtro
        wakbueno = request.args.get('wakbueno', '')
        setor = request.args.get('setor', '')
        quartos = request.args.get('quartos', '')
        proprietario = request.args.get('proprietario', '')
        tipo = request.args.get('tipo', '')
        edificio = request.args.get('edificio', '')
        limit = request.args.get('limit', 100, type=int)
        
        perms = get_user_permissions(session['username'])
        if perms['max_records'] > 0:
            limit = min(limit, perms['max_records'])
        
        # Construir query - Selecionar as colunas reais do banco
        query = supabase.table('imoveis').select('id,InscricaoCadastral,nomeBairro,uso,nomeEdificio,numeroGaragem,NomeContribuinte,ValorVenal,observacao,Endereco')
        
        if wakbueno:
            query = query.eq('InscricaoCadastral', wakbueno)
        if setor:
            query = query.ilike('nomeBairro', f'%{setor}%')
        if quartos:
            query = query.eq('numeroGaragem', int(quartos))
        if proprietario:
            query = query.ilike('NomeContribuinte', f'%{proprietario}%')
        if tipo:
            query = query.eq('uso', tipo)
        if edificio:
            query = query.ilike('nomeEdificio', f'%{edificio}%')
        
        result = query.limit(limit).execute()
        
        # Formatar os dados de volta para os nomes amigáveis que o frontend espera
        formatted_data = []
        for r in result.data:
            formatted_data.append({
                'id': r.get('id'),
                'wakbueno': r.get('InscricaoCadastral'),
                'setor': r.get('nomeBairro'),
                'tipo': r.get('uso'),
                'edificio': r.get('nomeEdificio'),
                'numeroQuartos': r.get('numeroGaragem'),
                'proprietario': r.get('NomeContribuinte'),
                'preco': r.get('ValorVenal'),
                'descricao': r.get('observacao'),
                'endereco': r.get('Endereco')
            })
        
        return jsonify({
            'data': formatted_data,
            'count': len(formatted_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/valores-unicos', methods=['GET'])
@require_login
def get_valores_unicos():
    """Obter valores únicos para filtros - Otimizado com limit para melhor performance"""
    try:
        column = request.args.get('column', 'setor')
        
        # Mapeamento para valores únicos
        col_map = {
            'wakbueno': 'InscricaoCadastral',
            'setor': 'nomeBairro',
            'tipo': 'uso',
            'edificio': 'nomeEdificio',
            'proprietario': 'NomeContribuinte'
        }
        db_column = col_map.get(column, column)
        
        # Limitar a 1000 registros para melhor performance
        result = supabase.table('imoveis').select(db_column).limit(1000).execute()
        
        valores = list(set([r[db_column] for r in result.data if r.get(db_column)]))
        valores.sort()
        
        return jsonify({'valores': valores[:100]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios', methods=['GET'])
@require_permission('can_manage_users')
def list_usuarios():
    """Listar usuários"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT id, username, email, role, active, created_at FROM users ORDER BY created_at DESC')
    usuarios = []
    for row in c.fetchall():
        usuarios.append({
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'role': row[3],
            'active': bool(row[4]),
            'created_at': row[5]
        })
    
    conn.close()
    return jsonify(usuarios)

@app.route('/api/usuarios', methods=['POST'])
@require_permission('can_manage_users')
def create_usuario():
    """Criar novo usuário"""
    data = request.json
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    role = data.get('role', 'viewer')
    
    if not username or not password:
        return jsonify({'error': 'Usuário e senha obrigatórios'}), 400
    
    if role not in ['admin', 'editor', 'viewer']:
        return jsonify({'error': 'Role inválida'}), 400
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                  (username, email, hash_password(password), role))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Usuário {username} criado'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Usuário já existe'}), 409

@app.route('/api/usuarios/<int:user_id>', methods=['PUT'])
@require_permission('can_manage_users')
def update_usuario(user_id):
    """Atualizar usuário"""
    data = request.json
    role = data.get('role')
    active = data.get('active')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if role:
        c.execute('UPDATE users SET role = ? WHERE id = ?', (role, user_id))
    if active is not None:
        c.execute('UPDATE users SET active = ? WHERE id = ?', (int(active), user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/usuarios/<int:user_id>', methods=['DELETE'])
@require_permission('can_manage_users')
def delete_usuario(user_id):
    """Desativar usuário"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('UPDATE users SET active = 0 WHERE id = ?', (user_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/export/pdf', methods=['POST'])
@require_permission('can_export')
def export_pdf():
    """Exportar dados em PDF"""
    try:
        data = request.json
        records = data.get('records', [])
        filters = data.get('filters', {})
        
        if not records:
            return jsonify({'error': 'Sem dados para exportar'}), 400
        
        # Criar PDF
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=landscape(letter),
                                topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=12
        )
        
        title = f"Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        elements.append(Paragraph(title, title_style))
        
        # Filtros aplicados
        if filters:
            filter_text = "Filtros: " + ", ".join([f"{k}={v}" for k, v in filters.items() if v])
            elements.append(Paragraph(filter_text, styles['Normal']))
        
        elements.append(Spacer(1, 12))
        
        # Tabela
        if records:
            columns = list(records[0].keys())
            data_table = [columns]
            
            for record in records[:500]:  # Limitar a 500 linhas por PDF
                row = [str(record.get(col, ''))[:30] for col in columns]
                data_table.append(row)
            
            table = Table(data_table, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ]))
            
            elements.append(table)
        
        # Rodapé
        elements.append(Spacer(1, 12))
        footer_text = f"Total de registros: {len(records)} | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        elements.append(Paragraph(footer_text, styles['Normal']))
        
        doc.build(elements)
        output.seek(0)
        
        return send_file(output, mimetype='application/pdf',
                        as_attachment=True,
                        download_name=f"imoveis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/csv', methods=['POST'])
@require_permission('can_export')
def export_csv():
    """Exportar dados em CSV"""
    try:
        data = request.json
        records = data.get('records', [])
        
        if not records:
            return jsonify({'error': 'Sem dados para exportar'}), 400
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
        
        output.seek(0)
        
        return send_file(io.BytesIO(output.getvalue().encode()),
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f"imoveis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
