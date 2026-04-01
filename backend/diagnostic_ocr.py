import tempfile
from pathlib import Path

import cv2
import pytesseract
from PIL import Image

try:
    from backend.path_utils import configure_tesseract, data_dir
except ImportError:
    from path_utils import configure_tesseract, data_dir


def test_ocr_variations(img_path):
    configure_tesseract()
    img = cv2.imread(str(img_path))
    if img is None:
        return "Error loading image"

    variations = {
        "original": img,
        "flipped_h": cv2.flip(img, 1),
        "flipped_v": cv2.flip(img, 0),
        "rotated_180": cv2.rotate(img, cv2.ROTATE_180),
    }

    report = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        for name, image in variations.items():
            temp_path = Path(tmp_dir) / f"temp_vari_{name}.png"
            cv2.imwrite(str(temp_path), image)
            for psm in (3, 6):
                config = f"--oem 3 --psm {psm}"
                try:
                    text = pytesseract.image_to_string(
                        Image.open(temp_path),
                        lang="eng",
                        config=config,
                    )
                    clean_text = " ".join(text.split())[:100]
                    report.append(f"Orientacion: {name}, PSM: {psm} -> [{clean_text}]")
                except Exception as exc:
                    report.append(f"Orientacion: {name}, PSM: {psm} -> Fallo: {exc}")
    return "\n".join(report)


if __name__ == "__main__":
    candidate = data_dir() / "temp_processing" / "page_36_forensic.png"
    print(test_ocr_variations(candidate))
