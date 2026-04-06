# Laboratorio Métodos Mixtos - AI Instructions

Este proyecto es una plataforma para análisis cualitativo y espacial. Siga estas reglas para mantener la consistencia.

## Comandos de Ejecución
- **Iniciar Aplicación (Streamlit):** `streamlit run app.py` o usar `Iniciar_Lab.bat`.
- **Tests:** `pytest tests/`.

## Reglas de Desarrollo
- **Backend Modular:** La lógica de OCR y procesamiento está en `backend/`. No mezcles lógica pesada en `app.py`.
- **Documentación Local:** Esta IA debe leer `docs/ARCHITECTURE.md` antes de modificar módulos del backend.
- **Formato de Salida:** Los reportes generados van a la carpeta `reports/`.

## Estado del Proyecto
- **OCR:** Implementado el sistema multiorquesta en `backend/ocr_engine.py`.
- **Integración:** El frontend en Streamlit está conectado al backend de reconstrucción documental.
- **Progreso:** Revisa `docs/PROGRESS.md`.
