import importlib.util, requests, json, os
spec = importlib.util.spec_from_file_location('m','up_supabase.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print('ENDPOINT=', m.ENDPOINT)
print('TABLE=', m.NOME_TABELA)
print('PASTA_RAIZ=', m.PASTA_RAIZ)
# mask key
print('HEADERS (keys):', list(m.HEADERS.keys()))
try:
    arquivos = m.encontrar_arquivos_xlsx(m.PASTA_RAIZ)
    if not arquivos:
        print('No xlsx files found in PASTA_RAIZ')
        raise SystemExit(0)
    caminho = arquivos[0]
    print('Using file:', caminho)
    import pandas as pd
    df = pd.read_excel(caminho, engine='openpyxl')
    for col in m.COLUNAS_DATAS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    df['_arquivo_origem'] = os.path.basename(caminho)
    df['_pasta_origem']   = os.path.dirname(caminho).replace(m.PASTA_RAIZ, '').lstrip(os.sep)
    df['_dt_importacao']  = m.datetime.now().isoformat()
    registros = [m.limpar_registro(r) for r in df.to_dict(orient='records')]
    lote = registros[:5]
    print('Sending lote of', len(lote))
    resp = requests.post(m.ENDPOINT, json=lote, headers=m.HEADERS, timeout=30)
    print('STATUS', resp.status_code)
    print('TEXT', resp.text[:2000])
except Exception as e:
    print('ERROR', e)
