# Contexto del Proyecto: Laboratorio Metodos Mixtos

Este laboratorio no es un proyecto de OCR aislado. Es una base de trabajo para investigacion de metodos mixtos que combina analisis cualitativo, cuantitativo, espacial y documental con herramientas open-source.

## Proposito

Desarrollar una plataforma local, trazable y extensible para:

- analizar documentos institucionales
- recuperar PDFs degradados
- apoyar codificacion cualitativa
- producir matrices y cruces para metodos mixtos
- integrar analisis espacial y estadistico

## Motivacion

La motivacion central es reducir dependencia de software de pago. El laboratorio se piensa como una ruta progresiva para reemplazar o complementar:

- NVivo
- Atlas.ti
- ArcGIS

La pila preferida es Python + R + QGIS + librerias libres.

## Evolucion

La evolucion del proyecto tuvo dos lineas:

1. La linea principal que quedo en `zerausn/laboratorio-metodos-mixtos`.
2. Una linea inicial desarrollada en otro computador y publicada en `zerausn/laboratorio-metodos-mixtos-asp`.

La fusion actual toma lo mejor de ambas:

- app y backend principal
- subproyecto de reconstruccion documental
- modulos OCR adicionales
- documentacion de contexto
- reportes de ejemplo

## Alcance actual

- Interfaz Streamlit operable localmente
- Backend NLP, espacial y estadistico
- OCR local con Tesseract y EasyOCR
- Reconstruccion de PDFs y exportacion a Office
- Ejemplos de reportes para trabajo fiscal e institucional

## Criterios de diseno

- prioridad a software libre
- procesamiento local siempre que sea viable
- documentacion suficiente para que otra IA o programador continue el trabajo
- separacion entre codigo reusable y artefactos temporales de sesion
