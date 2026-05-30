"""
Reenvia apenas os 6 arquivos que falharam por colunas inexistentes.
"""
import sys
sys.path.insert(0, r"c:\VS Code\upload_supabase.py")

import up_supabase as u
import requests

ARQUIVOS_ERRO = [
    r"C:\Arquivo Robô Prospecção\Dados Robô Mês Julho\Relatorio Execução 27.05.2025_Robô LOBO PA001_ExtracaoDados.xlsx",
    r"C:\Arquivo Robô Prospecção\Dados Robô Mês Junho\Relatorio Execução 06.06.2025_Robô LOBO PA001_ExtracaoDados.xlsx",
    r"C:\Arquivo Robô Prospecção\Dados Robô Mês Junho\Relatorio Execução 09.06.2025_Robô LOBO PA001_ExtracaoDados.xlsx",
    r"C:\Arquivo Robô Prospecção\Dados Robô Mês Junho\Relatorio Execução 11.06.2025 _Robô LOBO PA001_ExtracaoDados.xlsx",
    r"C:\Arquivo Robô Prospecção\Dados Robô Mês Junho\Relatorio Execução 12.06.2025_Robô LOBO PA001_ExtracaoDados.xlsx",
    r"C:\Arquivo Robô Prospecção\Dados Robô Mês Junho\Relatorio Execução 16.06.2025_Robô LOBO PA001_ExtracaoDados.xlsx",
]

print("=" * 60)
print("  REENVIO DOS 6 ARQUIVOS COM ERRO DE COLUNA")
print("=" * 60)

print("\nCarregando schema da tabela...")
u.COLUNAS_VALIDAS = u.buscar_colunas_validas()
if u.COLUNAS_VALIDAS:
    print(f"  {len(u.COLUNAS_VALIDAS)} colunas conhecidas")
else:
    print("  ERRO: nao foi possivel carregar o schema")
    sys.exit(1)

total_registros = 0
arquivos_ok = 0
arquivos_erro = []

for caminho in ARQUIVOS_ERRO:
    import os
    nome = os.path.basename(caminho)
    print(f"\n-> {nome}")
    enviados, erros = u.processar_arquivo(caminho)
    total_registros += enviados
    if erros:
        arquivos_erro.append((nome, erros))
        print(f"   [ERRO] {erros[0][:120]}")
    else:
        arquivos_ok += 1
        print(f"   [OK] {enviados} registros enviados")

print("\n" + "=" * 60)
print(f"  OK   : {arquivos_ok}/6 arquivos")
print(f"  ERRO : {len(arquivos_erro)}/6 arquivos")
print(f"  Total: {total_registros} registros enviados")
print("=" * 60)
