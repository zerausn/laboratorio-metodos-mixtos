from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = PROJECT_ROOT.parent

PDF_PATH = PROJECT_ROOT / "inputs" / "Sin_titulo.pdf"
DOCAI_JSON_DIR = LAB_ROOT / "Nueva carpeta"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
TESSDATA_DIR = PROJECT_ROOT / "resources" / "tessdata"


def as_dict() -> dict[str, str]:
    return {
        "PROJECT_ROOT": str(PROJECT_ROOT),
        "LAB_ROOT": str(LAB_ROOT),
        "PDF_PATH": str(PDF_PATH),
        "DOCAI_JSON_DIR": str(DOCAI_JSON_DIR),
        "OUTPUTS_DIR": str(OUTPUTS_DIR),
        "TESSDATA_DIR": str(TESSDATA_DIR),
    }
