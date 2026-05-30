@echo off
REM Script Rápido - Iniciar Dashboard com Supabase
REM Compatível com Windows

setlocal enabledelayedexpansion

echo.
echo =========================================================
echo   DASHBOARD DE IMOVEIS - Inicializador Automático
echo =========================================================
echo.

REM Definir variável de ambiente com a chave
set "SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDA3MzAxMiwiZXhwIjoyMDk1NjQ5MDEyfQ.G4n25w9oKKI9wvoMVimpUFfV-n1QTFPFrOtnGqsC-JM"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Instale em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado

REM Instalar dependências
echo.
echo Instalando dependências... (pode levar 2-3 minutos)
pip install -q flask flask-cors supabase python-dotenv reportlab pandas requests openpyxl tqdm "httpx==0.28.1" "websockets>=14.0"
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências
    pause
    exit /b 1
)

echo [OK] Dependências instaladas!

REM Iniciar Dashboard
echo.
echo =========================================================
echo   DASHBOARD INICIANDO...
echo =========================================================
echo.
echo   ACESSE: http://localhost:5000
echo.
echo   LOGIN PADRÃO:
echo   • Usuário: admin
echo   • Senha:   admin123
echo.
echo   Para publicar online, abra OUTRO terminal e execute:
echo   • ngrok http 5000
echo.
echo   Veja PUBLICAR_AGORA.md para instruções completas
echo.
echo   Pressione CTRL+C para PARAR
echo =========================================================
echo.

python app.py

pause
