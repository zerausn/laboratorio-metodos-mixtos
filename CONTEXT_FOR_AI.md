# Contexto para IA

## Que es este proyecto

Este repositorio es un laboratorio de metodos mixtos orientado a trabajo academico, institucional y de politica publica en Colombia. Su alcance no se limita al OCR de PDFs degradados: ese es solo uno de los frentes del laboratorio.

El objetivo estrategico es construir una plataforma abierta que combine:

- OCR local y reconstruccion documental
- Analisis cualitativo asistido por NLP
- Matrices y cruces para metodos mixtos
- Analisis espacial y territorial
- Exportacion a formatos de oficina y analisis

## Que problema intenta resolver

El proyecto busca reducir dependencia de herramientas de pago para investigacion aplicada. La idea es cubrir, de forma gradual, parte del terreno que hoy ocupan:

- NVivo
- Atlas.ti
- ArcGIS

La apuesta tecnica es trabajar con Python, R, QGIS y bibliotecas open-source.

## Contexto del usuario

- Usuario GitHub: `zerausn`
- Correo: `zerausn@gmail.com`
- Perfil de trabajo: investigacion en administracion publica, economia, sociologia, sistemas, ciencias ambientales y observatorios territoriales
- Preferencia tecnica: software libre, trazabilidad, analisis local y alta calidad documental

## Estado del repositorio

Este repo integra dos lineas de trabajo:

1. La linea principal ya presente en esta maquina, con app Streamlit, backend base y el subproyecto `reconstruccion_documental`.
2. La linea inicial publicada en `zerausn/laboratorio-metodos-mixtos-asp`, desarrollada en el equipo de `andre`, que aporto contexto, reportes de ejemplo y modulos OCR adicionales.

## Componentes principales

- `app.py`: interfaz Streamlit del laboratorio
- `backend/`: modulos de analisis, OCR, exportacion, validacion y reconstruccion
- `reconstruccion_documental/`: pipelines especializados para OCR, Document AI, PDF limpio y Excel
- `docs/`: arquitectura, historia, estrategia de datos y notas de fusion
- `reports/`: ejemplos heredados del laboratorio ASP

## Reglas para futuras IAs

1. No tratar este repositorio como un proyecto solo de OCR.
2. Priorizar herramientas open-source sobre SaaS comercial cuando la calidad sea razonable.
3. Conservar la separacion entre codigo fuente y artefactos pesados de sesion o debugging.
4. Antes de mover o borrar reportes, `Nueva carpeta` o salidas de OCR, confirmar impacto.
5. Documentar toda decision relevante para que otra IA pueda retomar el trabajo sin depender del chat previo.

## Que se fusiono del repo ASP

- Modulos backend faltantes para OCR y reconstruccion
- `requirements_layers.txt`
- `context_and_history.md`
- `docs/ESTRATEGIA_DATOS.md`
- reportes de ejemplo bajo `reports/`

## Que no se fusiono del repo ASP

- `brain/`
- `browser_recordings/`
- `conversations/`
- `scratch/research_lab/data/temp_processing/`
- otros artefactos temporales o de sesion

La razon es simple: son utiles como evidencia de proceso en origen, pero no son el nucleo portable del software.
