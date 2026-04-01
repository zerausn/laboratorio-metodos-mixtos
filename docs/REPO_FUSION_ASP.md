# Fusion del repo ASP

## Fuente

- Repo origen: `zerausn/laboratorio-metodos-mixtos-asp`
- Rama revisada: `windows-andre`
- Commit inspeccionado: `4e171aa24c7f18f78cafedfafcf754f2f47f1bc5`

## Hallazgo principal

El repo ASP no era un proyecto completamente distinto. Era la formulacion inicial del laboratorio en otro equipo, con esta situacion:

- `app.py` y `requirements.txt` ya habian sido trasladados al repo principal
- Los cuatro modulos base ya existentes en `backend/` eran identicos entre ambas repos
- La diferencia real estaba en modulos OCR faltantes, contexto documental y algunos reportes de ejemplo

## Material integrado al repo principal

- `backend/diagnostic_ocr.py`
- `backend/export_module.py`
- `backend/final_report_generator.py`
- `backend/full_recovery_manager.py`
- `backend/image_cleaner.py`
- `backend/layout_reconstructor.py`
- `backend/ocr_engine.py`
- `backend/path_utils.py`
- `backend/pipeline_layers.py`
- `backend/validator.py`
- `requirements_layers.txt`
- `context_and_history.md`
- `docs/ESTRATEGIA_DATOS.md`
- `reports/` heredados del laboratorio ASP

## Adaptaciones hechas durante la fusion

- Se eliminaron rutas duras de `C:\Users\andre\...`
- Se pasaron rutas a un esquema relativo al repo actual
- Se normalizaron imports para que funcionen como parte del backend actual
- Se dejaron utilidades de rutas en `backend/path_utils.py`
- Se ampliaron dependencias en `requirements.txt` para OCR local y reconstruccion

## Material no integrado a proposito

- `brain/`
- `browser_recordings/`
- `conversations/`
- `implicit/`
- `prompting/`
- `knowledge/`
- `scratch/research_lab/data/temp_processing/`

## Motivo de exclusion

Esas carpetas representan sesiones de Antigravity, grabaciones, estados temporales y datos de procesamiento. Aportan contexto historico, pero no deben dominar el repo principal ni volverlo un volcado de estados locales.

## Resultado

El repo principal `zerausn/laboratorio-metodos-mixtos` queda como la base consolidada del laboratorio, con:

- la interfaz principal
- el backend amplio
- el subproyecto de reconstruccion documental
- la documentacion necesaria para que otra IA o programador continue el trabajo
