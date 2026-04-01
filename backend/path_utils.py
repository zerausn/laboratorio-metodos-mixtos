from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_dir() -> Path:
    return ensure_dir(repo_root() / "data")


def reports_dir() -> Path:
    return ensure_dir(repo_root() / "reports")


def workspaces_dir() -> Path:
    return ensure_dir(repo_root() / "workspaces")


def default_pdf_path(filename: str = "ejecucion_presupuestal.pdf") -> Path:
    return data_dir() / filename


def default_checkpoint_path(filename: str = "recovery_status.json") -> Path:
    return data_dir() / filename


def default_output_dir(dirname: str = "layer_pipeline_output") -> Path:
    return ensure_dir(data_dir() / dirname)


def tesseract_cmd() -> str | None:
    candidates = [
        os.environ.get("TESSERACT_CMD"),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


def configure_tesseract() -> str | None:
    cmd = tesseract_cmd()
    if cmd:
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = cmd
    return cmd
