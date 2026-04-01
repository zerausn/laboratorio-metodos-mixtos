# Laboratorio de Metodos Mixtos

Plataforma open-source para analisis documental, OCR forense, codificacion cualitativa, NLP en espanol, estadistica, y analisis espacial.

Este repositorio ya no representa solo el trabajo reciente de OCR/PDF. Tambien consolida la linea original del laboratorio que nacio en otro equipo y se publico en `zerausn/laboratorio-metodos-mixtos-asp`.

## Objetivo

El laboratorio busca reemplazar dependencias de software de pago con una pila abierta y auditable:

- Python para OCR, NLP, mineria de datos y automatizacion documental.
- R para estadistica y metodos mixtos.
- QGIS y GeoPandas para analisis espacial y cartografia.
- Streamlit para una interfaz local que permita usar el laboratorio sin depender de servicios comerciales.

La meta de fondo es construir un entorno que pueda cubrir parte del espacio funcional de NVivo, Atlas.ti y, cuando sea viable, flujos que hoy suelen resolverse en ArcGIS.

## Estado actual

- App Streamlit en [app.py](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/app.py)
- Backend mixto en [backend](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/backend)
- Subproyecto OCR/reconstruccion en [reconstruccion_documental](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/reconstruccion_documental)
- Documentacion tecnica en [docs](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/docs)
- Ejemplos y reportes heredados del trabajo inicial en [reports](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/reports)
- JSON grandes de Document AI en `Nueva carpeta`, manejados con `git-lfs`

## Estructura

```text
Laboratorio metodos mixtos/
├─ app.py
├─ backend/
├─ docs/
├─ reports/
├─ reconstruccion_documental/
├─ Nueva carpeta/
├─ requirements.txt
├─ requirements_layers.txt
├─ context_and_history.md
└─ workspace.code-workspace
```

## Fusiones relevantes

- Fuente 1: `zerausn/laboratorio-metodos-mixtos`
  Contenia el trabajo principal que ya estaba en esta maquina: app, backend base, docs, y el subproyecto de reconstruccion documental.
- Fuente 2: `zerausn/laboratorio-metodos-mixtos-asp`
  Contenia la formulacion inicial del laboratorio en el equipo de `andre`, con modulos OCR adicionales, contexto para IA y ejemplos de reportes.

La integracion actual conserva el codigo y la documentacion utiles de ambas lineas y deja por fuera artefactos de sesion o temporales pesados del repo ASP.

## Instalacion rapida

```powershell
cd "C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements_layers.txt
python -m spacy download es_core_news_lg
streamlit run app.py
```

## Dependencias de sistema

- Tesseract OCR para OCR local avanzado
- FFMPEG para transcripcion con Whisper
- R si se quiere usar el modulo estadistico mixto con `rpy2`
- QGIS si se quiere ampliar la capa espacial por fuera de la app base

## Documentos clave

- Contexto general para IA: [CONTEXT_FOR_AI.md](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/CONTEXT_FOR_AI.md)
- Notas de fusion del repo ASP: [REPO_FUSION_ASP.md](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/docs/REPO_FUSION_ASP.md)
- Guia de Antigravity y Git: [ANTIGRAVITY_GIT_SETUP.md](C:/Users/ZN-/Documents/Antigravity/Laboratorio%20metodos%20mixtos/docs/ANTIGRAVITY_GIT_SETUP.md)
