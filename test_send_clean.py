import importlib.util, requests, os, re
import pandas as pd
spec = importlib.util.spec_from_file_location('m','up_supabase.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

print('ENDPOINT=', m.ENDPOINT)
print('Using PASTA_RAIZ=', m.PASTA_RAIZ)
arquivos = m.encontrar_arquivos_xlsx(m.PASTA_RAIZ)
if not arquivos:
    print('No xlsx files')
    raise SystemExit(0)
path = arquivos[0]
print('File:', path)
df = pd.read_excel(path, engine='openpyxl')
for col in m.COLUNAS_DATAS:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# analyze columns for numeric-likeness
candidates = []
for col in df.columns:
    ser = df[col].dropna()
    if ser.empty:
        continue
    # convert to string, strip
    s = ser.astype(str).str.strip()
    # try naive numeric coercion after removing common formatting
    cleaned = s.str.replace(r"[\.\s]", "", regex=True)  # remove dots and spaces (thousands)
    cleaned = cleaned.str.replace(',', '.', regex=False)     # comma to dot
    num = pd.to_numeric(cleaned, errors='coerce')
    frac = num.notna().sum() / len(num)
    if frac >= 0.9:
        candidates.append((col, round(frac,3)))

print('Numeric-like candidate columns (>=90%):')
for col, frac in candidates:
    print(' -', col, frac)

# Coerce candidates
for col, _ in candidates:
    s = df[col].astype(str).str.strip()
    cleaned = s.str.replace(r"[\.\s]", "", regex=True)
    cleaned = cleaned.str.replace(',', '.', regex=False)
    df[col] = pd.to_numeric(cleaned, errors='coerce')

# For columns not in candidates, try extracting digits if that makes them numeric
other_cols = [c for c in df.columns if c not in [x[0] for x in candidates]]
# tokens that indicate a numeric field
num_tokens = ['num', 'numero', 'id', 'codigo', 'inscricao', 'area', 'valor', 'ci', 'x_coord', 'y_coord', 'objectid', 'quadra', 'lote', 'bairro', 'zona', 'pavimento']
for col in other_cols:
    if col in m.COLUNAS_DATAS:
        continue
    name = col.lower()
    if not any(tok in name for tok in num_tokens):
        continue
    ser = df[col].dropna().astype(str).str.strip()
    if ser.empty:
        continue
    extracted = ser.str.extract(r"(\d+)")
    if extracted.dropna().empty:
        continue
    num = pd.to_numeric(extracted[0], errors='coerce')
    frac = num.notna().sum() / len(ser)
    if frac >= 0.9:
        print(f"Column '{col}' converted by extracting digits (fraction {frac:.3f})")
        df[col] = extracted[0]
        df[col] = pd.to_numeric(df[col], errors='coerce')

# prepare records and show sample
registros = [m.limpar_registro(r) for r in df.to_dict(orient='records')]
print('Prepared sample record (first):')
print(registros[0])

lote = registros[:5]
print('Sending lote of', len(lote))
try:
    resp = requests.post(m.ENDPOINT, json=lote, headers=m.HEADERS, timeout=30)
    print('STATUS', resp.status_code)
    print('TEXT', resp.text[:2000])
except Exception as e:
    print('ERROR during POST:', e)
