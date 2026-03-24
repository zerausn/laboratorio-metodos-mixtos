# Dependencies

This document lists the components used or installed for the reconstruction work.

## Python packages actually used in code

### Required

- `pandas`
  - DataFrames, CSV/XLSX export.
- `openpyxl`
  - XLSX writing for page-specific workbook output.
- `xlsxwriter`
  - XLSX writing for multi-sheet export in the extraction pipeline.
- `pymupdf`
  - Imported as `fitz`.
  - PDF rendering and PDF page inspection.
- `opencv-python-headless`
  - Imported as `cv2`.
  - Denoising and thresholding before OCR.
- `pytesseract`
  - Bridge between Python and local Tesseract OCR.
- `Pillow`
  - Indirectly useful through image tooling already present in the environment.
- `reportlab`
  - Clean PDF generation and PDF reports.
- `python-docx`
  - DOCX report generation.
- `google-cloud-documentai`
  - Native Document AI object model.
- `google-cloud-documentai-toolbox`
  - Wrapped access to Document AI pages, lines, tables and hOCR export.
- `numpy`
  - Image arrays for OCR preprocessing.

## Python packages specifically used by the no-JSON hybrid route

- `pymupdf`
  - reads the embedded text layer directly from the PDF.
- `opencv-python-headless`
  - detects the table area and the grid cell boundaries.
- `pytesseract`
  - OCR fallback at the cell level.
- `openpyxl`
  - writes the clean Excel comparison workbook.
- `reportlab`
  - writes the clean PDF comparison artifact.

## Python packages installed during this work

- `pymupdf`
- `pytesseract`
- `xlsxwriter`
- `python-docx`
- `rapidfuzz`
- `opencv-python-headless`

## Packages present and relevant even if not installed during this session

- `openpyxl`
- `pandas`
- `Pillow`
- `reportlab`
- `google-cloud-documentai`
- `google-cloud-documentai-toolbox`
- `pikepdf`

## Installed but currently redundant or optional

- `rapidfuzz`
  - Installed for possible fuzzy cleanup and reconciliation.
  - Not required by the final version of the scripts.
- `python-docx`
  - Useful for the extraction report.
  - Not needed for the clean PDF reconstruction itself.
- `pikepdf`
  - Useful for PDF inspection.
  - Not required by the final reconstruction scripts.
- `openpyxl` + `xlsxwriter`
  - Both are present.
  - `openpyxl` is used for the single-page workbook script.
  - `xlsxwriter` is used for the multi-sheet extraction workbook.

## Git and transport dependencies

- `git`
  - normal Git operations are working.
- `git-lfs`
  - required if the raw Document AI JSON files are pushed to GitHub,
  - because `document (2).json` exceeds `100 MB`.

## System dependencies

### Git

- `git` is installed and working.
- Remote access uses SSH.

### GitHub CLI

- `gh` is not installed.
- This is not a blocker because `git` over SSH already works.

### Tesseract OCR

- Installed system executable:
  - `C:\Program Files\Tesseract-OCR\tesseract.exe`

### Tesseract language models used by this project

Stored locally in:

- `resources/tessdata/eng.traineddata`
- `resources/tessdata/osd.traineddata`
- `resources/tessdata/spa.traineddata`

## Minimal practical environment

If another programmer or AI only wants the essentials, the minimal stack is:

- `pandas`
- `openpyxl`
- `xlsxwriter`
- `pymupdf`
- `opencv-python-headless`
- `pytesseract`
- `reportlab`
- `google-cloud-documentai`
- `google-cloud-documentai-toolbox`
- `numpy`
- local `Tesseract OCR`

## Recommended install command for Python packages

```powershell
.\.venv\Scripts\python.exe -m pip install `
  pandas openpyxl xlsxwriter pymupdf opencv-python-headless `
  pytesseract reportlab python-docx numpy `
  google-cloud-documentai google-cloud-documentai-toolbox rapidfuzz
```
