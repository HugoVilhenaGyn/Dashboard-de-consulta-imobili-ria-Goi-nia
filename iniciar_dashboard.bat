@echo off
chcp 65001 >nul
setlocal

REM ─── Configuração ───────────────────────────────────
set "PASTA=c:\VS Code\upload_supabase.py"
set "SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDA3MzAxMiwiZXhwIjoyMDk1NjQ5MDEyfQ.G4n25w9oKKI9wvoMVimpUFfV-n1QTFPFrOtnGqsC-JM"
set "VENV=%PASTA%\.venv\Scripts\python.exe"

REM ─── Mudar para a pasta do projeto ──────────────────
cd /d "%PASTA%"

REM ─── Iniciar o servidor Flask em segundo plano ──────
start "" /B "%VENV%" app.py

REM ─── Aguardar o servidor iniciar (3 segundos) ───────
timeout /t 3 /nobreak >nul

REM ─── Abrir o navegador ──────────────────────────────
start "" "http://localhost:5000"
