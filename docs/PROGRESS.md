# Historia de Tareas y Decisiones

## Fase 1: Nacimiento del laboratorio

El laboratorio nacio como un entorno local para analisis documental y metodos
mixtos, con una app Streamlit y un backend modular para NLP, analisis espacial
y estadistica.

## Fase 2: Primera publicacion en GitHub

Se publico una linea inicial del trabajo en
`zerausn/laboratorio-metodos-mixtos-asp`, en la rama `windows-andre`,
incluyendo:

- app Streamlit
- backend base
- modulos OCR adicionales
- documentacion para IA
- reportes de ejemplo

## Fase 3: Consolidacion del repo principal

En `zerausn/laboratorio-metodos-mixtos` se consolido el trabajo local mas
reciente, incluyendo:

- la app principal
- los modulos base del backend
- el subproyecto `reconstruccion_documental`
- integracion con JSON de Document AI
- reconstruccion limpia de PDF y Excel

## Fase 4: Caso OCR de Cali 2025

Se trabajo un caso fuerte de recuperacion documental sobre un PDF presupuestal
degradado de 69 paginas, con:

- OCR local
- pipelines con y sin JSON
- reconstruccion limpia pagina por pagina
- exportaciones a PDF, Excel y Word

## Fase 5: Fusion ASP -> repo principal

Se reviso `zerausn/laboratorio-metodos-mixtos-asp` y se encontro que:

- `app.py` y `requirements.txt` ya estaban fusionados
- los 4 modulos base compartidos eran identicos
- faltaban modulos OCR, contexto y reportes de ejemplo

La fusion incorporo:

- modulos backend OCR faltantes
- `requirements_layers.txt`
- `context_and_history.md`
- `docs/ESTRATEGIA_DATOS.md`
- `reports/` del laboratorio ASP

Y dejo por fuera:

- `brain/`
- `browser_recordings/`
- `conversations/`
- datos temporales y artefactos de sesion

## Fase 6: Contexto de agentes y automatizacion segura

- `AGENTS.md` y archivos de compatibilidad multiagente ya quedaron versionados.
- `.antigravity/automation.json` agregado con validacion baseline segura.
- Workflow `agent-validate.yml` agregado para PRs.
- El repo queda preparado para publicacion por rama corta y PR, sin push
  automatico directo a `main`.
