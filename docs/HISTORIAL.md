# Historia de Tareas y Decisiones

Este documento registra los pasos seguidos durante el desarrollo inicial del laboratorio.

## Fase 1: Extracción de Documentos (Conversación 212546d2)
- **Problema**: `pymupdf` y otros métodos simples fallaban con caracteres especiales (ñ, tildes) y layouts complejos.
- **Acción**: Investigación de librerías alternativas.
- **Solución**: Implementación de `pdfminer.six`. Se verificó la correcta extracción en archivos de prueba.
- **Resultado**: Módulo `backend/document_parser.py` funcional y robusto.

## Fase 2: Infraestructura y GitHub (Conversación actual)
- **Problema**: Proyecto solo local, sin control de versiones ni herramientas de despliegue fáciles.
- **Acciones**:
  - Creación de scripts `.bat` para usuarios Windows.
  - Configuración de `.gitignore` para omitir entornos virtuales.
  - Instalación de `git` y `gh` mediante `winget`.
  - Inicialización de repositorio Git local y remoto.
- **Configuración Git**:
  - Branch principal: `main`
  - Usuario: `zerausn`
  - Email: `zerausn@gmail.com`

## Próximos Pasos (Pendientes)
- Integración de los módulos en una interfaz de usuario (Streamlit o similar).
- Expansión de las capacidades de `stats_module.py`.
- Documentación de uso para el usuario final.
