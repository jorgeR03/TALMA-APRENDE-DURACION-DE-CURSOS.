import io

import sys
HTML = sys.argv[1] if len(sys.argv) > 1 else 'Tablero Duracion de Cursos.html'
JSON = 'duracion_dashboard_data.json'

with io.open(HTML, encoding='utf-8') as f:
    html = f.read()
with io.open(JSON, encoding='utf-8') as f:
    new_json = f.read().strip()

marker_start = 'const DATA = '
marker_end = ';\nfunction fmt(n)'

i = html.index(marker_start) + len(marker_start)
j = html.index(marker_end, i)

old_len = j - i
html2 = html[:i] + new_json + html[j:]

with io.open(HTML, 'w', encoding='utf-8') as f:
    f.write(html2)

print('DATA reemplazada. Tamaño anterior:', old_len, '-> nuevo:', len(new_json))
