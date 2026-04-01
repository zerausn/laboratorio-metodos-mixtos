from pathlib import Path

import cv2
import numpy as np
import pytesseract

try:
    from backend.path_utils import configure_tesseract
except ImportError:
    from path_utils import configure_tesseract


class ImageCleaner:
    def __init__(self, output_dir: str | Path = "cleaned_pages"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def clean_photocopier_noise(self, image_path: str | Path) -> str:
        image_path = Path(image_path)
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"No se pudo leer la imagen {image_path}")

        thresh = cv2.adaptiveThreshold(
            img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            21,
            15,
        )
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            cleaned,
            connectivity=8,
        )

        mask = np.zeros_like(cleaned)
        min_area = 10
        max_area = 5000
        for label in range(1, num_labels):
            area = stats[label, cv2.CC_STAT_AREA]
            if min_area < area < max_area:
                mask[labels == label] = 255

        final_img = cv2.bitwise_not(mask)
        out_path = self.output_dir / f"clean_{image_path.name}"
        cv2.imwrite(str(out_path), final_img)
        return str(out_path)

    def extract_text(self, image_path: str | Path, lang: str = "eng") -> str:
        configure_tesseract()
        try:
            text = pytesseract.image_to_string(str(image_path), lang=lang)
            return text.strip()
        except pytesseract.TesseractNotFoundError:
            return "[ERROR] Tesseract no esta instalado o no esta disponible en PATH."
