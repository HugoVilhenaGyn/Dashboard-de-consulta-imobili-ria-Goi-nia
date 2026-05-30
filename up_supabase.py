"""
=============================================================
  UPLOAD AUTOMÁTICO DE ARQUIVOS XLSX PARA O SUPABASE
  Versão: REST API direta (sem biblioteca supabase, sem IA)

  Como usar:
  1. Instale: pip install pandas openpyxl requests tqdm
  2. Defina a variável de ambiente SUPABASE_KEY
  3. Rode: python up_supabase.py
=============================================================
"""

import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime

# ============================================================
#  CONFIGURAÇÕES — PREENCHA AQUI
# ============================================================

SUPABASE_URL  = "https://mquuvzrwrimrlpgjdnjv.supabase.co"
SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xdXV2enJ3cmltcmxwZ2pkbmp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDA3MzAxMiwiZXhwIjoyMDk1NjQ5MDEyfQ.G4n25w9oKKI9wvoMVimpUFfV-n1QTFPFrOtnGqsC-JM"

PASTA_RAIZ   = r"C:\Arquivo Robô Prospecção"
NOME_TABELA  = "imoveis"
TAMANHO_LOTE = 50    # registros por requisicao
UPSERT       = True  # True = upsert (atualiza duplicatas); False = insert puro
MAX_TENTATIVAS = 3   # tentativas por lote em caso de erro de rede

# Colunas de metadados adicionadas automaticamente.
# Coloque False se a tabela nao tiver essas colunas.
ADICIONAR_METADADOS = True

# ============================================================

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates,return=minimal" if UPSERT else "return=minimal",
}

ENDPOINT     = f"{SUPABASE_URL}/rest/v1/{NOME_TABELA}"
COLUNAS_DATAS = ["horaInsercao", "horaInicio", "horaFim"]

COLUNAS_VALIDAS = None  # preenchido em main() com as colunas reais da tabela


# ============================================================

def buscar_colunas_validas():
    """Retorna o conjunto de colunas existentes na tabela do Supabase."""
    try:
        resp = requests.get(ENDPOINT + "?limit=1", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            rows = resp.json()
            if rows:
                return set(rows[0].keys())
            # tabela vazia: usa o header Content-Range ou OpenAPI
            schema_resp = requests.get(
                f"{SUPABASE_URL}/rest/v1/",
                headers={**HEADERS, "Accept": "application/openapi+json"},
                timeout=10,
            )
            if schema_resp.status_code == 200:
                props = (
                    schema_resp.json()
                    .get("definitions", {})
                    .get(NOME_TABELA, {})
                    .get("properties", {})
                )
                if props:
                    return set(props.keys())
    except Exception:
        pass
    return None


def encontrar_arquivos_xlsx(pasta_raiz):
    arquivos = []
    for dirpath, _, filenames in os.walk(pasta_raiz):
        for filename in filenames:
            if filename.lower().endswith(".xlsx"):
                arquivos.append(os.path.join(dirpath, filename))
    return arquivos


def limpar_coluna_numerica(serie, col_name):
    s = serie.dropna().astype(str).str.strip()
    if s.empty:
        return serie
    cleaned = s.str.replace(r"[\.\s]", "", regex=True).str.replace(",", ".", regex=False)
    num = pd.to_numeric(cleaned, errors="coerce")
    frac = num.notna().sum() / len(num) if len(num) > 0 else 0
    if frac >= 0.9:
        return num
    num_tokens = [
        "num", "numero", "id", "codigo", "inscricao", "area",
        "valor", "ci", "x_coord", "y_coord", "objectid", "quadra",
        "lote", "bairro", "zona", "pavimento",
    ]
    if any(tok in col_name.lower() for tok in num_tokens):
        extracted = s.str.extract(r"(\d+)")[0]
        num2 = pd.to_numeric(extracted, errors="coerce")
        frac2 = num2.notna().sum() / len(num2) if len(num2) > 0 else 0
        if frac2 >= 0.9:
            return num2
    return serie


def limpar_registro(registro):
    limpo = {}
    for k, v in registro.items():
        if isinstance(v, float) and v != v:          # NaN float
            limpo[k] = None
        elif not isinstance(v, (list, dict)) and pd.isna(v) if not isinstance(v, (bool, int, float, str, list, dict)) else False:
            limpo[k] = None
        elif hasattr(v, "isoformat"):
            limpo[k] = v.isoformat()
        elif isinstance(v, float) and v.is_integer():
            limpo[k] = int(v)  # converte 58.0 → 58 para colunas bigint
        else:
            limpo[k] = v
    return limpo


def enviar_lote(registros):
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            resp = requests.post(ENDPOINT, json=registros, headers=HEADERS, timeout=30)
            if resp.status_code in (200, 201):
                return True, None
            return False, f"HTTP {resp.status_code}: {resp.text[:300]}"
        except requests.exceptions.ConnectionError as e:
            if tentativa < MAX_TENTATIVAS:
                time.sleep(2 * tentativa)
                continue
            return False, f"Erro de conexao apos {MAX_TENTATIVAS} tentativas: {e}"
        except Exception as e:
            return False, str(e)
    return False, "Falhou todas as tentativas"


def processar_arquivo(caminho):
    erros = []
    total_enviado = 0

    try:
        df = pd.read_excel(caminho, engine="openpyxl")
    except Exception as e:
        return 0, [f"Erro ao ler arquivo: {e}"]

    if df.empty:
        return 0, []

    for col in COLUNAS_DATAS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in df.columns:
        if col not in COLUNAS_DATAS:
            df[col] = limpar_coluna_numerica(df[col], col)

    if ADICIONAR_METADADOS:
        df["_arquivo_origem"] = os.path.basename(caminho)
        df["_pasta_origem"]   = os.path.dirname(caminho).replace(PASTA_RAIZ, "").lstrip(os.sep)
        df["_dt_importacao"]  = datetime.now().isoformat()

    if COLUNAS_VALIDAS:
        colunas_remover = [c for c in df.columns if c not in COLUNAS_VALIDAS]
        if colunas_remover:
            df = df.drop(columns=colunas_remover)

    registros = [limpar_registro(r) for r in df.to_dict(orient="records")]

    for i in range(0, len(registros), TAMANHO_LOTE):
        lote = registros[i : i + TAMANHO_LOTE]
        sucesso, erro = enviar_lote(lote)
        if sucesso:
            total_enviado += len(lote)
        else:
            erros.append(f"Lote {i // TAMANHO_LOTE + 1}: {erro}")

    return total_enviado, erros


def main():
    print("=" * 60)
    modo = "UPSERT" if UPSERT else "INSERT"
    print(f"  UPLOAD XLSX -> SUPABASE  [{modo}]")
    print("=" * 60)

    print("\nTestando conexao...")
    try:
        resp = requests.get(ENDPOINT + "?limit=1", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            print("  Conectado com sucesso!")
        else:
            print(f"  Erro: HTTP {resp.status_code} — {resp.text[:300]}")
            print("  Verifique SUPABASE_URL e SUPABASE_KEY.")
            return
    except Exception as e:
        print(f"  Erro de conexao: {e}")
        return

    global COLUNAS_VALIDAS
    COLUNAS_VALIDAS = buscar_colunas_validas()
    if COLUNAS_VALIDAS:
        print(f"  Schema carregado: {len(COLUNAS_VALIDAS)} colunas conhecidas")
    else:
        print("  Aviso: nao foi possivel carregar o schema — colunas nao serao filtradas")

    print(f"\nVarrendo: {PASTA_RAIZ}")
    arquivos = encontrar_arquivos_xlsx(PASTA_RAIZ)

    if not arquivos:
        print("  Nenhum .xlsx encontrado. Verifique PASTA_RAIZ.")
        return

    print(f"  {len(arquivos)} arquivo(s) encontrado(s)\n")

    total_registros = 0
    arquivos_ok     = 0
    arquivos_erro   = []
    log_linhas      = []

    for caminho in tqdm(arquivos, desc="Enviando", unit="arq"):
        nome_curto = caminho.replace(PASTA_RAIZ, "").lstrip(os.sep)
        enviados, erros = processar_arquivo(caminho)
        total_registros += enviados

        if erros:
            arquivos_erro.append((nome_curto, erros))
            log_linhas.append(f"[ERRO] {nome_curto}: {erros}")
        else:
            arquivos_ok += 1
            log_linhas.append(f"[OK]   {nome_curto}: {enviados} registros")

    print("\n" + "=" * 60)
    print("  RESUMO FINAL")
    print("=" * 60)
    print(f"  Arquivos enviados com sucesso : {arquivos_ok}")
    print(f"  Arquivos com erro             : {len(arquivos_erro)}")
    print(f"  Total de registros enviados   : {total_registros}")

    if arquivos_erro:
        print("\n  Arquivos com problema:")
        for nome, erros in arquivos_erro:
            print(f"    * {nome}")
            for e in erros:
                print(f"      -> {e}")

    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_upload.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Upload: {datetime.now()}\n")
        f.write(f"Modo: {modo}\n")
        f.write(f"Pasta: {PASTA_RAIZ}\n")
        f.write(f"Arquivos: {len(arquivos)} | Registros: {total_registros}\n\n")
        f.write("\n".join(log_linhas))

    print(f"\n  Log salvo em: {log_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
