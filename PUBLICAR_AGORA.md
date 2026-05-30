# 🚀 PUBLICAR DASHBOARD - Guia Rápido

## 📌 Status Atual

- ✅ Dashboard criado em `c:\VS Code\upload_supabase.py\app.py`
- ✅ Integrado com Supabase (mesmo banco de 196 arquivos)
- ✅ Dependências sendo instaladas...
- ⏳ Próxima: Publicar online

---

## ⚡ Opção 1: Ngrok (TESTE RÁPIDO - Recomendado)

### 1️⃣ Download Ngrok

**Windows:**
```bash
choco install ngrok
```

**Se não tem Chocolatey:**
- Baixar em https://ngrok.com/download
- Descompactar em `C:\ngrok`
- Adicionar ao PATH

### 2️⃣ Configurar Ngrok

```bash
# 1. Criar conta em https://ngrok.com
# 2. Copiar seu token

# 3. No terminal, executar:
ngrok authtoken seu-token-aqui
```

### 3️⃣ Executar Dashboard + Ngrok

**Terminal 1 - Dashboard:**
```bash
cd "c:\VS Code\upload_supabase.py"
$env:SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDA3MzAxMiwiZXhwIjoyMDk1NjQ5MDEyfQ.G4n25w9oKKI9wvoMVimpUFfV-n1QTFPFrOtnGqsC-JM"
python app.py
```

**Terminal 2 - Ngrok:**
```bash
ngrok http 5000
```

### 4️⃣ Resultado

Você verá algo como:
```
┌─────────────────────────────────────────────────┐
│ Session Status                        online    │
├─────────────────────────────────────────────────┤
│ Account                          seu@email.com  │
│ Version                                 3.3.0   │
│ Region                              United     │
├─────────────────────────────────────────────────┤
│ Forwarding    https://abc123-456-xyz.ngrok.io   │
│               http://abc123-456-xyz.ngrok.io    │
└─────────────────────────────────────────────────┘
```

### 5️⃣ Compartilhar

Copie a URL e envie:
```
https://abc123-456-xyz.ngrok.io
```

Login: `admin` / `admin123`

✅ **Qualquer pessoa com a URL consegue acessar o dashboard!**

---

## 🌍 Opção 2: PythonAnywhere (PRODUCTION - Fácil)

### 1️⃣ Criar Conta

- Ir para https://www.pythonanywhere.com
- Criar conta gratuita

### 2️⃣ Upload Arquivos

1. No painel, clicar em "Files"
2. Fazer upload:
   - `app.py`
   - `requirements.txt`
   - Pasta `templates/` (com `dashboard.html`)

### 3️⃣ Criar Web App

1. Clicar em "Web" → "Add a new web app"
2. Escolher "Manual configuration" → "Python 3.10"
3. Configurar WSGI:

```python
import os
os.environ['SUPABASE_KEY'] = 'sua-chave-aqui'
from app import app as application
```

### 4️⃣ Instalar Dependências

No console:
```bash
pip install flask flask-cors supabase reportlab
```

### 5️⃣ Acessar

```
https://seu-usuario.pythonanywhere.com
```

✅ **Dashboard rodando 24/7 no seu domínio próprio!**

---

## 📊 Comparação Rápida

| Método | Tempo | Custo | Permanente | Melhor Para |
|--------|-------|-------|-----------|-------------|
| Ngrok | 2 min | Grátis | 2h | Testes/Demos |
| PythonAnywhere | 15 min | Grátis/$5 | Sim | Produção |
| DigitalOcean | 30 min | $5-12/mês | Sim | Escala |

---

## ✅ Checklist

- [ ] Dashboard instalado localmente (`c:\VS Code\upload_supabase.py`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Supabase configurado com chave válida
- [ ] Banco de dados `dashboard.db` criado
- [ ] Dashboard rodando em `localhost:5000`
- [ ] Login funcionando (admin/admin123)
- [ ] Filtros retornando dados do Supabase
- [ ] Exportação PDF/CSV funcionando
- [ ] Usuários conseguem ser criados
- [ ] Publicado com Ngrok ou PythonAnywhere ✅

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Erro: "Invalid API key"
- Confirme a chave `SUPABASE_KEY` está correta
- Deve ter `role: service_role` no JWT

### Dashboard lento
- Aumentar limite de registros em PythonAnywhere
- Implementar cache (Redis)

### Ngrok expira/para
- Remontá-lo com mesmo comando
- URL muda automaticamente

---

## 📞 Próximas Ações

1. **Agora:** Instalar dependências (`pip install -r requirements.txt`)
2. **Depois:** Rodar dashboard (`python app.py`)
3. **Depois:** Publicar com Ngrok ou PythonAnywhere
4. **Depois:** Compartilhar URL com equipe

---

**Versão:** 1.0.0  
**Data:** Maio 2026  
**Status:** 🟢 PRONTO PARA PUBLICAÇÃO
