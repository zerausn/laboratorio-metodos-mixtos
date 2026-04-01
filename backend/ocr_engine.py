from __future__ import annotations

from pathlib import Path

import cv2
import easyocr
import fitz
import numpy as np
import pytesseract
from PIL import Image

try:
    from backend.path_utils import configure_tesseract, data_dir
except ImportError:
    from path_utils import configure_tesseract, data_dir


class DegradedDocProcessor:
    def __init__(self, languages=None, gpu: bool = False):
        self.languages = languages or ["es"]
        self.reader = easyocr.Reader(self.languages, gpu=gpu, verbose=False)

    def pdf_to_images(self, pdf_path, output_dir, force_rebuild: bool = False):
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(pdf_path)
        image_paths = []
        for index in range(len(doc)):
            img_path = output_dir / f"page_{index + 1}.png"
            if force_rebuild or not img_path.exists():
                page = doc.load_page(index)
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
                pix.save(str(img_path))
            image_paths.append(str(img_path))
        return image_paths

    def get_page_image(self, pdf_path, page_num, output_dir):
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        img_path = output_dir / f"page_{page_num}.png"
        if not img_path.exists():
            doc = fitz.open(pdf_path)
            page = doc.load_page(page_num - 1)
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
            pix.save(str(img_path))
        return str(img_path)

    def clean_image_forensic(self, img_path):
        img_path = Path(img_path)
        img = cv2.imread(str(img_path))
        if img is None:
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, h=15)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        thresh = cv2.adaptiveThreshold(
            enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            10,
        )

        thresh_inv = cv2.bitwise_not(thresh)
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
        lines = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
        clean_inv = cv2.subtract(thresh_inv, lines)
        final = cv2.bitwise_not(clean_inv)

        configure_tesseract()
        try:
            osd = pytesseract.image_to_osd(Image.fromarray(final))
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

        coords = np.column_stack(np.where(final == 0))
        if len(coords) > 0:
            angle = cv2.minAreaRect(coords)[-1]
            angle = -(90 + angle) if angle < -45 else -angle
            height, width = final.shape[:2]
            center = (width // 2, height // 2)
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            final = cv2.warpAffine(
                final,
                matrix,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE,
            )

        final = cv2.medianBlur(final, 3)
        clean_path = img_path.with_name(f"{img_path.stem}_forensic.png")
        cv2.imwrite(str(clean_path), final)
        return str(clean_path)

    def extract_text_multi(self, img_path):
        configure_tesseract()
        config = "--oem 3 --psm 3"
        try:
            text_tess = pytesseract.image_to_string(Image.open(img_path), config=config, lang="eng")
        except Exception as exc:
            text_tess = f"[Tesseract fallo: {exc}]"

        text_easy = self.reader.readtext(img_path, detail=0)
        text_easy_str = " ".join(text_easy)

        if "ILAC" in text_easy_str or "OTIRTSIID" in text_easy_str or "ILAC" in text_tess:
            img = cv2.imread(str(img_path))
            flipped = cv2.flip(img, 1)
            flipped_path = str(Path(img_path).with_name(f"{Path(img_path).stem}_flipped.png"))
            cv2.imwrite(flipped_path, flipped)
            return self.extract_text_multi(flipped_path)

        return {"easyocr": text_easy_str, "tesseract": text_tess}

    def extract_text(self, img_path):
        return "\n".join(self.reader.readtext(img_path, detail=0))

    def process_document(self, pdf_path, page_range=None, output_dir=None):
        pdf_path = Path(pdf_path)
        temp_dir = Path(output_dir) if output_dir else data_dir() / "temp_processing"
        pages = self.pdf_to_images(pdf_path, temp_dir)

        all_text = []
        selected = set(page_range or [])
        for index, page_path in enumerate(pages, start=1):
            if selected and index not in selected:
                continue
            clean_path = self.clean_image_forensic(page_path)
            results = self.extract_text_multi(clean_path)
            combined_text = (
                "--- EASYOCR ---\n"
                f"{results['easyocr']}\n\n"
                "--- TESSERACT ---\n"
                f"{results['tesseract']}"
            )
            all_text.append(
                {
                    "page": index,
                    "text": combined_text,
                    "easyocr": results["easyocr"],
                    "tesseract": results["tesseract"],
                    "img_path": page_path,
                    "clean_path": clean_path,
                }
            )
        return all_text


if __name__ == "__main__":
    processor = DegradedDocProcessor()
    pdf_path = data_dir() / "ejecucion_presupuestal.pdf"
    results = processor.process_document(pdf_path, page_range=[3, 36])
    for result in results:
        print(f"--- PAGINA {result['page']} ---")
        print(result["text"][:500] + "...")
