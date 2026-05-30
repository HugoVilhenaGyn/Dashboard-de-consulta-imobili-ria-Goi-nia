import os, sys
# Lê a chave do arquivo temporariamente para teste
# Em produção, usar: set SUPABASE_KEY=sua_chave e depois rodar up_supabase.py
import importlib.util
spec = importlib.util.spec_from_file_location('m','up_supabase.py')
m = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
    print("✅ Script carregado com sucesso!")
    print(f"   Endpoint: {m.ENDPOINT}")
    print(f"   Tabela: {m.NOME_TABELA}")
    print(f"   Pasta: {m.PASTA_RAIZ}")
    arquivos = m.encontrar_arquivos_xlsx(m.PASTA_RAIZ)
    if not arquivos:
        print("❌ Nenhum arquivo .xlsx encontrado")
        raise SystemExit(1)
    print(f"✅ {len(arquivos)} arquivo(s) encontrado(s)")
    # Process first file as test
    caminho = arquivos[0]
    print(f"\n📝 Testando com: {caminho.split(os.sep)[-1]}")
    enviados, erros = m.processar_arquivo(caminho)
    if erros:
        print(f"❌ Erros: {erros}")
    else:
        print(f"✅ {enviados} registros enviados com sucesso!")
except SystemExit as e:
    if e.code != 0:
        print(f"❌ Erro: SUPABASE_KEY não definida. Configure primeiro com:")
        print("   Windows: set SUPABASE_KEY=sua_chave_aqui")
        print("   Linux:   export SUPABASE_KEY=sua_chave_aqui")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
