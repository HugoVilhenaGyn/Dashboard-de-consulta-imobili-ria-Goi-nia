@echo off
REM Script de inicialização do Dashboard
REM Compatível com Windows

echo.
echo ====================================================
echo   Dashboard de Imoveis - Inicializador
echo ====================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Instale Python de https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado

REM Verificar se pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] pip não encontrado!
    pause
    exit /b 1
)

echo [OK] pip encontrado

REM Instalar/atualizar dependências
echo.
echo Instalando dependências...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências
    pause
    exit /b 1
)

echo [OK] Dependências instaladas

REM Configurar variável de ambiente
echo.
echo Digite sua chave JWT do Supabase:
set /p SUPABASE_KEY="SUPABASE_KEY="

if "%SUPABASE_KEY%"=="" (
    echo [ERRO] Chave não pode estar vazia
    pause
    exit /b 1
)

REM Executar aplicação
echo.
echo ====================================================
echo   Iniciando Dashboard...
echo   Acesse: http://localhost:5000
echo ====================================================
echo.
echo Credenciais padrão:
echo   Usuário: admin
echo   Senha: admin123
echo.
echo Pressione CTRL+C para parar
echo.

python app.py

pause
