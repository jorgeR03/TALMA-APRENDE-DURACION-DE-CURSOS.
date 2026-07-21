# Talma Servicios Aeroportuarios — Cursos No Vigentes & Duración de Cursos

Este repositorio contiene dos proyectos independientes de formación (Talma Aprende), cada uno con su Excel de trabajo y su tablero interactivo (HTML autocontenido, sin dependencias externas, sin necesidad de iniciar sesión para verlo).

## ⚠️ Antes de publicar: datos personales

Los tableros de la carpeta **`Cursos No Vigentes BOG/`** contienen **nombre completo y cédula** de 657 colaboradores. Eso es información personal (dato sensible bajo la Ley 1581 de 2012 / Habeas Data en Colombia).

Si vas a subir esto a GitHub, **usa un repositorio privado** (o una instancia interna tipo GitLab/Bitbucket de Talma), y comparte acceso solo con quien deba verlo. Un repo público expondría las cédulas de todo el personal a cualquiera en internet. El tablero de `Duracion de Cursos/` no tiene datos de personas, así que ese sí es publicable sin este riesgo.

## Estructura

```
Bogota cursos no vigentes/
├── Cursos No Vigentes BOG/
│   ├── Archivos/                                        ← fuentes originales (BI + reporteador + malla curricular)
│   ├── BOG NO CUMPLEN BI - TALMA APRENDE (2026-07-16).xlsx   ← Excel final (incluye hoja "Dashboard" nativa)
│   ├── Tablero Cursos No Vigentes BOG.html                   ← tablero interactivo
│   └── *.py, *.json                                          ← scripts y datos intermedios del cruce
│
└── Duracion de Cursos/
    ├── Tiempo de Duracion de Cursos.xlsx                     ← catálogo de duración de cursos 2026
    ├── Tablero Duracion de Cursos.html                       ← tablero interactivo
    └── *.py, *.json                                          ← scripts y datos intermedios
```

## Ver un tablero

Cada `Tablero *.html` es un archivo autocontenido: todo el código y los datos van adentro, no llama a ningún servidor. Ábrelo con doble clic en cualquier navegador (Chrome, Edge, Firefox) y funciona igual, con o sin internet.

## Publicar con un enlace (GitHub Pages)

Para que cualquiera pueda entrar con un link sin descargar nada:

1. Crea el repositorio en GitHub (**privado** si vas a subir `Cursos No Vigentes BOG/`, ver aviso arriba) y sube esta carpeta.
2. En el repo: **Settings → Pages → Build and deployment → Source: "Deploy from a branch"**, rama `main`, carpeta `/ (root)` → **Save**.
3. Si el repo es privado, GitHub Pages solo queda accesible para quienes tengan acceso al repo (o a la organización, según el plan) — no queda público en internet.
4. GitHub te da un enlace tipo `https://<usuario>.github.io/<repositorio>/`. Cada tablero queda en:
   - `https://<usuario>.github.io/<repositorio>/Duracion de Cursos/Tablero Duracion de Cursos.html`
   - `https://<usuario>.github.io/<repositorio>/Cursos No Vigentes BOG/Tablero Cursos No Vigentes BOG.html`

   Los espacios en el nombre de carpeta/archivo se ven en la barra de direcciones como `%20`; el link funciona igual, pero si prefieres uno más limpio (sin espacios ni tildes) para compartir por WhatsApp o correo, dímelo y renombro los archivos antes de subirlos.
5. Los cambios tardan 1–2 minutos en reflejarse después de cada `git push`.

## Actualizar los datos más adelante

- **Cursos No Vigentes BOG**: descarga el reporteador actualizado desde `https://aprende.talma.com.co/reporteglobal.xlsx`, reemplaza el archivo en `Archivos/`, corre `extract_matches.py` y luego `build_output.py` (ajusta la fecha `HOY` dentro del script primero).
- **Duración de Cursos**: corre `extract_duracion_cursos.py` sobre un reporteador nuevo y luego `build_duracion_excel.py`. Si el Excel ya tiene datos completados a mano, usa `refresh_duracion_excel.py` en su lugar para no perder lo ya revisado.

Después de regenerar cualquier Excel, vuelve a pedir que se actualice el tablero HTML correspondiente para que refleje los datos nuevos.
