# Arquitectura Tecnica

## Vision general

El laboratorio tiene dos capas principales:

1. Una capa de interfaz y analisis mixto para operar documentos, corpus y capas espaciales.
2. Una capa especializada de OCR y reconstruccion documental para PDFs degradados.

## Componentes principales

### 1. Interfaz principal

- `app.py`
- Streamlit como superficie de trabajo local
- Modulos visibles: NLP, codificacion cualitativa, analisis espacial, metodos mixtos y flujos documentales

### 2. Backend base

- `backend/document_parser.py`
  Extrae texto desde PDF, Word, PowerPoint, Excel, CSV, texto y audio/video transcrito.
- `backend/nlp_module.py`
  Procesamiento NLP para entidades, frecuencias, sentimiento y apoyo a codificacion.
- `backend/spatial_module.py`
  Carga y operaciones sobre datos espaciales.
- `backend/stats_module.py`
  Estadistica y apoyo cuantitativo.

### 3. Backend OCR y reconstruccion

Linea heredada y adaptada del repo ASP:

- `backend/ocr_engine.py`
- `backend/image_cleaner.py`
- `backend/pipeline_layers.py`
- `backend/export_module.py`
- `backend/layout_reconstructor.py`
- `backend/validator.py`
- `backend/diagnostic_ocr.py`
- `backend/final_report_generator.py`
- `backend/full_recovery_manager.py`
- `backend/path_utils.py`

Esta capa sirve para trabajar documentos deteriorados sin depender de APIs comerciales.

### 4. Subproyecto especializado de reconstruccion

- `reconstruccion_documental/`

Aqui viven pipelines mas recientes y comparativos:

- OCR apoyado en Document AI JSON
- reconstruccion limpia de PDF pagina por pagina
- reconstruccion sin JSON para comparar enfoques
- exportacion a Excel, PDF y Word

## Flujo de alto nivel

1. El usuario carga documentos o datos desde la app o scripts.
2. `document_parser` y los modulos de backend transforman el insumo.
3. Si el documento esta degradado, entra la capa OCR/reconstruccion.
4. Los resultados pueden ir a:
   - analisis cualitativo
   - reportes de auditoria
   - tablas para Excel
   - reconstruccion documental limpia
   - cruces espaciales o estadisticos

## Decision arquitectonica importante

El repo consolidado mantiene juntos:

- el software reusable
- la documentacion de contexto
- un subproyecto fuerte de OCR

pero evita incorporar artefactos pesados de sesion de Antigravity o datos temporales de origen que no agregan valor como software portable.
