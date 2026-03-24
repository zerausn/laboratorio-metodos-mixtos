# No-JSON Hybrid Pipeline

## Purpose

This pipeline exists as a separate experiment from the original Document AI workflow.

It should be used when you want to answer:

- how far can we reconstruct the document without Google JSON,
- whether the PDF itself contains enough embedded text to beat pure OCR,
- and whether a grid-based rebuild is better than a line-based rebuild.

## Script

- `scripts/reconstruct_without_json_hybrid.py`

## Inputs

- `inputs/Sin_titulo.pdf`
- local `Tesseract OCR`
- local `tessdata`

No Document AI JSON is used by this script.

## Reconstruction logic

1. choose the best visual rotation for the page
2. detect the largest table region
3. detect grid lines and derive cells
4. read the PDF native text layer and map it into those cells
5. OCR each cell as fallback
6. choose the better candidate per cell
7. write a clean PDF and Excel

## Why this route is valuable

- It avoids dependency on cloud outputs.
- It is reproducible from the PDF alone.
- It is useful for sensitivity analysis and benchmarking.
- It gives the user a fair comparison against the JSON-assisted pipeline.

## Suggested comparison protocol

1. Run `run_reconstruct_clean.ps1` for the JSON-assisted version.
2. Run `run_no_json_hybrid.ps1` for the no-JSON version.
3. Compare page readability, numeric reliability, and Excel usability.
4. Focus first on dense budget pages like 3, 15, 35, 49, and 69.
