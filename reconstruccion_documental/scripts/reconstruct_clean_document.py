from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cv2
import fitz
import pandas as pd
import pytesseract
from google.cloud.documentai_toolbox.wrappers.document import Document as WrappedDocument
from reportlab.lib import colors
from reportlab.pdfgen import canvas

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from docai_pdf_pipeline import (
    DocAiPage,
    configure_tesseract,
    detect_section,
    extract_marker,
    preprocess_for_ocr,
    preview_text,
    render_page,
    resolve_tesseract,
    rotate_image,
    seed_docai_mappings,
)
from project_paths import DOCAI_JSON_DIR, OUTPUTS_DIR, PDF_PATH, TESSDATA_DIR


PDF_SCALE = 0.30
UNIFORM_FONT_SIZE = 4.2


@dataclass
class CleanLine:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float


@dataclass
class CleanPage:
    absolute_page: int
    width: float
    height: float
    source: str
    source_file: str | None
    local_page: int | None
    section: str
    marker_page: int | None
    marker_total: int | None
    lines: list[CleanLine]
    preview: str


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def is_noise_text(text: str) -> bool:
    compact = normalize_spaces(text)
    if not compact:
        return True
    if len(compact) <= 2 and not re.search(r"[A-Za-z0-9]", compact):
        return True
    if re.fullmatch(r"[\W_]+", compact):
        return True
    if re.search(r"[\u0600-\u06FF]", compact) and not re.search(r"[A-Za-z0-9]", compact):
        return True
    return False


def normalized_bbox(layout: Any) -> tuple[float, float, float, float]:
    vertices = layout.bounding_poly.normalized_vertices
    xs = [float(vertex.x) for vertex in vertices]
    ys = [float(vertex.y) for vertex in vertices]
    return min(xs), min(ys), max(xs), max(ys)


def avg(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def score_ocr_data(data: dict[str, list[Any]]) -> float:
    words = [str(word).strip() for word in data["text"] if str(word).strip()]
    confidences = [
        float(conf)
        for conf in data["conf"]
        if str(conf).strip() not in {"", "-1"} and float(conf) >= 0
    ]
    return avg(confidences) * max(len(words), 1)


def lines_from_ocr_data(
    data: dict[str, list[Any]],
    width: int,
    height: int,
) -> list[CleanLine]:
    grouped: dict[tuple[int, int, int], list[dict[str, Any]]] = defaultdict(list)
    for idx, raw_text in enumerate(data["text"]):
        text = str(raw_text).strip()
        if not text:
            continue
        grouped[
            (
                int(data["block_num"][idx]),
                int(data["par_num"][idx]),
                int(data["line_num"][idx]),
            )
        ].append(
            {
                "text": text,
                "left": int(data["left"][idx]),
                "top": int(data["top"][idx]),
                "width": int(data["width"][idx]),
                "height": int(data["height"][idx]),
            }
        )

    lines: list[CleanLine] = []
    for group in grouped.values():
        group.sort(key=lambda item: item["left"])
        line_text = normalize_spaces(" ".join(item["text"] for item in group))
        if is_noise_text(line_text):
            continue
        x0 = min(item["left"] for item in group) / width
        y0 = min(item["top"] for item in group) / height
        x1 = max(item["left"] + item["width"] for item in group) / width
        y1 = max(item["top"] + item["height"] for item in group) / height
        lines.append(CleanLine(text=line_text, x0=x0, y0=y0, x1=x1, y1=y1))
    lines.sort(key=lambda item: (item.y0, item.x0))
    return lines


def ocr_clean_page(pdf_page: fitz.Page, absolute_page: int) -> CleanPage:
    base_image = render_page(pdf_page, zoom=2.0)
    candidates: list[tuple[int, dict[str, list[Any]], int, int]] = []
    for rotation in (0, 90):
        rotated = rotate_image(base_image, rotation)
        processed = preprocess_for_ocr(rotated)
        data = pytesseract.image_to_data(
            processed,
            lang="spa+eng",
            config="--psm 6",
            output_type=pytesseract.Output.DICT,
        )
        candidates.append((rotation, data, processed.shape[1], processed.shape[0]))

    best_rotation, best_data, width, height = max(candidates, key=lambda item: score_ocr_data(item[1]))
    lines = lines_from_ocr_data(best_data, width=width, height=height)
    text = "\n".join(line.text for line in lines)
    marker_page, marker_total = extract_marker(text)
    section = detect_section(text)
    if section == "sin_clasificar" and absolute_page in {35, 67}:
        section = "portada"
    return CleanPage(
        absolute_page=absolute_page,
        width=float(width),
        height=float(height),
        source="ocr",
        source_file=None,
        local_page=None,
        section=section,
        marker_page=marker_page,
        marker_total=marker_total,
        lines=lines,
        preview=preview_text(text),
    )


def load_docai_source_pages(docai_dir: Path) -> dict[int, CleanPage]:
    metadata_pages: list[DocAiPage] = []
    wrapped_pages: dict[tuple[str, int], Any] = {}

    for json_path in sorted(docai_dir.glob("document*.json")):
        wrapped = WrappedDocument.from_document_path(str(json_path))
        for local_page, page in enumerate(wrapped.pages, start=1):
            text = page.text or ""
            marker_page, marker_total = extract_marker(text)
            metadata_pages.append(
                DocAiPage(
                    source_file=json_path.name,
                    local_page=local_page,
                    marker_page=marker_page,
                    marker_total=marker_total,
                    mapped_pdf_page=None,
                    section=detect_section(text),
                    avg_token_confidence=0.0,
                    table_count=len(page.tables),
                    text_length=len(text),
                    preview=preview_text(text),
                    text=text,
                )
            )
            wrapped_pages[(json_path.name, local_page)] = page

    seed_docai_mappings(metadata_pages)
    selected: dict[int, tuple[DocAiPage, Any]] = {}
    for meta in metadata_pages:
        if meta.mapped_pdf_page is None:
            continue
        wrapped_page = wrapped_pages[(meta.source_file, meta.local_page)]
        current = selected.get(meta.mapped_pdf_page)
        candidate_score = (meta.table_count, meta.text_length, len(wrapped_page.lines))
        if current is None:
            selected[meta.mapped_pdf_page] = (meta, wrapped_page)
            continue
        current_score = (
            current[0].table_count,
            current[0].text_length,
            len(current[1].lines),
        )
        if candidate_score > current_score:
            selected[meta.mapped_pdf_page] = (meta, wrapped_page)

    clean_pages: dict[int, CleanPage] = {}
    for absolute_page, (meta, wrapped_page) in selected.items():
        raw_page = wrapped_page.documentai_object
        lines: list[CleanLine] = []
        for line in wrapped_page.lines:
            text = normalize_spaces(line.text)
            if is_noise_text(text):
                continue
            x0, y0, x1, y1 = normalized_bbox(line.documentai_object.layout)
            lines.append(CleanLine(text=text, x0=x0, y0=y0, x1=x1, y1=y1))
        lines.sort(key=lambda item: (item.y0, item.x0))
        clean_pages[absolute_page] = CleanPage(
            absolute_page=absolute_page,
            width=float(raw_page.dimension.width),
            height=float(raw_page.dimension.height),
            source="docai",
            source_file=meta.source_file,
            local_page=meta.local_page,
            section=meta.section,
            marker_page=meta.marker_page,
            marker_total=meta.marker_total,
            lines=lines,
            preview=meta.preview,
        )
    return clean_pages


def draw_clean_pdf(output_pdf: Path, pages: list[CleanPage]) -> None:
    pdf = canvas.Canvas(str(output_pdf))
    for page in pages:
        page_width = page.width * PDF_SCALE
        page_height = page.height * PDF_SCALE
        pdf.setPageSize((page_width, page_height))
        pdf.setFillColor(colors.white)
        pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)
        pdf.setFillColor(colors.black)

        for line in page.lines:
            x = line.x0 * page_width
            y = page_height - (line.y1 * page_height)
            pdf.setFont("Helvetica", UNIFORM_FONT_SIZE)
            pdf.drawString(x, y, normalize_spaces(line.text))

        pdf.setFont("Helvetica", 8)
        pdf.drawRightString(page_width - 10, 8, f"PDF page {page.absolute_page}")
        pdf.showPage()
    pdf.save()


def cluster_positions(values: list[float], tolerance: float) -> list[float]:
    if not values:
        return []
    clusters: list[list[float]] = [[sorted(values)[0]]]
    for value in sorted(values)[1:]:
        if abs(value - clusters[-1][-1]) <= tolerance:
            clusters[-1].append(value)
        else:
            clusters.append([value])
    return [avg(cluster) for cluster in clusters]


def write_layout_excel(output_xlsx: Path, pages: list[CleanPage]) -> None:
    summary_rows = []
    with pd.ExcelWriter(output_xlsx, engine="xlsxwriter") as writer:
        for page in pages:
            sheet_name = f"p{page.absolute_page:03d}"
            workbook = writer.book
            worksheet = workbook.add_worksheet(sheet_name)
            writer.sheets[sheet_name] = worksheet

            row_positions = cluster_positions(
                [(line.y0 + line.y1) / 2 for line in page.lines],
                tolerance=0.005,
            )
            col_positions = cluster_positions(
                [line.x0 for line in page.lines],
                tolerance=0.015,
            )
            if not row_positions:
                row_positions = [0.01]
            if not col_positions:
                col_positions = [0.01]

            cell_map: dict[tuple[int, int], str] = {}
            for line in page.lines:
                row_index = min(
                    range(len(row_positions)),
                    key=lambda idx: abs(row_positions[idx] - ((line.y0 + line.y1) / 2)),
                )
                col_index = min(
                    range(len(col_positions)),
                    key=lambda idx: abs(col_positions[idx] - line.x0),
                )
                key = (row_index, col_index)
                existing = cell_map.get(key)
                cell_map[key] = f"{existing}\n{line.text}" if existing else line.text

            wrap_format = workbook.add_format({"text_wrap": True, "valign": "top"})
            for (row_index, col_index), value in cell_map.items():
                worksheet.write(row_index, col_index, value, wrap_format)

            column_breaks = col_positions + [1.0]
            for index, start in enumerate(col_positions):
                end = column_breaks[index + 1]
                width = max(8, min(60, (end - start) * 120))
                worksheet.set_column(index, index, width)

            row_breaks = row_positions + [1.0]
            for index, start in enumerate(row_positions):
                end = row_breaks[index + 1]
                height = max(16, min(80, (end - start) * 500))
                worksheet.set_row(index, height)

            worksheet.freeze_panes(0, 0)
            summary_rows.append(
                {
                    "absolute_page": page.absolute_page,
                    "source": page.source,
                    "source_file": page.source_file,
                    "local_page": page.local_page,
                    "section": page.section,
                    "marker_page": page.marker_page,
                    "marker_total": page.marker_total,
                    "line_count": len(page.lines),
                    "preview": page.preview,
                }
            )

        pd.DataFrame(summary_rows).to_excel(writer, sheet_name="summary", index=False)


def write_manifest(output_json: Path, pages: list[CleanPage]) -> None:
    payload = {
        "pages": [
            {
                **asdict(page),
                "lines": [asdict(line) for line in page.lines],
            }
            for page in pages
        ]
    }
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild a clean page-by-page PDF and Excel from Document AI + OCR.")
    parser.add_argument("--pdf", default=str(PDF_PATH), help="Absolute path to the original PDF.")
    parser.add_argument("--docai-dir", default=str(DOCAI_JSON_DIR), help="Directory with Document AI JSON files.")
    parser.add_argument("--output-dir", default=str(OUTPUTS_DIR / "sin_titulo_reconstructed_uniform_v2"), help="Directory for reconstructed outputs.")
    parser.add_argument("--tesseract-cmd", default=None, help="Optional explicit path to tesseract.exe.")
    parser.add_argument("--tessdata-dir", default=str(TESSDATA_DIR), help="Optional tessdata directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pdf_path = Path(args.pdf)
    docai_dir = Path(args.docai_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tesseract_cmd = resolve_tesseract(args.tesseract_cmd)
    tessdata_dir = Path(args.tessdata_dir) if args.tessdata_dir else None
    configure_tesseract(tesseract_cmd=tesseract_cmd, tessdata_dir=tessdata_dir)

    clean_pages_by_pdf = load_docai_source_pages(docai_dir)
    pdf_doc = fitz.open(str(pdf_path))
    for absolute_page in range(1, pdf_doc.page_count + 1):
        if absolute_page in clean_pages_by_pdf:
            continue
        clean_pages_by_pdf[absolute_page] = ocr_clean_page(pdf_doc.load_page(absolute_page - 1), absolute_page)

    pages = [clean_pages_by_pdf[number] for number in sorted(clean_pages_by_pdf)]
    draw_clean_pdf(output_dir / "document_reconstructed_clean.pdf", pages)
    write_layout_excel(output_dir / "document_reconstructed_layout.xlsx", pages)
    write_manifest(output_dir / "document_reconstructed_manifest.json", pages)
    print(f"Done. Reconstructed outputs written to: {output_dir}")


if __name__ == "__main__":
    main()
