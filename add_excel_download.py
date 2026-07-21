import io, sys

TARGET = sys.argv[1]

with io.open(TARGET, encoding='utf-8') as f:
    c = f.read()

replacements = [
    (
        '  .filters .count { font-size: 12.5px; color: var(--text-muted); margin-left: auto; }\n',
        '  .filters .count { font-size: 12.5px; color: var(--text-muted); margin-left: auto; }\n'
        '  .btn-excel {\n'
        '    display:inline-flex; align-items:center; gap:7px; font: inherit; font-size: 13px; font-weight: 600;\n'
        '    padding: 7px 14px; border-radius: 8px; border: 1px solid var(--green);\n'
        '    background: var(--green); color: #0B1220; cursor: pointer;\n'
        '    transition: filter .15s ease, transform .05s ease; white-space: nowrap;\n'
        '  }\n'
        '  .btn-excel:hover { filter: brightness(1.08); }\n'
        '  .btn-excel:active { transform: translateY(1px); }\n'
        '  .btn-excel svg { width:14px; height:14px; flex:none; }\n'
        '  .btn-excel:disabled { opacity:.6; cursor: default; }\n'
    ),
    (
        '        <span class="count" id="f-count"></span>\n',
        '        <span class="count" id="f-count"></span>\n'
        '        <button type="button" id="btn-excel" class="btn-excel" title="Descarga el catálogo filtrado en Excel">\n'
        '          <svg viewBox="0 0 24 24" fill="none" stroke="#0B1220" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n'
        '            <path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M4 19h16"/>\n'
        '          </svg>\n'
        '          Descargar Excel\n'
        '        </button>\n'
    ),
    (
        "render();\n</script>",
        """function xmlEsc(s) {
  return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function durTexto(min) {
  if (min === null || min === undefined) return '';
  const hh = Math.floor(min / 60), mm = Math.round(min % 60);
  if (hh && mm) return hh + ' h ' + mm + ' min';
  if (hh) return hh + ' h';
  return mm + ' min';
}
function descargarExcel() {
    const r = applyFilters();
    const headers = ['Curso', 'Cliente / Institución', 'Duración (min)', 'Duración', 'Estado', 'Registros en 2026'];
    let rowsXml = '<Row ss:StyleID="Header">' + headers.map(h => '<Cell><Data ss:Type="String">' + xmlEsc(h) + '</Data></Cell>').join('') + '</Row>\\n';
    r.forEach(x => {
      const styleId = (x.estado === 'sin_tiempo' || x.estado === 'sin_examen') ? ' ss:StyleID="SinTiempo"' : (x.estado === 'nuevo' ? ' ss:StyleID="Nuevo"' : '');
      const minCell = (x.min === null || x.min === undefined) ? '<Cell><Data ss:Type="String"></Data></Cell>' : ('<Cell><Data ss:Type="Number">' + x.min + '</Data></Cell>');
      const texto = x.min !== null && x.min !== undefined ? durTexto(x.min) : (x.estado === 'nuevo' ? 'NUEVO - REVISAR' : (ESTADO_LABEL[x.estado] || ''));
      rowsXml += '<Row' + styleId + '>' +
        '<Cell><Data ss:Type="String">' + xmlEsc(x.curso) + '</Data></Cell>' +
        '<Cell><Data ss:Type="String">' + xmlEsc(x.inst || '') + '</Data></Cell>' +
        minCell +
        '<Cell><Data ss:Type="String">' + xmlEsc(texto) + '</Data></Cell>' +
        '<Cell><Data ss:Type="String">' + xmlEsc(ESTADO_LABEL[x.estado] || x.estado) + '</Data></Cell>' +
        '<Cell><Data ss:Type="Number">' + (x.n || 0) + '</Data></Cell>' +
        '</Row>\\n';
    });
    const fecha = new Date().toISOString().slice(0, 10);
    const xml = '<?xml version="1.0" encoding="UTF-8"?>\\n' +
      '<?mso-application progid="Excel.Sheet"?>\\n' +
      '<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">\\n' +
      '<Styles>\\n' +
      '<Style ss:ID="Header"><Font ss:Bold="1" ss:Color="#FFFFFF"/><Interior ss:Color="#16245C" ss:Pattern="Solid"/></Style>\\n' +
      '<Style ss:ID="SinTiempo"><Font ss:Color="#6B7280" ss:Italic="1"/><Interior ss:Color="#F0F0EE" ss:Pattern="Solid"/></Style>\\n' +
      '<Style ss:ID="Nuevo"><Font ss:Color="#2F6BE4" ss:Bold="1"/><Interior ss:Color="#E8F0FE" ss:Pattern="Solid"/></Style>\\n' +
      '</Styles>\\n' +
      '<Worksheet ss:Name="Duracion Cursos"><Table>\\n' + rowsXml + '</Table></Worksheet>\\n' +
      '</Workbook>';
    const blob = new Blob(['\\ufeff' + xml], { type: 'application/vnd.ms-excel' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Catalogo_Cursos_2026_' + fecha + '.xls';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}
document.getElementById('btn-excel').addEventListener('click', descargarExcel);

render();
</script>""",
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
