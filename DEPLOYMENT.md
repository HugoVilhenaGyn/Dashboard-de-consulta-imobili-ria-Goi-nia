# Guia de Publicação - Dashboard de Imóveis

## 🌐 Opções de Publicação

### Opção 1: Ngrok (Compartilhamento Rápido - Teste)

**Ideal para:** Testes, demos, compartilhamento temporal

#### 1.1 Instalar Ngrok

**Windows:**
```bash
choco install ngrok
```

**Mac:**
```bash
brew install ngrok
```

**Linux:**
```bash
curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok-v3-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
```

#### 1.2 Configurar Ngrok

1. Criar conta em https://ngrok.com/
2. Copiar seu token de autenticação
3. Executar:
```bash
ngrok authtoken seu-token-aqui
```

#### 1.3 Executar Dashboard com Ngrok

```bash
# Terminal 1 - Iniciar dashboard
python app.py

# Terminal 2 - Executar ngrok
ngrok http 5000
```

**Resultado:** Você receberá uma URL pública como:
```
https://abc123-456-xyz.ngrok.io
```

Qualquer pessoa com acesso a esta URL pode acessar o dashboard!

---

### Opção 2: PythonAnywhere (Hospedagem Gratuita)

**Ideal para:** Produção pequena, sem configuração de servidor

#### 2.1 Criar Conta

1. Ir para https://www.pythonanywhere.com
2. Criar conta gratuita ou pro
3. Confirmar email

#### 2.2 Upload de Arquivos

1. No painel PythonAnywhere, clicar em "Files"
2. Fazer upload dos arquivos:
   - `app.py`
   - `requirements.txt`
   - Pasta `templates/`
   - Arquivo `dashboard.db` (depois de criar)

#### 2.3 Configurar Web App

1. Clicar em "Web" no menu superior
2. Clicar em "Add a new web app"
3. Selecionar "Python 3.10" e "Flask"
4. Seguir as instruções

#### 2.4 Configurar Arquivo WSGI

Na aba "Web", em "WSGI configuration file":

```python
import sys
from dotenv import load_dotenv
import os

path = '/home/seu-usuario/seu-projeto'
if path not in sys.path:
    sys.path.append(path)

load_dotenv(os.path.join(path, '.env'))

from app import app
application = app
```

#### 2.5 Instalar Dependências

No console PythonAnywhere:
```bash
mkvirtualenv --python=/usr/bin/python3.10 myvenv
pip install -r requirements.txt
```

#### 2.6 Acessar Dashboard

Seu dashboard estará em:
```
https://seu-usuario.pythonanywhere.com
```

---

### Opção 3: Heroku (Hospedagem com Dyno Grátis - DEPRECATED)

⚠️ **Nota:** Heroku descontinuou a camada gratuita em 2022. Use PythonAnywhere em vez disso.

---

### Opção 4: DigitalOcean (VPS - Produção Profissional)

**Ideal para:** Produção, múltiplos usuários, controle total

#### 4.1 Criar Droplet

1. Criar conta em https://www.digitalocean.com
2. Criar novo Droplet:
   - OS: Ubuntu 22.04
   - Size: 5$ ou $12/mês
   - Region: Mais próximo aos usuários

#### 4.2 Conectar via SSH

```bash
ssh root@seu-ip-droplet
```

#### 4.3 Atualizar Sistema

```bash
apt update && apt upgrade -y
```

#### 4.4 Instalar Dependências

```bash
apt install -y python3-pip python3-venv nginx supervisor

# Python
python3 -m venv /home/app/venv
source /home/app/venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 4.5 Clonar/Upload Código

```bash
cd /home/app
git clone seu-repo-aqui
# ou fazer upload dos arquivos
```

#### 4.6 Configurar Gunicorn

Criar arquivo `/home/app/gunicorn.conf.py`:

```python
import multiprocessing

bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
max_requests = 1000
timeout = 30
```

#### 4.7 Configurar Supervisor

Criar arquivo `/etc/supervisor/conf.d/dashboard.conf`:

```ini
[program:dashboard]
directory=/home/app
command=/home/app/venv/bin/gunicorn -c gunicorn.conf.py app:app
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/dashboard.log
environment=SUPABASE_KEY="sua-chave-aqui"
```

Executar:
```bash
supervisorctl reread
supervisorctl update
supervisorctl start dashboard
```

#### 4.8 Configurar Nginx

Criar arquivo `/etc/nginx/sites-available/dashboard`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/app/static/;
    }
}
```

Ativar:
```bash
ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 4.9 Configurar SSL com Let's Encrypt

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d seu-dominio.com
```

#### 4.10 Acessar Dashboard

```
https://seu-dominio.com
```

---

### Opção 5: AWS Lightsail (Hospedagem em Nuvem)

**Similar ao DigitalOcean, com passos semelhantes.**

1. Criar Lightsail instance
2. Seguir passos 4.2 a 4.9 acima

---

## 📋 Comparação de Opções

| Opção | Custo | Setup | Limite | SSL | Melhor Para |
|-------|-------|-------|--------|-----|-------------|
| Ngrok | Gratuito | <5min | 40 req/min | ✅ | Demos |
| PythonAnywhere | Gratuito/$5/mês | 15min | 100MB | ✅ | Pequeno |
| Heroku | N/A | N/A | N/A | N/A | DEPRECATED |
| DigitalOcean | $5-12/mês | 30min | Ilimitado | ✅ | Produção |
| AWS | $3-20/mês | 30min | Ilimitado | ✅ | Produção |

---

## 🔒 Segurança em Produção

### Antes de Publicar:

1. **Alterar Senha Admin**
   - Login com admin/admin123
   - Criar novo usuário admin com senha forte
   - Desativar usuário "admin" padrão

2. **Configurar HTTPS**
   - Usar certificado SSL válido
   - Redirecionar HTTP → HTTPS

3. **Variáveis de Ambiente**
   - Nunca expor `SUPABASE_KEY` no código
   - Usar arquivo `.env` (não commitado no git)

4. **Firewall**
   - Configurar firewall do VPS
   - Apenas portas 80/443 abertas

5. **Backup**
   - Fazer backup do `dashboard.db` regularmente
   - Usar versão controle para código

6. **Rate Limiting**
   - Implementar limitador de taxa (rate limit)
   - Proteger contra brute force

---

## 🚀 Deploy Automático (GitHub Actions)

Arquivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy to DigitalOcean

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to VPS
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/app
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          supervisorctl restart dashboard
```

---

## 🔧 Comandos Úteis

```bash
# Verificar logs Nginx
tail -f /var/log/nginx/error.log

# Verificar logs Supervisor
tail -f /var/log/dashboard.log

# Reiniciar serviços
supervisorctl restart dashboard
systemctl restart nginx

# Verificar status
supervisorctl status
systemctl status nginx

# Conectar ao banco de dados
sqlite3 dashboard.db
```

---

## 📞 Troubleshooting de Deployment

### "502 Bad Gateway"
- Verificar se Gunicorn está rodando: `supervisorctl status`
- Verificar logs: `tail -f /var/log/dashboard.log`

### "Connection refused"
- Verificar firewall: `ufw status`
- Adicionar regra: `ufw allow 80` e `ufw allow 443`

### "SSL certificate error"
- Renovar cert: `certbot renew`
- Verificar data: `certbot certificates`

### Dashboard lento
- Aumentar workers Gunicorn
- Implementar cache (Redis)
- Otimizar queries Supabase

---

**Sucesso no deploy!** 🎉
