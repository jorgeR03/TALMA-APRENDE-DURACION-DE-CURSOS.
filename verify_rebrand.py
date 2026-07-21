import json, sys
target = sys.argv[1] if len(sys.argv) > 1 else 'Tablero Duracion de Cursos.html'
with open(target, encoding='utf-8') as f:
    html = f.read()
i = html.index('const DATA = ') + len('const DATA = ')
j = html.index(';\nfunction fmt(n)', i)
data = json.loads(html[i:j])
print('DATA ok:', data['total'], data['ok'], data['sin_tiempo'], data['sin_examen'])
print('svg logo presente:', 'aria-label="Talma Aprende"' in html)
print('h1 nuevo:', '<h1>Catálogo Cursos 2026</h1>' in html)
print('navy oficial:', '#16245C' in html)
print('dur-min:', '.dur-min' in html)
print('no institucion col:', 'Cliente / institución' not in html)
print('old img base64 logo removido:', 'banner-logo" src="data:image/png' not in html)
