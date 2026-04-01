# Contexto del Proyecto: Recuperación de PDF Degradado por Capas

## Objetivo
El objetivo de estas modificaciones fue procesar un archivo PDF institucional ("ejecución presupuestal" de la Alcaldía de Cali, con 69 páginas) severamente dañado por fotocopias redundantes (ruido tipo "sal y pimienta" y manchas oscuras grandes) para recuperar su texto y tabularlo, **exclusivamente mediante procesamiento local sin consumir cuotas o tokens de APIs comerciales** (como Google Cloud Vision o AWS Textract).

## Decisión Arquitectónica: Modelo de "Capas"
Siguiendo las instrucciones del investigador, se conceptualizó el documento en dos capas:
1. **Capa Buena (Tipografía):** Las letras y números estables de una fuente común.
2. **Capa Mala (Ruido de fotocopia):** Manchas grandes aleatorias o puntos en el fondo.

Se eligió lenguaje **Python** utilizando la librería **OpenCV** por encima de **R (`magick`)** por su superior capacidad de análisis de componentes conectados y manipulación matricial veloz.

## Librerías Implementadas
Para la inteligencia artificial si necesita entender cómo levantar este proyecto localmente, ver el archivo `requirements_layers.txt`. Allí se explican a detalle los propósitos de `PyMuPDF`, `opencv-python`, `pytesseract`, `pandas`, `xlsxwriter`, `python-docx` y `reportlab`.

## Historial y Decisiones del Chat
1. **Solicitud original (2026-03-22):** El usuario pidió procesar el PDF "página por página", analizando el patrón de la fotocopiadora. Entregarlo en tres formatos: Word, PDF y Excel (CSV) para OCR. Consultó opciones: Google Cloud Vision API, AWS Textract, Adobe Acrobat Pro.
2. **Planificación:** Se planteó un Plan de Implementación donde propusimos separar capas con OpenCV.
3. **Restricción Comercial (El uso de "Tokens"):** El usuario solicitó `revisa que no te vayas a gastar los tokens, antes de subir todo a git hub`. En respuesta, reemplazamos cualquier llamado a Cloud APIs por **Tesseract OCR local**. 
4. **Implementación de Scripts:** 
   - Se construyó `image_cleaner.py` con filtros `cv2.adaptiveThreshold` y `cv2.connectedComponentsWithStats`.
   - Modificamos `export_module.py` para escribir directamente en `.docx`, `.csv`, `.xlsx` y `.pdf`.
   - Se aglutinó todo en `pipeline_layers.py` para procesar el lote completo (69 páginas).
5. **Prueba Completa y Corrección de idioma Tesseract:** Al lanzar la ejecución de las 69 páginas saltó un error porque el sistema no tenía el diccionario en español `spa` para Tesseract. Se corrigió forzando a `lang='eng'` temporalmente, lo cual es suficiente para números, logrando que inicie la extracción masiva en segundo plano.

## Estado de Ejecución
Actualmente, el bot se encuentra ejecutando el script sobre el PDF real en el background. La extracción de una página demora ~30 a 60 segundos debido a la resolución 3x adoptada antes del procesamiento forense por capas. Genera salidas intermedias en `data/layer_pipeline_output`.
