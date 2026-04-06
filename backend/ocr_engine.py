"""
backend/ocr_engine.py
=====================
Motor OCR multi-engine con redundancia y control de calidad.

Estrategia de capas (de más rápido a más robusto):
  1. PyMuPDF  — extracción de texto nativo del PDF (sin imagen). Cero dependencias externas extra.
  2. Tesseract — OCR clásico, muy estable en Windows. Requiere Tesseract instalado en el SO.
  3. EasyOCR   — OCR por deep learning, mejor en documentos degradados. Requiere torch + easyocr.

El motor evalúa la calidad de cada resultado y elige el mejor, o los combina.
Si un motor no está disponible (no instalado), se omite sin romper la ejecución.

Uso típico:
    from backend.ocr_engine import OCREngine
    engine = OCREngine()
    results = engine.process_pdf("archivo.pdf", page_range=[1, 2, 3])
    for r in results:
        print(r["best_text"])
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Optional

# ── Importaciones opcionales — cada una puede fallar sin romper el módulo ──────

try:
    import fitz  # PyMuPDF
    _PYMUPDF_OK = True
except ImportError:
    fitz = None
    _PYMUPDF_OK = False

try:
    import cv2
    _CV2_OK = True
except ImportError:
    cv2 = None
    _CV2_OK = False

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    np = None
    _NUMPY_OK = False

try:
    from PIL import Image as PILImage
    _PIL_OK = True
except ImportError:
    PILImage = None
    _PIL_OK = False

try:
    import pytesseract
    _TESSERACT_OK = True
except ImportError:
    pytesseract = None
    _TESSERACT_OK = False

try:
    import easyocr
    _EASYOCR_OK = True
except ImportError:
    easyocr = None
    _EASYOCR_OK = False

try:
    from backend.path_utils import configure_tesseract, data_dir
except ImportError:
    try:
        from path_utils import configure_tesseract, data_dir
    except ImportError:
        configure_tesseract = lambda: None  # noqa: E731
        data_dir = lambda: Path("data")    # noqa: E731


# ── Funciones de calidad ───────────────────────────────────────────────────────

def _score_text(text: str) -> float:
    """
    Evalúa la calidad de un texto OCR entre 0.0 (inútil) y 1.0 (excelente).

    Criterios:
    - longitud mínima (texto vacío = 0)
    - ratio de caracteres alfanuméricos vs total
    - ratio de palabras reconocibles en español/inglés (longitud > 2)
    - penalización por exceso de caracteres de control o símbolos raros
    """
    if not text or not text.strip():
        return 0.0

    text = text.strip()
    total = max(len(text), 1)

    # Ratio alfanumérico
    alnum = sum(1 for c in text if c.isalnum())
    alnum_ratio = alnum / total

    # Ratio de "palabras legibles" (≥ 3 caracteres alfabéticos)
    words = re.findall(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]{3,}', text)
    word_density = min(len(words) / max(total / 6, 1), 1.0)

    # Penalización por símbolos raros (no ASCII imprimibles que no sean letras latinas)
    def _is_expected(c):
        if c.isalnum() or c in ' \n\t.,;:()[]{}!?-_/@#$%&*+=<>\'"\\':
            return True
        try:
            return unicodedata.category(c).startswith('L')  # letras Unicode
        except Exception:
            return False

    strange = sum(1 for c in text if not _is_expected(c))
    strange_penalty = strange / total

    score = (alnum_ratio * 0.4) + (word_density * 0.5) - (strange_penalty * 0.2)
    return max(0.0, min(1.0, round(score, 3)))


def _is_useful(text: str, min_score: float = 0.15, min_words: int = 3) -> bool:
    """Devuelve True si el texto tiene calidad suficiente para ser considerado."""
    if not text or not text.strip():
        return False
    words = re.findall(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]{3,}', text)
    return _score_text(text) >= min_score and len(words) >= min_words


# ── Limpieza de imágenes ───────────────────────────────────────────────────────

def _preprocess_image(img_path: str) -> Optional[str]:
    """
    Aplica preprocesamiento forense a una imagen PNG y guarda la versión limpia.
    Requiere OpenCV y NumPy. Si no están disponibles, devuelve la ruta original.
    """
    if not (_CV2_OK and _NUMPY_OK and _PIL_OK):
        return img_path

    try:
        img = cv2.imread(str(img_path))
        if img is None:
            return img_path

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, h=15)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        thresh = cv2.adaptiveThreshold(
            enhanced, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 10,
        )

        # Eliminar líneas verticales largas (artefactos de fotocopia)
        thresh_inv = cv2.bitwise_not(thresh)
        vkernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
        lines = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, vkernel, iterations=1)
        clean_inv = cv2.subtract(thresh_inv, lines)
        final = cv2.bitwise_not(clean_inv)

        # Corrección de rotación (Tesseract OSD)
        if _TESSERACT_OK:
            configure_tesseract()
            try:
                osd = pytesseract.image_to_osd(PILImage.fromarray(final))
                angle = 0
                for line in osd.splitlines():
                    if line.startswith("Rotate:"):
                        angle = int(line.split(":", 1)[1].strip())
                        break
                if angle == 90:
                    final = cv2.rotate(final, cv2.ROTATE_90_CLOCKWISE)
                elif angle == 180:
                    final = cv2.rotate(final, cv2.ROTATE_180)
                elif angle == 270:
                    final = cv2.rotate(final, cv2.ROTATE_90_COUNTERCLOCKWISE)
            except Exception:
                pass

        final = cv2.medianBlur(final, 3)
        clean_path = str(Path(img_path).with_name(Path(img_path).stem + "_clean.png"))
        cv2.imwrite(clean_path, final)
        return clean_path

    except Exception as exc:
        print(f"[ocr_engine] Advertencia al preprocesar imagen: {exc}")
        return img_path


# ── Motores individuales ───────────────────────────────────────────────────────

def engine_pymupdf_native(pdf_path: str, page_num: int) -> dict:
    """Motor 1: extracción de texto nativo del PDF (sin OCR de imagen)."""
    result = {"engine": "pymupdf_native", "text": "", "score": 0.0, "available": _PYMUPDF_OK, "error": None}
    if not _PYMUPDF_OK:
        result["error"] = "PyMuPDF no instalado"
        return result
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num - 1)
        text = page.get_text("text")
        doc.close()
        result["text"] = text.strip()
        result["score"] = _score_text(text)
    except Exception as exc:
        result["error"] = str(exc)
    return result


def engine_tesseract(img_path: str, lang: str = "spa+eng") -> dict:
    """Motor 2: Tesseract OCR local. Soporta español e inglés simultáneo."""
    result = {"engine": "tesseract", "text": "", "score": 0.0, "available": _TESSERACT_OK, "error": None}
    if not (_TESSERACT_OK and _PIL_OK):
        result["error"] = "Tesseract o PIL no disponibles"
        return result
    configure_tesseract()
    try:
        img = PILImage.open(img_path)
        # Intentar con spa+eng, si falla intentar solo eng
        try:
            text = pytesseract.image_to_string(img, config="--oem 3 --psm 3", lang=lang)
        except pytesseract.TesseractError:
            try:
                text = pytesseract.image_to_string(img, config="--oem 3 --psm 3", lang="eng")
                result["engine"] = "tesseract_eng_only"
            except Exception as e2:
                result["error"] = str(e2)
                return result
        result["text"] = text.strip()
        result["score"] = _score_text(text)
    except Exception as exc:
        result["error"] = str(exc)
    return result


def engine_easyocr(img_path: str, langs: list = None, gpu: bool = False) -> dict:
    """Motor 3: EasyOCR — mejor para documentos degradados y rotados."""
    result = {"engine": "easyocr", "text": "", "score": 0.0, "available": _EASYOCR_OK, "error": None}
    if not _EASYOCR_OK:
        result["error"] = "EasyOCR no instalado (pip install easyocr)"
        return result
    try:
        langs = langs or ["es", "en"]
        reader = easyocr.Reader(langs, gpu=gpu, verbose=False)
        raw = reader.readtext(img_path, detail=0)
        text = " ".join(raw)
        result["text"] = text.strip()
        result["score"] = _score_text(text)
    except Exception as exc:
        result["error"] = str(exc)
    return result


# ── Motor combinado ────────────────────────────────────────────────────────────

def _select_best(results: list[dict]) -> dict:
    """
    Elige el resultado con mayor score. Si varios son similares (diff < 0.1),
    combina sus textos de forma ponderada.
    """
    valid = [r for r in results if r.get("text") and _is_useful(r["text"])]
    if not valid:
        # Ningún motor produjo texto útil — devolver el de mayor score igual
        fallback = max(results, key=lambda r: r.get("score", 0.0))
        fallback["combined"] = False
        fallback["warning"] = "Ningún motor produjo texto de calidad aceptable."
        return fallback

    valid.sort(key=lambda r: r["score"], reverse=True)
    best = valid[0]

    # Si hay varios con scores cercanos, combinar con separador de fuente
    high_quality = [r for r in valid if best["score"] - r["score"] <= 0.1]
    if len(high_quality) > 1:
        combined_text = "\n\n".join(
            f"[{r['engine'].upper()}]\n{r['text']}" for r in high_quality
        )
        best = best.copy()
        best["text"] = combined_text
        best["combined"] = True
        best["engines_used"] = [r["engine"] for r in high_quality]
    else:
        best["combined"] = False

    return best


# ── Clase principal ────────────────────────────────────────────────────────────

class OCREngine:
    """
    Motor OCR multi-engine con redundancia y control de calidad automático.

    Parámetros:
        gpu (bool): Usar GPU para EasyOCR (requiere CUDA). Default False.
        langs (list): Idiomas para EasyOCR. Default ["es", "en"].
        tesseract_lang (str): Idioma(s) para Tesseract. Default "spa+eng".
        temp_dir (str/Path): Directorio temporal para imágenes de páginas.
    """

    def __init__(
        self,
        gpu: bool = False,
        langs: list = None,
        tesseract_lang: str = "spa+eng",
        temp_dir=None,
    ):
        self.gpu = gpu
        self.langs = langs or ["es", "en"]
        self.tesseract_lang = tesseract_lang
        self.temp_dir = Path(temp_dir) if temp_dir else data_dir() / "temp_processing"

    # ── Disponibilidad de motores ──────────────────────────────────────────────

    def get_engines_status(self) -> dict:
        """Devuelve un dict con la disponibilidad de cada motor."""
        return {
            "pymupdf_native": _PYMUPDF_OK,
            "tesseract": _TESSERACT_OK and _PIL_OK,
            "easyocr": _EASYOCR_OK,
            "image_preprocessing": _CV2_OK and _NUMPY_OK,
        }

    # ── Conversión PDF → imagen ────────────────────────────────────────────────

    def pdf_to_image(self, pdf_path: str, page_num: int, force_rebuild: bool = False) -> Optional[str]:
        """Convierte una página del PDF a PNG. Requiere PyMuPDF."""
        if not _PYMUPDF_OK:
            return None
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        img_path = self.temp_dir / f"page_{page_num}.png"
        if force_rebuild or not img_path.exists():
            doc = fitz.open(pdf_path)
            page = doc.load_page(page_num - 1)
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # 3x = ~216 DPI
            pix.save(str(img_path))
            doc.close()
        return str(img_path)

    # ── Procesar una página ────────────────────────────────────────────────────

    def process_page(self, pdf_path: str, page_num: int, force_rebuild: bool = False) -> dict:
        """
        Ejecuta todos los motores disponibles sobre una página y devuelve:
        - results_by_engine: dict con resultado de cada motor
        - best: el resultado elegido como mejor
        - page: número de página
        - score_summary: resumen de scores
        """
        pdf_path = str(pdf_path)
        all_results = []

        # Motor 1: PyMuPDF nativo (más rápido, solo para PDFs con texto incrustado)
        r1 = engine_pymupdf_native(pdf_path, page_num)
        all_results.append(r1)

        # Convertir a imagen para los motores basados en imagen
        img_path = self.pdf_to_image(pdf_path, page_num, force_rebuild)

        if img_path:
            # Preprocesar imagen (denoising, threshold, etc.)
            clean_path = _preprocess_image(img_path)

            # Motor 2: Tesseract
            r2 = engine_tesseract(clean_path or img_path, lang=self.tesseract_lang)
            all_results.append(r2)

            # Motor 3: EasyOCR
            r3 = engine_easyocr(clean_path or img_path, langs=self.langs, gpu=self.gpu)
            all_results.append(r3)
        else:
            all_results.append({"engine": "tesseract", "available": False, "text": "", "score": 0.0,
                                 "error": "No se pudo generar imagen (PyMuPDF no disponible)"})
            all_results.append({"engine": "easyocr", "available": False, "text": "", "score": 0.0,
                                 "error": "No se pudo generar imagen"})

        best = _select_best(all_results)

        return {
            "page": page_num,
            "best_engine": best.get("engine"),
            "best_text": best.get("text", ""),
            "best_score": best.get("score", 0.0),
            "combined": best.get("combined", False),
            "warning": best.get("warning"),
            "results_by_engine": {r["engine"]: r for r in all_results},
            "score_summary": {r["engine"]: r.get("score", 0.0) for r in all_results},
            "img_path": img_path,
        }

    # ── Procesar documento completo ────────────────────────────────────────────

    def process_pdf(self, pdf_path: str, page_range: list = None, force_rebuild: bool = False) -> list:
        """
        Procesa un PDF completo o un rango de páginas.

        Args:
            pdf_path: Ruta al archivo PDF.
            page_range: Lista de números de página [1,2,5,...]. Si None, procesa todo.
            force_rebuild: Si True, regenera las imágenes aunque ya existan.

        Returns:
            Lista de dicts, uno por página, con campo 'best_text', 'score_summary', etc.
        """
        pdf_path = Path(pdf_path)
        if not _PYMUPDF_OK:
            raise ImportError("PyMuPDF es requerido para abrir PDFs. Instala con: pip install pymupdf")

        doc = fitz.open(str(pdf_path))
        total_pages = len(doc)
        doc.close()

        pages_to_process = sorted(set(page_range)) if page_range else list(range(1, total_pages + 1))
        # Validar rango
        pages_to_process = [p for p in pages_to_process if 1 <= p <= total_pages]

        results = []
        for page_num in pages_to_process:
            page_result = self.process_page(str(pdf_path), page_num, force_rebuild)
            results.append(page_result)
            print(f"  [OCR] Página {page_num}/{total_pages} — "
                  f"mejor motor: {page_result['best_engine']} (score: {page_result['best_score']:.2f})")

        return results

    # ── Test rápido de disponibilidad de motores ───────────────────────────────

    def run_diagnostics(self) -> list:
        """
        Ejecuta diagnóstico de todos los motores sin procesar ningún documento.
        Devuelve lista de mensajes de estado.
        """
        status = self.get_engines_status()
        report = []
        for engine_name, ok in status.items():
            icon = "✅" if ok else "❌"
            report.append(f"{icon} {engine_name}: {'disponible' if ok else 'no disponible'}")

        if not any([_PYMUPDF_OK, _TESSERACT_OK, _EASYOCR_OK]):
            report.append("⚠️ ADVERTENCIA: Ningún motor OCR está disponible. Instala al menos PyMuPDF.")
        elif not _TESSERACT_OK and not _EASYOCR_OK:
            report.append("⚠️ Solo PyMuPDF disponible: solo funcionará con PDFs que tengan texto incrustado.")

        return report


# ── Alias de compatibilidad con código anterior ────────────────────────────────

class DegradedDocProcessor(OCREngine):
    """Alias de compatibilidad para código que ya usaba DegradedDocProcessor."""
    pass


# ── Ejecución directa ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    engine = OCREngine()
    print("=== Diagnóstico de motores OCR ===")
    for line in engine.run_diagnostics():
        print(line)

    pdf_path = data_dir() / "ejecucion_presupuestal.pdf"
    if pdf_path.exists():
        print(f"\nProcesando {pdf_path.name} (páginas 1-3)...")
        results = engine.process_pdf(str(pdf_path), page_range=[1, 2, 3])
        for r in results:
            print(f"\n── Página {r['page']} (motor: {r['best_engine']}, score: {r['best_score']:.2f}) ──")
            print(r["best_text"][:400] + "..." if len(r["best_text"]) > 400 else r["best_text"])
    else:
        print(f"\n(No se encontró PDF de prueba en {pdf_path})")
