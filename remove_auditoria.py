import json

with open('merged_state.json', encoding='utf-8') as f:
    merged = json.load(f)

before = len(merged['order'])
removed = [c for c in merged['order'] if 'auditoria' in c.lower()]
merged['order'] = [c for c in merged['order'] if 'auditoria' not in c.lower()]
for c in removed:
    merged['data'].pop(c, None)

with open('merged_state.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False)

print(f'Cursos antes: {before} | despues: {len(merged["order"])} | eliminados: {len(removed)}')
for c in removed:
    print('  -', c)
