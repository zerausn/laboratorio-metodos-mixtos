# Contexto del Proyecto: Laboratorio Métodos Mixtos

Este documento resume el propósito, la evolución y las decisiones técnicas tomadas durante el desarrollo de este laboratorio para que futuras inteligencias artificiales o colaboradores puedan entender el "por qué" detrás del código.

## Propósito
El objetivo de este laboratorio es desarrollar una herramienta robusta para el análisis de documentos (principalmente PDFs) utilizando métodos mixtos (cuantitativos y cualitativos). Esto incluye extracción de texto, procesamiento de lenguaje natural (NLP), análisis espacial y estadísticas descriptivas.

## Arquitectura y Estructura
- **`app.py`**: El punto de entrada de la aplicación.
- **`backend/`**: Contiene la lógica modular:
  - `document_parser.py`: Encargado de la extracción de texto.
  - `nlp_module.py`: Procesa el texto (entidades, sentimientos, etc.).
  - `spatial_module.py`: Realiza análisis geométrico o espacial.
  - `stats_module.py`: Genera métricas y estadísticas.
- **`tests/`**: Suite de pruebas unitarias para cada módulo.

## Hitos y Decisiones Clave

### 1. Robustez en la Extracción de PDF
Originalmente, el sistema enfrentó problemas con caracteres especiales en español (tildes, ñ) y estructuras complejas.
- **Decisión**: Se migró a `pdfminer.six` para una extracción más precisa y de bajo nivel, priorizando la integridad del texto sobre la velocidad simple de otras librerías.

### 2. Flujo de Trabajo Basado en Pruebas
Se implementó una estructura de tests desde el inicio para asegurar que cada módulo de análisis (NLP, Espacial, Stats) funcione de forma independiente antes de integrarse en la UI.

### 3. Automatización de Entorno
Se incluyeron archivos `.bat` para facilitar la instalación (`Instalacion_PC_Nueva.bat`) e inicio (`Iniciar_Lab.bat`) en máquinas Windows, asegurando que cualquier usuario pueda levantar el laboratorio sin conocimientos profundos de Python.

## Decisiones de Git
- El proyecto se migró a GitHub el 21 de marzo de 2026.
- Se utiliza la rama `main` como rama principal.
- Se configuró el usuario `zerausn` para los commits oficiales.

## Estado Actual
El sistema es capaz de procesar textos, realizar análisis básicos y está listo para ser expandido con una interfaz gráfica o procesos de análisis más complejos.
