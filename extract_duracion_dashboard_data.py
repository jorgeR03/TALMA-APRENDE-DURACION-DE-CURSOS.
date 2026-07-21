import json, re

with open('cursos_2026_tiempos.json', encoding='utf-8') as f:
    cursos = json.load(f)

def parse_minutos(tiempos):
    if not tiempos:
        return None
    t = tiempos[0]
    m = re.match(r'(\d+)\s*h,\s*(\d+)\s*min,\s*(\d+)\s*seg', t)
    if not m:
        return None
    h, mi, s = (int(x) for x in m.groups())
    return h * 60 + mi + round(s / 60)

rows = []
for curso, e in cursos.items():
    minutos = parse_minutos(e['tiempos'])
    rows.append([curso, ', '.join(e['instituciones']), minutos, e['n']])

rows.sort(key=lambda r: (r[2] is not None, r[0].upper()))

buckets = [
    ('<= 15 min', 0, 15), ('16-30 min', 16, 30), ('31-60 min', 31, 60),
    ('61-120 min', 61, 120), ('121-240 min', 121, 240),
    ('241-480 min', 241, 480), ('> 480 min', 481, 10**9),
]
hist = [0] * len(buckets)
for r in rows:
    if r[2] is None:
        continue
    for i, (label, lo, hi) in enumerate(buckets):
        if lo <= r[2] <= hi:
            hist[i] += 1
            break

data = dict(
    total=len(rows),
    con_dato=sum(1 for r in rows if r[2] is not None),
    sin_dato=sum(1 for r in rows if r[2] is None),
    buckets=[b[0] for b in buckets],
    hist=hist,
    rows=rows,
)
with open('duracion_dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
print('OK', data['total'], data['con_dato'], data['sin_dato'])
