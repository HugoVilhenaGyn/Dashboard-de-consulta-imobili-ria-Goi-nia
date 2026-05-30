# 🚀 GUIA RÁPIDO - Dashboard de Imóveis

## ⚡ 5 Minutos para Começar

### 1️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar Chave Supabase

**Windows PowerShell:**
```powershell
$env:SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDA3MzAxMiwiZXhwIjoyMDk1NjQ5MDEyfQ.G4n25w9oKKI9wvoMVimpUFfV-n1QTFPFrOtnGqsC-JM"
```

**Windows CMD:**
```cmd
set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDA3MzAxMiwiZXhwIjoyMDk1NjQ5MDEyfQ.G4n25w9oKKI9wvoMVimpUFfV-n1QTFPFrOtnGqsC-JM
```

**Linux/Mac:**
```bash
export SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDA3MzAxMiwiZXhwIjoyMDk1NjQ5MDEyfQ.G4n25w9oKKI9wvoMVimpUFfV-n1QTFPFrOtnGqsC-JM"
```

### 3️⃣ Iniciar Dashboard

**Windows:**
```bash
python app.py
```

**Linux/Mac:**
```bash
python3 app.py
```

### 4️⃣ Acessar no Navegador

```
http://localhost:5000
```

### 5️⃣ Fazer Login

- **Usuário:** admin
- **Senha:** admin123

✅ **Pronto! Dashboard rodando!**

---

## 📋 Funcionalidades

### ✨ Consultar Dados

1. Use os filtros para encontrar imóveis:
   - **Wakbueno:** Código da propriedade
   - **Setor:** Localização
   - **Quartos:** Número de quartos
   - **Proprietário:** Nome do dono

2. Clique em **"Buscar"** para aplicar filtros

3. Visualize resultados na tabela

### 📤 Exportar Dados

1. Selecione os dados desejados com filtros
2. Clique em:
   - **"📄 Exportar PDF"** - Relatório formatado
   - **"📊 Exportar CSV"** - Planilha Excel

### 👥 Gerenciar Usuários (Admin)

1. Clique em **"👥 Gerenciar Usuários"** na lateral
2. Clique em **"+ Novo Usuário"**
3. Preencha os dados:
   - Nome de usuário
   - Email
   - Senha
   - Função (Visualizador/Editor/Admin)

---

## 🔐 Tipos de Usuários

| Função | Consultar | Exportar | Gerenciar Usuários |
|--------|-----------|----------|-------------------|
| **Visualizador** | ✅ | ❌ | ❌ |
| **Editor** | ✅ | ✅ | ❌ |
| **Admin** | ✅ | ✅ | ✅ |

---

## 🌐 Publicar Online (Ngrok)

### Compartilhar com Colegas

```bash
# Terminal 1 - Dashboard
python app.py

# Terminal 2 - Ngrok (Download em https://ngrok.com)
ngrok http 5000
```

Você receberá uma URL como: `https://abc123.ngrok.io`

Compartilhe com sua equipe! 🎉

---

## 📊 Exemplos de Uso

### Exemplo 1: Buscar proprietários em Buenoseco

1. Digite no filtro **"Setor":** `buenoseco`
2. Clique **"Buscar"**
3. Exporte em PDF

### Exemplo 2: Imóveis com 3 quartos em Wakbueno PA001

1. Digite no filtro **"Wakbueno":** `PA001`
2. Digite no filtro **"Quartos":** `3`
3. Clique **"Buscar"**
4. Exporte em CSV para análise

### Exemplo 3: Todos os imóveis de um proprietário

1. Digite no filtro **"Proprietário":** (nome da pessoa)
2. Clique **"Buscar"**
3. Veja todos os imóveis dessa pessoa

---

## ⚙️ Configuração Avançada

### Alterar Porta

Editar `app.py`, linha final:
```python
app.run(debug=False, host='0.0.0.0', port=8080)  # Mudar 5000 para 8080
```

### Ativar Debug (Desenvolvimento)

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Conectar em Outro Computador

Em vez de `localhost`, use o IP da máquina:
```
http://192.168.1.100:5000
```

---

## 🆘 Problemas Comuns

### ❌ "Module not found: flask"
**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ "SUPABASE_KEY not found"
**Solução:** Definir variável de ambiente (veja passo 2️⃣ acima)

### ❌ "Connection refused"
**Solução:** Verificar se dashboard está rodando (veja passo 3️⃣)

### ❌ "Nenhum dado carregado"
**Solução:** Verificar se os filtros estão corretos e se há dados no Supabase

---

## 📚 Documentação Completa

Para mais informações, leia:

1. **README.md** - Documentação completa
2. **DEPLOYMENT.md** - Guia de publicação em domínio
3. **app.py** - Código backend comentado
4. **dashboard.html** - Código frontend comentado

---

## 🎯 Próximos Passos

### Curto Prazo
- [ ] Criar usuários para sua equipe
- [ ] Testar filtros com dados reais
- [ ] Configurar exportação em PDF

### Médio Prazo
- [ ] Publicar com Ngrok para testes
- [ ] Configurar domínio com PythonAnywhere

### Longo Prazo
- [ ] Publicar em VPS (DigitalOcean/AWS)
- [ ] Configurar SSL com Let's Encrypt
- [ ] Implementar backups automáticos

---

## 💡 Dicas Pro

1. **Filtros Combinados:** Use múltiplos filtros simultaneamente para buscas precisas
2. **Limite de Registros:** Aumente para carregar mais dados (impacta performance)
3. **Exportar Antes de Limpar:** Sempre exporte antes de filtrar novamente
4. **Nomes Únicos:** Ao criar usuários, use nomes descritivos (ex: maria.oliveira)
5. **Backup Manual:** Faça download do `dashboard.db` regularmente

---

## 📞 Suporte Rápido

| Problema | Solução |
|----------|---------|
| Esqueceu senha admin | Edite dashboard.db com SQLite |
| Dashboard lento | Aumente recursos, reduza limite de registros |
| Dados não aparecem | Verifique filtros, aumentar limite |
| Erro de exportação | Reduzir número de registros |

---

**Versão:** 1.0.0  
**Status:** ✅ Pronto para Produção

Bom uso! 🚀
