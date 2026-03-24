# Page 3 without JSON

This document explains the isolated reconstruction test for PDF page 3 without using any Google Document AI JSON.

## Goal

- Prove that page 3 can be rebuilt from the PDF alone.
- Keep this route separate from the previous Document AI workflow.
- Leave a second experimental pipeline that can be executed later on all 69 pages and compared against the JSON-assisted pipeline.

## New no-JSON route

The page 3 experiment now uses:

1. `PyMuPDF`
   - reads the PDF,
   - renders the page,
   - extracts the embedded PDF text layer when available.

2. `OpenCV`
   - rotates the page,
   - detects the main table,
   - detects row and column separators from the grid.

3. `Tesseract`
   - OCR fallback for cells where the embedded PDF text is weak,
   - especially useful in the rightmost percentage column or broken code cells.

4. `openpyxl` and `reportlab`
   - rebuild the page as clean Excel and clean PDF outputs.

## Scripts

- `scripts/reconstruct_without_json_hybrid.py`
  - generic no-JSON experimental pipeline.
- `scripts/reconstruct_page3_without_json.py`
  - page 3 wrapper for a controlled benchmark.

## Outputs

Page 3 benchmark outputs are written to:

- `outputs/page3_without_json_hybrid/page3_reconstructed_without_json_hybrid.pdf`
- `outputs/page3_without_json_hybrid/page3_reconstructed_without_json_hybrid.xlsx`
- `outputs/page3_without_json_hybrid/page3_reconstructed_without_json_hybrid.json`

## Limitation

The PDF embedded text layer is better than raw OCR in some numeric cells, but weak in narrow identifier columns. That is why the hybrid script combines both sources cell by cell instead of trusting only one source.
