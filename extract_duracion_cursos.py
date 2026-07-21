import json, time, sys
import openpyxl

SRC = sys.argv[1] if len(sys.argv) > 1 else r'Archivos\reporteglobal (2).xlsx'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'cursos_2026_tiempos.json'

t0 = time.time()
wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb['Sheet1']

rows = ws.iter_rows(values_only=True)
header = next(rows)
header = [h.strip().lower() if isinstance(h, str) else h for h in header]
idx = {h: i for i, h in enumerate(header)}
print('columnas:', header)

i_curso = idx.get('curso')
i_tiempo = idx.get('tiempo requerido')
i_idcurso = idx.get('idcurso')
i_institucion = idx.get('institucion')

cursos = {}  # nombre -> dict(tiempos=set, idcursos=set, instituciones=set, n=count)
n = 0
for row in rows:
    n += 1
    curso = row[i_curso]
    if not curso or '2026' not in curso:
        continue
    tiempo = row[i_tiempo]
    idcurso = row[i_idcurso]
    inst = row[i_institucion]
    e = cursos.setdefault(curso, dict(tiempos=set(), idcursos=set(), instituciones=set(), n=0))
    e['n'] += 1
    if tiempo not in (None, ''):
        e['tiempos'].add(tiempo)
    if idcurso is not None:
        e['idcursos'].add(idcurso)
    if inst is not None:
        e['instituciones'].add(inst)

print('filas procesadas:', n, 'en', round(time.time() - t0, 1), 's')
print('cursos 2026 unicos:', len(cursos))

out = {}
for curso, e in cursos.items():
    out[curso] = dict(
        n=e['n'],
        tiempos=sorted(e['tiempos']),
        idcursos=sorted(e['idcursos']),
        instituciones=sorted(e['instituciones']),
    )

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

con_tiempo = sum(1 for e in out.values() if e['tiempos'])
sin_tiempo = len(out) - con_tiempo
multi_tiempo = sum(1 for e in out.values() if len(e['tiempos']) > 1)
print('con tiempo_requerido:', con_tiempo, '| sin tiempo:', sin_tiempo, '| con valores distintos:', multi_tiempo)
