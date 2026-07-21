import io, sys

TARGET = sys.argv[1]

with io.open(TARGET, encoding='utf-8') as f:
    c = f.read()

replacements = [
    (
        "  .badge.sin_examen { background: var(--grid); color: var(--text-muted); }\n",
        "  .badge.sin_examen { background: var(--grid); color: var(--text-muted); }\n"
        "  .badge.nuevo { background: color-mix(in srgb, #2F6BE4 20%, transparent); color: #6C9CFF; }\n"
    ),
    (
        '  .kpis { display:grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 18px; }\n',
        '  .kpis { display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 18px; }\n'
        '  @media (max-width: 860px) { .kpis { grid-template-columns: repeat(2, 1fr); } }\n'
    ),
    (
        '  .kpi .value.muted { color: var(--text-muted); }\n',
        '  .kpi .value.muted { color: var(--text-muted); }\n'
        '  .kpi .value.nuevo { color: #6C9CFF; }\n'
    ),
    (
        '          <option value="sin_examen">Sin examen</option>\n        </select>',
        '          <option value="sin_examen">Sin examen</option>\n'
        '          <option value="nuevo">Nuevo - revisar</option>\n        </select>'
    ),
    (
        "    { label: 'Sin tiempo / sin examen', raw: DATA.sin_tiempo + DATA.sin_examen, foot: DATA.sin_tiempo + ' sin tiempo · ' + DATA.sin_examen + ' sin examen', cls:'muted' },\n  ];",
        "    { label: 'Sin tiempo / sin examen', raw: DATA.sin_tiempo + DATA.sin_examen, foot: DATA.sin_tiempo + ' sin tiempo · ' + DATA.sin_examen + ' sin examen', cls:'muted' },\n"
        "    { label: 'Nuevos por revisar', raw: DATA.nuevo || 0, foot: 'detectados en la última actualización', cls:'nuevo' },\n  ];"
    ),
    (
        "const items = [['ok','Con duración', DATA.ok, 'var(--good)'], ['sin_tiempo','Sin tiempo definido', DATA.sin_tiempo, 'var(--accent)'], ['sin_examen','Sin examen', DATA.sin_examen, 'var(--text-muted)']];",
        "const items = [['ok','Con duración', DATA.ok, 'var(--good)'], ['sin_tiempo','Sin tiempo definido', DATA.sin_tiempo, 'var(--accent)'], ['sin_examen','Sin examen', DATA.sin_examen, 'var(--text-muted)'], ['nuevo','Nuevo - revisar', DATA.nuevo || 0, '#6C9CFF']];"
    ),
    (
        "const ESTADO_LABEL = { ok: 'Con duración', sin_tiempo: 'Sin tiempo', sin_examen: 'Sin examen' };",
        "const ESTADO_LABEL = { ok: 'Con duración', sin_tiempo: 'Sin tiempo', sin_examen: 'Sin examen', nuevo: 'Nuevo - revisar' };"
    ),
]

missing = []
for old, new in replacements:
    if old not in c:
        missing.append(old[:70])
        continue
    c = c.replace(old, new, 1)

with io.open(TARGET, 'w', encoding='utf-8') as f:
    f.write(c)

print('OK ->', TARGET)
if missing:
    print('ADVERTENCIA, no se encontraron estos marcadores:')
    for m in missing:
        print('  ', repr(m))
