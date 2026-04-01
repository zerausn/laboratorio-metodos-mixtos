from pathlib import Path

import pandas as pd
from docx import Document

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class DataExporter:
    @staticmethod
    def _prepare(output_path: str | Path) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path

    @staticmethod
    def to_csv(data_list, output_path):
        output_path = DataExporter._prepare(output_path)
        pd.DataFrame(data_list).to_csv(output_path, index=False, encoding="utf-8")
        return output_path

    @staticmethod
    def to_excel(data_list, output_path):
        output_path = DataExporter._prepare(output_path)
        pd.DataFrame(data_list).to_excel(output_path, index=False, engine="xlsxwriter")
        return output_path

    @staticmethod
    def to_word(data_list, output_path):
        output_path = DataExporter._prepare(output_path)
        doc = Document()
        doc.add_heading("Resultado de extraccion de datos", 0)
        for item in data_list:
            page = item.get("page", "N/A")
            text = item.get("text", "")
            doc.add_heading(f"Pagina {page}", level=1)
            doc.add_paragraph(str(text))
            doc.add_page_break()
        doc.save(output_path)
        return output_path

    @staticmethod
    def to_pdf_text(data_list, output_path):
        output_path = DataExporter._prepare(output_path)
        if not REPORTLAB_AVAILABLE:
            return None

        pdf = canvas.Canvas(str(output_path), pagesize=letter)
        _, height = letter
        for item in data_list:
            pdf.setFont("Helvetica", 12)
            pdf.drawString(50, height - 50, f"Pagina {item.get('page', 'N/A')}")
            text_object = pdf.beginText(50, height - 80)
            text_object.setFont("Helvetica", 10)
            for line in str(item.get("text", "")).splitlines():
                text_object.textLine(line[:120])
            pdf.drawText(text_object)
            pdf.showPage()
        pdf.save()
        return output_path
