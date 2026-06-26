import pathlib

f = pathlib.Path('venv/Lib/site-packages/psycopg2/__init__.py')
content = f.read_bytes()
fixed = content.replace(b'open(f)', b'open(f, encoding="latin-1")')
f.write_bytes(fixed)
print('Corrigido!')