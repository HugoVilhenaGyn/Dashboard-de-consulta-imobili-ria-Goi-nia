import importlib.util, requests
spec = importlib.util.spec_from_file_location('m','up_supabase.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
try:
    resp = requests.get(m.ENDPOINT + '?limit=5', headers=m.HEADERS, timeout=15)
    print('STATUS', resp.status_code)
    print(resp.text)
except Exception as e:
    print('ERROR', e)
