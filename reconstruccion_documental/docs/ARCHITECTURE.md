# Architecture

## 1. Input layers

The project works with three information layers:

1. `PDF source`
   - Original scanned public-finance report.
   - Good for page order and visual reference.
   - Bad as a direct data source because of noise, sideways pages and weak embedded OCR.

2. `Document AI JSON`
   - Primary structured layer when available.
   - Best source for page geometry, line positions and extracted tables.
   - Not complete for every page, so it must be combined with OCR.

3. `Local OCR`
   - Fallback for missing or low-coverage pages.
   - Uses `PyMuPDF` for rendering, `OpenCV` for preprocessing, and `Tesseract` for OCR.

## 2. Main scripts

### `scripts/docai_pdf_pipeline.py`

Purpose:

- Merge Document AI pages and fallback OCR.
- Export page inventories, text files, CSV, XLSX, PDF report and DOCX report.

Key responsibilities:

- Load JSON files.
- Map JSON page markers to absolute PDF pages.
- OCR missing pages.
- Produce auditable outputs.

### `scripts/reconstruct_clean_document.py`

Purpose:

- Rebuild the document page by page on a clean white background.
- Preserve line geometry recovered by Document AI.
- Use OCR only for pages that do not have reliable JSON coverage.

Key responsibilities:

- Build `CleanPage` objects.
- Draw a clean PDF.
- Create one Excel sheet per page using page layout.
- Write a JSON manifest with page/line geometry.

### `scripts/reconstruct_page3_without_json.py`

Purpose:

- Prove that page 3 can be rebuilt without any Document AI JSON.
- Use OCR only.
- Export PDF, XLSX and JSON for that isolated page.

### `scripts/reconstruct_without_json_hybrid.py`

Purpose:

- Create a second experimental family of code that does not depend on Document AI JSON.
- Reconstruct pages from the PDF itself, using native PDF text when available and OCR when needed.
- Serve as a benchmark pipeline against the JSON-assisted route.

## 3. Mapping logic

The document is split in several internal page blocks:

- `1-32 de 32`: ingresos.
- `1-13 de 13`: first gastos block.
- `1-16 de 16`: second gastos block.
- `1-2 de 2`: resumen por organismos.
- `1-1`: deuda block.

Those blocks are mapped to absolute PDF pages through known offsets:

- `32 -> +2`
- `13 -> +35`
- `16 -> +48`
- `2 -> +64`
- `1 -> +67`

This logic is codified in `KNOWN_PAGE_OFFSETS`.

## 4. Rendering strategy

### Clean PDF

- Use original recovered page geometry.
- White background.
- Black text.
- Uniform small font for the reconstructed version.
- Page number added at bottom-right.

### Layout Excel

- One sheet per page.
- Lines clustered into row and column anchors.
- The goal is visual exploitation and traceability, not perfect semantic normalization.

## 5. Why there are two output families

### `sin_titulo_extraction_full`

Best when you want:

- inventories,
- reports,
- table CSVs,
- Document AI traceability,
- mixed extraction audit outputs.

### `sin_titulo_reconstructed_uniform_v2`

Best when you want:

- a clean rebuilt PDF,
- a page-by-page Excel that looks closer to a spreadsheet layout,
- a presentation artifact instead of a raw extraction artifact.

### `no_json_hybrid_full`

Best when you want:

- a controlled comparison against the previous pipeline,
- no dependency on Document AI JSON,
- page-by-page testing of `PDF native text + OCR + grid detection`.
