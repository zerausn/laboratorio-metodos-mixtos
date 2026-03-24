from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from project_paths import OUTPUTS_DIR, PDF_PATH, TESSDATA_DIR
from reconstruct_without_json_hybrid import run_pipeline


def main() -> None:
    output_dir = OUTPUTS_DIR / "page3_without_json_hybrid"
    run_pipeline(
        pdf_path=PDF_PATH,
        output_dir=output_dir,
        pages_arg="3",
        tesseract_cmd=None,
        tessdata_dir=TESSDATA_DIR,
        artifact_prefix="page3_reconstructed_without_json_hybrid",
    )
    print(f"Done. Page 3 written to: {output_dir}")


if __name__ == "__main__":
    main()
