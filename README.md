# Dashboard de Imóveis - Documentação

## 🚀 Quick Start

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Configurar Variável de Ambiente

```bash
# Windows PowerShell
$env:SUPABASE_KEY="sua_chave_jwt_aqui"

# Windows CMD
set SUPABASE_KEY=sua_chave_jwt_aqui

# Linux/Mac
export SUPABASE_KEY="sua_chave_jwt_aqui"
```

### Iniciar o Servidor

```bash
python app.py
```

O dashboard estará disponível em: **http://localhost:5000**

---

## 🔐 Credenciais Padrão

- **Usuário:** admin
- **Senha:** admin123

⚠️ **Altere a senha do admin imediatamente após o primeiro login!**

---

## 👤 Funções de Usuário

### 1. **Visualizador (Viewer)**
- ✅ Consultar dados
- ✅ Aplicar filtros
- ❌ Exportar (PDF/CSV)
- ❌ Gerenciar usuários

### 2. **Editor**
- ✅ Consultar dados
- ✅ Aplicar filtros
- ✅ Exportar (PDF/CSV)
- ❌ Gerenciar usuários

### 3. **Administrador (Admin)**
- ✅ Consultar dados
- ✅ Aplicar filtros
- ✅ Exportar (PDF/CSV)
- ✅ Gerenciar usuários
- ✅ Criar/editar/desativar usuários
- ✅ Configurar permissões

---

## 🔍 Recursos do Dashboard

### Consultar Dados

**Filtros Disponíveis:**

1. **Propriedade (Wakbueno)**
   - Filtrar por código da propriedade
   - Ex: `Wakbueno PA001`

2. **Setor**
   - Filtrar por setor de localização
   - Suporta busca parcial (contains)

3. **Número de Quartos**
   - Filtrar por quantidade exata de quartos
   - Ex: `3` para propriedades com 3 quartos

4. **Proprietário**
   - Filtrar por nome do proprietário
   - Suporta busca parcial

5. **Registros por Página**
   - 100, 500, 1000 ou 5000 registros
   - Limitado pela permissão do usuário

### Exportar Dados

#### 📄 Exportar em PDF
- Cria relatório formatado
- Inclui título, filtros aplicados e timestamp
- Máximo 500 registros por PDF
- Ideal para impressão

#### 📊 Exportar em CSV
- Formato compatível com Excel
- Todos os registros carregados
- Ideal para análise em planilha

### Gerenciar Usuários (Admin Only)

**Criar Novo Usuário:**
1. Clique em "+ Novo Usuário"
2. Preencha dados:
   - Nome de usuário (único)
   - Email
   - Senha
   - Função
3. Clique em "Criar Usuário"

**Desativar Usuário:**
- Clique no botão "Desativar" na linha do usuário
- O usuário não poderá mais fazer login

---

## 📊 Estatísticas

O dashboard mostra:
- **Total de Registros:** Quantidade de registros na tabela
- **Registros Carregados:** Quantidade de registros exibidos com filtros atuais

---

## 🗂️ Estrutura de Arquivos

```
/
├── app.py                    # Backend Flask
├── requirements.txt          # Dependências Python
├── dashboard.db             # Banco de dados SQLite (local)
├── templates/
│   └── dashboard.html       # Frontend (interface web)
├── log_upload.txt           # Log de uploads
└── README.md               # Este arquivo
```

---

## 🔒 Segurança

### Autenticação
- Senhas são hash-ificadas com SHA-256
- Sessões gerenciadas pelo Flask
- Tokens JWT do Supabase para API

### Permissões
- Controle de acesso baseado em funções (RBAC)
- Cada usuário tem permissões específicas
- Limites de registros por função

### Dados
- Conexão segura com Supabase via REST API
- Validação de entrada em todos os filtros
- Proteção contra SQL injection

---

## 🌐 Publicar em Domínio

### Opção 1: Usando Ngrok (Quick Demo)

```bash
# Instalar ngrok
choco install ngrok  # Windows
# ou
brew install ngrok   # Mac

# Criar conta em https://ngrok.com

# Executar
ngrok http 5000
```

Ngrok fornecerá uma URL pública como: `https://xxxx-xx-xxxx-xxxx-xx.ngrok.io`

### Opção 2: Usando PythonAnywhere

1. Criar conta em https://www.pythonanywhere.com
2. Upload dos arquivos
3. Configurar web app
4. Usar domínio fornecido: `seu-usuario.pythonanywhere.com`

### Opção 3: Servidor VPS (Produção)

```bash
# 1. Instalar dependências no VPS
pip install -r requirements.txt
pip install gunicorn

# 2. Executar com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.py

# 3. Usar Nginx como reverse proxy
# 4. Configurar SSL com Let's Encrypt
```

---

## 🐛 Troubleshooting

### "Invalid API key"
- Verifique se a variável `SUPABASE_KEY` está definida
- Confirme que é um token JWT válido com role `service_role`
- Gere um novo token em Supabase Settings → API

### "Could not connect to Supabase"
- Verifique a URL do Supabase
- Confirme a conexão de internet
- Cheque se a tabela `imoveis` existe

### Usuário bloqueado após múltiplas tentativas
- Atualmente não há limite de tentativas
- Implemente rate limiting em produção

### Dados não aparecem após filtros
- Verifique se os valores dos filtros existem
- Tente com um único filtro por vez
- Aumente o limite de registros

---

## 📈 Performance

### Otimizações Recomendadas

1. **Cache de Dados**
   ```javascript
   // Adicionar cache local de 5 minutos
   ```

2. **Paginação**
   - Implementar paginação em vez de carregar todos os dados

3. **Índices no Supabase**
   - Criar índices nas colunas de filtro

4. **Compressão**
   - Ativar gzip no Flask

---

## 🚀 Roadmap

- [ ] Autenticação 2FA
- [ ] Exportação em Excel com gráficos
- [ ] Dashboard com KPIs
- [ ] Busca full-text
- [ ] Histórico de alterações
- [ ] Backup automático
- [ ] Mobile app
- [ ] Integração com Zapier

---

## 📞 Suporte

Para problemas ou sugestões, entre em contato:
- Email: admin@imoveis.local
- Documentação Supabase: https://supabase.io/docs

---

## 📄 Licença

Este projeto é fornecido como está para uso interno.

---

**Versão:** 1.0.0  
**Última atualização:** Maio 2026
