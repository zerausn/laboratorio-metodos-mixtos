"""
tests/test_export_module.py
===========================
Tests unitarios para el módulo de exportación.

Para correr:
    python -m pytest tests/test_export_module.py -v
"""

import sys
import os
import unittest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.export_module import DataExporter


SAMPLE_OCR_RESULTS = [
    {
        "page": 1,
        "best_engine": "pymupdf_native",
        "best_text": "Informe de ejecución presupuestal. Alcaldía de Cali.",
        "best_score": 0.72,
        "combined": False,
        "score_summary": {"pymupdf_native": 0.72, "tesseract": 0.55, "easyocr": 0.40},
    },
    {
        "page": 2,
        "best_engine": "tesseract",
        "best_text": "Datos del período fiscal enero-diciembre.",
        "best_score": 0.60,
        "combined": False,
        "score_summary": {"pymupdf_native": 0.10, "tesseract": 0.60, "easyocr": 0.55},
    },
]

SAMPLE_CODEBOOK = ["Presupuesto", "Ejecución", "Inversión", "Gasto"]

SAMPLE_QUOTES = pd.DataFrame([
    {"Documento": "doc1.pdf", "Fragmento": "El presupuesto fue ejecutado en un 90%.",
     "Codigo": "Ejecución", "Comentario": ""},
    {"Documento": "doc1.pdf", "Fragmento": "La inversión en salud fue prioritaria.",
     "Codigo": "Inversión", "Comentario": "Importante"},
    {"Documento": "doc2.pdf", "Fragmento": "Los gastos corrientes superaron la meta.",
     "Codigo": "Gasto", "Comentario": ""},
])


class TestCSVExport(unittest.TestCase):
    def test_csv_bytes_returns_bytes(self):
        result = DataExporter.to_csv_bytes(
            [{"pagina": 1, "texto": "Hola mundo desde el test."}]
        )
        self.assertIsInstance(result, bytes)
        self.assertIn(b"pagina", result)

    def test_csv_bytes_non_empty(self):
        result = DataExporter.to_csv_bytes(SAMPLE_OCR_RESULTS)
        self.assertGreater(len(result), 50)


class TestExcelExport(unittest.TestCase):
    def test_excel_bytes_returns_bytes_or_none(self):
        result = DataExporter.to_excel_bytes(
            [{"col_a": 1, "col_b": "texto"}]
        )
        # Puede ser None si xlsxwriter/openpyxl no están instalados
        self.assertTrue(result is None or isinstance(result, bytes))

    def test_ocr_results_excel(self):
        result = DataExporter.ocr_results_to_excel_bytes(SAMPLE_OCR_RESULTS)
        if result is not None:
            self.assertIsInstance(result, bytes)
            # Los bytes de un xlsx siempre empiezan con PK (ZIP)
            self.assertTrue(result[:2] == b"PK", "Los bytes de Excel deben empezar con PK (formato ZIP)")


class TestWordExport(unittest.TestCase):
    def test_word_bytes_returns_bytes_or_none(self):
        result = DataExporter.to_word_bytes(SAMPLE_OCR_RESULTS, title="Informe de Prueba")
        # Puede ser None si python-docx no está instalado
        self.assertTrue(result is None or isinstance(result, bytes))

    def test_word_bytes_with_valid_content(self):
        result = DataExporter.to_word_bytes(SAMPLE_OCR_RESULTS)
        if result is not None:
            self.assertGreater(len(result), 100)


class TestCodebookExport(unittest.TestCase):
    def test_codebook_export_structure(self):
        result = DataExporter.codebook_to_excel_bytes(SAMPLE_CODEBOOK, SAMPLE_QUOTES)
        if result is not None:
            self.assertIsInstance(result, bytes)
            self.assertTrue(result[:2] == b"PK")

    def test_codebook_empty_quotes(self):
        empty_quotes = pd.DataFrame(columns=["Documento", "Fragmento", "Codigo", "Comentario"])
        result = DataExporter.codebook_to_excel_bytes(SAMPLE_CODEBOOK, empty_quotes)
        # No debe romper con citas vacías
        self.assertTrue(result is None or isinstance(result, bytes))


if __name__ == "__main__":
    unittest.main()
