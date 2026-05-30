#!/bin/bash

# Script de inicialização do Dashboard
# Compatível com Linux e macOS

echo ""
echo "===================================================="
echo "  Dashboard de Imoveis - Inicializador"
echo "===================================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não encontrado!"
    echo "Instale com: brew install python (macOS) ou apt install python3 (Linux)"
    exit 1
fi

echo "[OK] Python 3 encontrado"

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "[ERRO] pip não encontrado!"
    exit 1
fi

echo "[OK] pip encontrado"

# Instalar/atualizar dependências
echo ""
echo "Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao instalar dependências"
    exit 1
fi

echo "[OK] Dependências instaladas"

# Configurar variável de ambiente
echo ""
echo "Digite sua chave JWT do Supabase:"
read -p "SUPABASE_KEY=" SUPABASE_KEY

if [ -z "$SUPABASE_KEY" ]; then
    echo "[ERRO] Chave não pode estar vazia"
    exit 1
fi

export SUPABASE_KEY

# Executar aplicação
echo ""
echo "===================================================="
echo "  Iniciando Dashboard..."
echo "  Acesse: http://localhost:5000"
echo "===================================================="
echo ""
echo "Credenciais padrão:"
echo "  Usuário: admin"
echo "  Senha: admin123"
echo ""
echo "Pressione CTRL+C para parar"
echo ""

python3 app.py
