# Document AI + PDF exploitation route

This route is designed for degraded public-finance documents like scanned photocopies with hard-to-read tables.

## Recommended stack

Use these tools in this order:

1. `Google Cloud Document AI JSON` as the primary structured source.
2. `google-cloud-documentai-toolbox` to read JSON pages, text, tables, and export hOCR.
3. `PyMuPDF` (`fitz`) to inspect and render the original PDF page by page.
4. `OpenCV` to denoise and threshold difficult pages before OCR.
5. `Tesseract` with `spa+eng+osd` for local fallback OCR when JSON coverage is partial or weak.
6. `pandas` + `xlsxwriter/openpyxl` to export tables and page inventories to Excel.
7. `reportlab` and `python-docx` to generate a readable PDF/DOCX report.

## Why this route works

The PDF has three different realities at once:

- a noisy scan layer,
- an unreliable OCR text layer embedded in the PDF,
- a stronger but partial structured extraction from Document AI JSON.

The safest pipeline is therefore hybrid:

- trust `Document AI` first for structured tables,
- use `PyMuPDF` to preserve the original page order,
- use `OpenCV + Tesseract` only as fallback or gap-filler,
- export everything with traceability so each row can be linked back to its source page.

## Document diagnosis for this case

- PDF length: `69` pages.
- Observed font in the PDF text layer: mostly `Helvetica` / `Helvetica-Bold`.
- Practical caveat: on a scanned photocopy this is usually the OCR/export layer, not proof of the original printed font.
- The visible document style is consistent with an institutional sans-serif family similar to `Helvetica/Arial`.
- The main image problem is not the font. It is scan degradation:
  - vertical noise on the left margin,
  - sideways table pages,
  - low contrast around numbers,
  - unstable OCR on dense accounting tables.

## Page logic detected

- PDF pages `3-34`: `Ingresos` tables.
- PDF page `35`: `Gastos` cover.
- PDF pages `36-48`: first `Gastos` table block, partially covered by Document AI JSON.
- PDF pages `49-64`: second `Gastos` table block, recovered mainly with local OCR.
- PDF page `69`: summary page with macro totals for `Total`, `Funcionamiento`, `Deuda`, and `Inversion`.

## Files produced by the pipeline

The script writes:

- `document_extraction.xlsx`
- `document_extraction_report.pdf`
- `document_extraction_report.docx`
- `processing_manifest.json`
- `pdf_page_inventory.csv`
- `docai_page_inventory.csv`
- `ocr_tokens.csv`
- `tables_csv/*.csv`
- `pdf_ocr_text/*.txt`
- `docai_text/*.txt`
- `hocr/*.hocr.html`

## How to run from Antigravity or VS Code

```powershell
.\\.venv\\Scripts\\python.exe .\\tools\\docai_pdf_pipeline.py `
  --pdf "C:\\Users\\ZN-\\Downloads\\Sin título.pdf" `
  --docai-dir "C:\\Users\\ZN-\\Documents\\Antigravity\\.venv\\Nueva carpeta" `
  --output-dir "C:\\Users\\ZN-\\Documents\\Antigravity\\artifacts\\sin_titulo_extraction" `
  --tesseract-cmd "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" `
  --tessdata-dir "C:\\Users\\ZN-\\Documents\\Antigravity\\tools\\tessdata"
```

## How to rebuild a clean PDF page by page

Use this when you do not want a noisy scan anymore and need a clean reconstructed document plus an Excel workbook with one sheet per page:

```powershell
.\\.venv\\Scripts\\python.exe .\\tools\\reconstruct_clean_document.py `
  --pdf "C:\\Users\\ZN-\\Downloads\\Sin título.pdf" `
  --docai-dir "C:\\Users\\ZN-\\Documents\\Antigravity\\Laboratorio metodos mixtos\\Nueva carpeta" `
  --output-dir "C:\\Users\\ZN-\\Documents\\Antigravity\\artifacts\\sin_titulo_reconstructed" `
  --tesseract-cmd "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" `
  --tessdata-dir "C:\\Users\\ZN-\\Documents\\Antigravity\\tools\\tessdata"
```

This second script produces:

- `document_reconstructed_clean.pdf`
- `document_reconstructed_layout.xlsx`
- `document_reconstructed_manifest.json`

## What Antigravity should infer from this pipeline

When the input is a degraded fiscal report, Antigravity should follow this decision rule:

1. If there is `Document AI JSON`, use it first.
2. If a page has extracted tables in JSON, export those tables directly to Excel.
3. If a page is missing from JSON or looks low quality, render the PDF page locally.
4. Test OCR on multiple rotations and keep the version with better confidence.
5. Mark difficult pages instead of pretending confidence is high.
6. Preserve page-level traceability in every export.
7. Prefer macro totals and summary pages when exact row-level recovery remains uncertain.

## Alternative recovery proposals

If you need stronger recovery later, the next best options are:

1. Re-run the missing page ranges through `Google Cloud Document AI` with a table-focused processor.
2. Export difficult pages as cleaned images and review only the flagged subset manually.
3. Request the native spreadsheet from the public entity under open-data and transparency rules, then use this extraction only as audit support.
