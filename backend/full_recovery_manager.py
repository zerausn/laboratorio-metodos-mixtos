import json
from pathlib import Path

import fitz

try:
    from backend.final_report_generator import generate_reports
    from backend.ocr_engine import DegradedDocProcessor
    from backend.path_utils import default_checkpoint_path, default_pdf_path, reports_dir
except ImportError:
    from final_report_generator import generate_reports
    from ocr_engine import DegradedDocProcessor
    from path_utils import default_checkpoint_path, default_pdf_path, reports_dir


def full_document_recovery(pdf_path=None, checkpoint_file=None):
    processor = DegradedDocProcessor()
    pdf_path = Path(pdf_path or default_pdf_path())
    checkpoint_file = Path(checkpoint_file or default_checkpoint_path())
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

    if checkpoint_file.exists():
        with open(checkpoint_file, "r", encoding="utf-8") as handle:
            status = json.load(handle)
    else:
        status = {"processed_pages": [], "data": []}

    total_pages = len(fitz.open(pdf_path))
    for page_num in range(1, total_pages + 1):
        if page_num in status["processed_pages"]:
            continue
        try:
            page_results = processor.process_document(pdf_path, page_range=[page_num])
            if page_results:
                status["processed_pages"].append(page_num)
                status["data"].append(page_results[0])
                with open(checkpoint_file, "w", encoding="utf-8") as handle:
                    json.dump(status, handle, indent=4, ensure_ascii=False)
        except Exception as exc:
            print(f"Error en pagina {page_num}: {exc}")

    if status["data"]:
        generate_reports(status["data"], reports_dir())
    return status


if __name__ == "__main__":
    full_document_recovery()
