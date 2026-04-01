# Estrategia de Acceso y Minería de Datos (Alcaldía de Cali)

Este documento detalla el enfoque estratégico para manejar documentos de baja calidad técnica y alta relevancia fiscal.

## 1. El Desafío de la Transparencia Pasiva
El documento de "Ejecución Presupuestal Septiembre 2025" presenta barreras deliberadas a la minería de datos:
- Ruido visual "Salt and Pepper".
- Rayas verticales de escaneo.
- Baja resolución en tablas densas.

## 2. Acciones Técnicas (Pipeline Python)
- **Visión Artificial (OpenCV)**: Limpieza morfológica para remover rayas y binarización para aislar números.
- **Deep Learning OCR (EasyOCR)**: Uso de redes neuronales para inferir caracteres en bordes difuminados.
- **Validación Cruzada**: Comparar la suma de rubros individuales con los totales liquidados reportados en el mismo documento.

## 3. Acciones Administrativas (Ley 1712 de 2014)
Si la extracción técnica presenta un margen de error inaceptable para fines de auditoría, se recomienda:
- **Solicitud de Datos Abiertos**: Invocar el derecho de acceso a la información pública para obtener los reportes originales de SAP/ERP en formatos procesables (`.xlsx`, `.csv`).
- **Enfoque en Macro-Agregados**: Priorizar la extracción de:
    - *Presupuesto Inicial vs Modificado*.
    - *Total Recaudo Admon. Central*.
    - *Total Gastos de Funcionamiento e Inversión*.

## 4. Referencias Territoriales
- Entidad: Alcaldía de Santiago de Cali.
- Fuente: Departamento Administrativo de Hacienda Municipal.
