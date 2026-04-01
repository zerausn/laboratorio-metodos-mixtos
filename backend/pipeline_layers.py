import json
from pathlib import Path

import fitz

try:
    from backend.export_module import DataExporter
    from backend.image_cleaner import ImageCleaner
    from backend.path_utils import default_output_dir, default_pdf_path
except ImportError:
    from export_module import DataExporter
    from image_cleaner import ImageCleaner
    from path_utils import default_output_dir, default_pdf_path


class LayerPipeline:
    def __init__(self, pdf_path, output_dir):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cleaner = ImageCleaner(output_dir=self.output_dir / "cleaned_images")
        self.exporter = DataExporter()
        self.checkpoint_file = self.output_dir / "layer_pipeline_status.json"

    def _load_status(self):
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, "r", encoding="utf-8") as handle:
                return json.load(handle)
        return {"processed_pages": [], "data": []}

    def _save_status(self, status):
        with open(self.checkpoint_file, "w", encoding="utf-8") as handle:
            json.dump(status, handle, indent=4, ensure_ascii=False)

    def process_pdf(self):
        doc = fitz.open(self.pdf_path)
        status = self._load_status()
        temp_img_dir = self.output_dir / "temp_images"
        temp_img_dir.mkdir(parents=True, exist_ok=True)

        for index in range(len(doc)):
            page_num = index + 1
            if page_num in status["processed_pages"]:
                continue

            img_path = temp_img_dir / f"page_{page_num}.png"
            page = doc.load_page(index)
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
            pix.save(str(img_path))

            clean_img_path = self.cleaner.clean_photocopier_noise(img_path)
            text_extracted = self.cleaner.extract_text(clean_img_path)
            page_data = {
                "page": page_num,
                "text": text_extracted,
                "clean_image_path": clean_img_path,
            }
            status["processed_pages"].append(page_num)
            status["data"].append(page_data)
            self._save_status(status)
            self._export_all(status["data"])

    def _export_all(self, data_list):
        self.exporter.to_word(data_list, self.output_dir / "output_layers.docx")
        self.exporter.to_excel(data_list, self.output_dir / "output_layers.xlsx")
        self.exporter.to_csv(data_list, self.output_dir / "output_layers.csv")
        self.exporter.to_pdf_text(data_list, self.output_dir / "output_layers.pdf")


if __name__ == "__main__":
    pipeline = LayerPipeline(default_pdf_path(), default_output_dir())
    pipeline.process_pdf()
