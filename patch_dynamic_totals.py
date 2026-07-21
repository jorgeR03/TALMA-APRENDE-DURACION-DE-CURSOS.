import io, sys
TARGET = sys.argv[1]
with io.open(TARGET, encoding='utf-8') as f:
    c = f.read()

reps = [
    ('<p class="sub">261 cursos revisados: con duración registrada, sin tiempo definido (autoformativos o de lectura) y sin examen asociado.</p>',
     '<p class="sub" id="sub-estado">Cursos revisados: con duración registrada, sin tiempo definido (autoformativos o de lectura) y sin examen asociado.</p>'),
    ('<p class="sub">261 cursos con "2026" en el nombre. Clic en un encabezado para ordenar.</p>',
     '<p class="sub" id="sub-catalogo">Cursos con "2026" en el nombre. Clic en un encabezado para ordenar.</p>'),
    ('(function renderKPIs(){',
     "document.getElementById('sub-estado').textContent = `${fmt(DATA.total)} cursos revisados: con duración registrada, sin tiempo definido (autoformativos o de lectura) y sin examen asociado.`;\n"
     "document.getElementById('sub-catalogo').textContent = `${fmt(DATA.total)} cursos con \"2026\" en el nombre. Clic en un encabezado para ordenar.`;\n\n"
     "(function renderKPIs(){"),
]
missing = []
for old, new in reps:
    if old not in c:
        missing.append(old[:60])
        continue
    c = c.replace(old, new, 1)
with io.open(TARGET, 'w', encoding='utf-8') as f:
    f.write(c)
print('OK', TARGET, 'faltantes:', missing)
