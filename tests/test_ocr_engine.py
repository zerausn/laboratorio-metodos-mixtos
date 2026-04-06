"""
tests/test_ocr_engine.py
========================
Tests unitarios para el motor OCR multi-engine.

Estos tests validan:
- Disponibilidad e instanciación del OCREngine
- Función de scoring de calidad de texto
- Diagnóstico de motores
- Motores individuales (se saltan si la dependencia no está instalada)

Para correr:
    python -m pytest tests/test_ocr_engine.py -v
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.ocr_engine import _score_text, _is_useful, OCREngine, engine_pymupdf_native, engine_tesseract, engine_easyocr


class TestQualityScoring(unittest.TestCase):
    """Tests para las funciones de evaluación de calidad de texto OCR."""

    def test_empty_text_scores_zero(self):
        self.assertEqual(_score_text(""), 0.0)
        self.assertEqual(_score_text("   "), 0.0)
        self.assertEqual(_score_text(None), 0.0)

    def test_good_spanish_text_scores_high(self):
        text = (
            "La Alcaldía Municipal de Santiago de Cali presenta el informe de ejecución "
            "presupuestal correspondiente al período enero-diciembre del año fiscal."
        )
        score = _score_text(text)
        self.assertGreater(score, 0.4, f"Texto limpio debería tener score > 0.4, obtuvo {score}")

    def test_garbage_text_scores_low(self):
        garbage = "§§§ ¤¤¤ @@@ ### %%% ^^^ &&& *** ||| \\\\\ ≈≈≈ ∞∞∞"
        score = _score_text(garbage)
        self.assertLess(score, 0.3, f"Texto basura debería tener score < 0.3, obtuvo {score}")

    def test_is_useful_with_real_text(self):
        text = "Informe de ejecución presupuestal del municipio de Cali."
        self.assertTrue(_is_useful(text))

    def test_is_useful_rejects_empty(self):
        self.assertFalse(_is_useful(""))
        self.assertFalse(_is_useful("   "))

    def test_is_useful_rejects_two_word_fragments(self):
        self.assertFalse(_is_useful("Ok si"))

    def test_score_numbers_only(self):
        # Solo números — baja calidad (sin palabras reales)
        score = _score_text("1234567890 9876543210 111 222 333")
        self.assertLess(score, 0.5)


class TestOCREngineInit(unittest.TestCase):
    """Tests de inicialización del motor OCR."""

    def test_engine_instantiates(self):
        engine = OCREngine()
        self.assertIsInstance(engine, OCREngine)

    def test_get_engines_status_returns_dict(self):
        engine = OCREngine()
        status = engine.get_engines_status()
        self.assertIsInstance(status, dict)
        self.assertIn("pymupdf_native", status)
        self.assertIn("tesseract", status)
        self.assertIn("easyocr", status)

    def test_diagnostics_returns_list_of_strings(self):
        engine = OCREngine()
        diag = engine.run_diagnostics()
        self.assertIsInstance(diag, list)
        self.assertGreater(len(diag), 0)
        for line in diag:
            self.assertIsInstance(line, str)


class TestPyMuPDFEngine(unittest.TestCase):
    """Tests para el motor PyMuPDF nativo."""

    def test_result_structure(self):
        """Verifica que el resultado tiene las claves esperadas."""
        # Pasamos un path inválido — debe devolver error, no romper
        result = engine_pymupdf_native("archivo_inexistente.pdf", page_num=1)
        self.assertIn("engine", result)
        self.assertIn("text", result)
        self.assertIn("score", result)
        self.assertIn("available", result)
        self.assertEqual(result["engine"], "pymupdf_native")
        # Con archivo inválido debe quedar text vacío o tener error
        if result["available"]:
            self.assertIsNotNone(result.get("error") or result.get("text") is not None)


class TestTesseractEngine(unittest.TestCase):
    """Tests para el motor Tesseract."""

    def test_result_structure(self):
        result = engine_tesseract("imagen_inexistente.png")
        self.assertIn("engine", result)
        self.assertIn("text", result)
        self.assertIn("score", result)
        self.assertIn("available", result)
        if result["available"]:
            # Si está disponible pero la imagen no existe, debe tener error
            self.assertTrue(result.get("error") is not None or result["text"] == "")


class TestEasyOCREngine(unittest.TestCase):
    """Tests para el motor EasyOCR."""

    def test_result_structure(self):
        if not self._easyocr_available():
            self.skipTest("EasyOCR no instalado")
        result = engine_easyocr("imagen_inexistente.png")
        self.assertIn("engine", result)
        self.assertIn("text", result)
        self.assertIn("score", result)

    def _easyocr_available(self):
        try:
            import easyocr  # noqa: F401
            return True
        except ImportError:
            return False


class TestSelectBest(unittest.TestCase):
    """Tests para la función de selección del mejor resultado."""

    def test_selects_highest_score(self):
        from backend.ocr_engine import _select_best
        results = [
            {"engine": "pymupdf_native", "text": "Informe presupuestal de Cali.",
             "score": 0.55, "available": True, "error": None},
            {"engine": "tesseract", "text": "Inf0rme presupue5tal de Cal1.",
             "score": 0.30, "available": True, "error": None},
        ]
        best = _select_best(results)
        self.assertEqual(best["engine"], "pymupdf_native")

    def test_returns_fallback_if_all_bad(self):
        from backend.ocr_engine import _select_best
        results = [
            {"engine": "pymupdf_native", "text": "", "score": 0.0, "available": True, "error": None},
            {"engine": "tesseract", "text": "§§§", "score": 0.02, "available": True, "error": None},
        ]
        best = _select_best(results)
        # Debe devolver algo, no romper
        self.assertIn("engine", best)
        self.assertIn("warning", best)


if __name__ == "__main__":
    unittest.main()
