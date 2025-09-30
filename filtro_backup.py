import json

with open('backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# quitar las filas de permisos
data = [o for o in data if o.get('model') != 'auth.permission']

with open('backup_noperms.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('OK: backup_noperms.json generado')
