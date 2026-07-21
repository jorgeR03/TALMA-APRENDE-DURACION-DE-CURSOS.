import io, sys

TARGET = sys.argv[1]

with io.open(TARGET, encoding='utf-8') as f:
    c = f.read()

OLD = """function descargarExcel() {
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
}"""

NEW = """function barraGrafico(min, maxMin) {
  if (min === null || min === undefined || !maxMin) return '';
  const total = 20;
  const llenas = Math.max(1, Math.round((min / maxMin) * total));
  return '\\u2588'.repeat(llenas) + '\\u2591'.repeat(total - llenas);
}
function descargarExcel() {
    const r = applyFilters();
    const maxMin = Math.max(1, ...r.filter(x => x.min !== null && x.min !== undefined).map(x => x.min), 1);
    const headers = ['Curso', 'Duración (min)', 'Duración (h)', 'Gráfico'];
    let rowsXml = '<Row ss:StyleID="Header">' + headers.map(h => '<Cell><Data ss:Type="String">' + xmlEsc(h) + '</Data></Cell>').join('') + '</Row>\\n';
    r.forEach(x => {
      const styleId = (x.estado === 'sin_tiempo' || x.estado === 'sin_examen') ? ' ss:StyleID="SinTiempo"' : (x.estado === 'nuevo' ? ' ss:StyleID="Nuevo"' : '');
      const tieneMin = x.min !== null && x.min !== undefined;
      const etiqueta = x.estado === 'nuevo' ? 'NUEVO - REVISAR' : (ESTADO_LABEL[x.estado] || '');
      const minCell = tieneMin
        ? '<Cell><Data ss:Type="Number">' + x.min + '</Data></Cell>'
        : '<Cell><Data ss:Type="String">' + xmlEsc(etiqueta) + '</Data></Cell>';
      const hCell = tieneMin
        ? '<Cell><Data ss:Type="Number">' + hoursOf(x.min) + '</Data></Cell>'
        : '<Cell><Data ss:Type="String">' + xmlEsc(etiqueta) + '</Data></Cell>';
      const barra = barraGrafico(x.min, maxMin);
      const barCell = barra
        ? '<Cell ss:StyleID="Bar"><Data ss:Type="String">' + xmlEsc(barra) + '</Data></Cell>'
        : '<Cell><Data ss:Type="String"></Data></Cell>';
      rowsXml += '<Row' + styleId + '>' +
        '<Cell><Data ss:Type="String">' + xmlEsc(x.curso) + '</Data></Cell>' +
        minCell +
        hCell +
        barCell +
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
      '<Style ss:ID="Bar"><Font ss:FontName="Consolas" ss:Color="#1E9E63"/></Style>\\n' +
      '</Styles>\\n' +
      '<Worksheet ss:Name="Duracion Cursos"><Table>\\n' +
      '<Column ss:Width="380"/><Column ss:Width="80"/><Column ss:Width="70"/><Column ss:Width="160"/>\\n' +
      rowsXml + '</Table></Worksheet>\\n' +
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
}"""

OLD_DURTEXTO = """function durTexto(min) {
  if (min === null || min === undefined) return '';
  const hh = Math.floor(min / 60), mm = Math.round(min % 60);
  if (hh && mm) return hh + ' h ' + mm + ' min';
  if (hh) return hh + ' h';
  return mm + ' min';
}
"""

missing = []
if OLD not in c:
    missing.append('descargarExcel')
else:
    c = c.replace(OLD, NEW, 1)
if OLD_DURTEXTO not in c:
    missing.append('durTexto')
else:
    c = c.replace(OLD_DURTEXTO, '', 1)

with io.open(TARGET, 'w', encoding='utf-8') as f:
    f.write(c)

if missing:
    print('ADVERTENCIA, no se encontraron:', missing, 'en', TARGET)
else:
    print('OK ->', TARGET)
