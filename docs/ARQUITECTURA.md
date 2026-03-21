# Arquitectura Técnica

## Componentes

### 1. Document Parser (`backend/document_parser.py`)
- Usa `pdfminer.six`.
- Enfocado en la extracción de texto plano preservando la codificación UTF-8.

### 2. NLP Module (`backend/nlp_module.py`)
- Preparado para análisis de entidades y sentimientos.
- Probado mediante `tests/test_nlp.py`.

### 3. Spatial Module (`backend/spatial_module.py`)
- Análisis de coordenadas y disposición de elementos en el documento.
- Probado mediante `tests/test_spatial.py`.

### 4. Stats Module (`backend/stats_module.py`)
- Generación de métricas cuantitativas sobre los datos extraídos.
- Probado mediante `tests/test_stats.py`.

## Flujo de Datos
1. El usuario coloca PDFs en el sistema.
2. `document_parser` extrae el contenido.
3. Los módulos de `nlp`, `spatial` y `stats` procesan el contenido de forma paralela o secuencial.
4. Se generan reportes o visualizaciones (Por implementar).
