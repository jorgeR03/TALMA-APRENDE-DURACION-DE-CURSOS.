import io, sys

TARGET = sys.argv[1] if len(sys.argv) > 1 else 'Tablero Duracion de Cursos.html'

with io.open(TARGET, encoding='utf-8') as f:
    content = f.read()

with io.open('hero_rampa_b64.txt', encoding='utf-8') as f:
    hero_b64 = f.read().strip()

LOGO_SVG_WHITE = '''<svg class="banner-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 470 96" role="img" aria-label="Talma Aprende">
        <defs>
          <linearGradient id="leafw" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#3FD0C6"/>
            <stop offset="1" stop-color="#14A8A0"/>
          </linearGradient>
        </defs>
        <path d="M70 16 C40 8, 14 22, 10 40 C30 30, 52 28, 74 30 C70 24, 70 20, 70 16 Z" fill="url(#leafw)"/>
        <text x="6" y="70" font-family="'Segoe UI', Arial, sans-serif" font-size="58" font-weight="800" fill="#FFFFFF" letter-spacing="-1">Talma</text>
        <line x1="232" y1="26" x2="252" y2="74" stroke="#5C6B96" stroke-width="3" stroke-linecap="round"/>
        <text x="262" y="62" font-family="'Segoe UI', Arial, sans-serif" font-size="34" font-weight="700" fill="#9CCC65" letter-spacing="2">APRENDE</text>
      </svg>'''

NEW_HEADER = '''<title>Catálogo Cursos 2026 — Talma Aprende</title>
<meta name="color-scheme" content="dark">
<style>
  :root, .viz-root {
    color-scheme: dark;
    --navy:           #16245C;
    --navy-700:       #101B45;
    --navy-600:       #233A7A;
    --green:          #70B818;
    --green-600:      #5C9613;
    --surface-1:      #131B40;
    --page:           #0A1230;
    --text-primary:   #FFFFFF;
    --text-secondary: #C7CEDA;
    --text-muted:     #8B93B3;
    --grid:           #263159;
    --baseline:       #33407A;
    --border:         rgba(255,255,255,0.12);
    --good:           #1E9E63;
    --warning:        #C9870C;
    --serious:        #D97F3D;
    --critical:       #D2453C;
    --neutral:        #33407A;
    --neutral-text:   #8B93B3;
    --brand-green:    #70B818;
    --accent:         #8CCB2E;
    --accent-wash:    rgba(112,184,24,0.16);
    --mono:           ui-monospace, "Cascadia Mono", "SF Mono", Consolas, "Roboto Mono", monospace;
    --card-shadow:    0 1px 2px rgba(0,0,0,0.35), 0 1px 1px rgba(0,0,0,0.25);
  }
  * { box-sizing: border-box; }
  html, body { margin:0; padding:0; background: var(--page); color: var(--text-primary); }
  .viz-root {
    background-color: var(--page);
    background-image: linear-gradient(rgba(9,14,34,.90), rgba(9,14,34,.94)), url("data:image/jpeg;base64,__HERO_B64__");
    background-size: cover; background-position: center 30%; background-attachment: fixed; background-repeat: no-repeat;
    color: var(--text-primary);
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    min-height: 100vh; padding: 0 0 60px;
  }
  .wrap { max-width: 1080px; margin: 0 auto; padding: 0 20px; }

  @keyframes fadeSlideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  @media (prefers-reduced-motion: no-preference) {
    .banner, .kpis, .card { animation: fadeSlideIn .5s ease both; }
    .kpis { animation-delay: .08s; }
    .card:nth-of-type(1) { animation-delay: .14s; }
    .card:nth-of-type(2) { animation-delay: .19s; }
    .card { transition: box-shadow .18s ease, transform .18s ease; }
    .card:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(0,0,0,0.35), 0 1px 2px rgba(0,0,0,0.3); }
  }

  .banner {
    background: linear-gradient(155deg, var(--navy) 0%, var(--navy-700) 100%);
    margin: 0 0 20px; padding: 20px 20px 16px;
    border-bottom: 3px solid var(--green);
    position: relative; overflow: hidden;
  }
  .banner::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,0.10) 45%, transparent 60%);
    background-size: 220% 220%; background-position: 130% 0;
    pointer-events: none;
  }
  @media (prefers-reduced-motion: no-preference) { .banner::after { animation: sheen 1.6s ease-out .3s both; } }
  @keyframes sheen { from { background-position: 130% 0; } to { background-position: -30% 0; } }
  .banner-inner { max-width: 1080px; margin: 0 auto; display:flex; align-items:center; gap: 18px; flex-wrap: wrap; }
  .banner-logo { height: 34px; width: auto; flex: none; display:block; }
  .banner-text h1 { color: #fff; font-size: 20px; font-weight: 700; margin: 0 0 4px; letter-spacing: -0.01em; text-wrap: balance; }
  .banner-text p { margin: 0; color: rgba(255,255,255,0.82); font-size: 12.5px; line-height: 1.5; max-width: 760px; }
'''

NEW_HEADER = NEW_HEADER.replace('__HERO_B64__', hero_b64)

start_marker = '<title>Duración de Cursos 2026 — Talma Aprende</title>'
end_marker = '.banner-text p { margin: 0; color: rgba(255,255,255,0.82); font-size: 12.5px; line-height: 1.5; max-width: 760px; }'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker) + len(end_marker)

if start_idx != 0:
    raise SystemExit(f'ADVERTENCIA: el marcador de inicio no esta en la posicion 0 (esta en {start_idx})')

content = NEW_HEADER + content[end_idx:]

# --- Reemplazar el <img> del logo por el SVG inline ---
img_start = content.index('<img class="banner-logo"')
b64_pos = content.index('base64,', img_start)
img_end = content.index('>', b64_pos) + 1
content = content[:img_start] + LOGO_SVG_WHITE + content[img_end:]

# --- Titulo H1 ---
content = content.replace(
    '<h1>Duración de Cursos — Catálogo 2026</h1>',
    '<h1>Catálogo Cursos 2026</h1>'
)
content = content.replace(
    '<p>Cursos del reporteador global de Talma Aprende cuyo nombre incluye "2026", con su duración verificada. Catálogo revisado y completado manualmente.</p>',
    '<p>Cursos del reporteador global de Talma Aprende cuyo nombre incluye &quot;2026&quot;, con su duración verificada.</p>'
)

with io.open(TARGET, 'w', encoding='utf-8') as f:
    f.write(content)

print('OK ->', TARGET, '| tamaño final:', len(content))
