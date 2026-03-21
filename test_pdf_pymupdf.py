import sys
from unittest.mock import MagicMock

class MockFile:
    def __init__(self, filename):
        self.name = filename
        
    def getvalue(self):
        # We need a real file to reproduce this issue since the user's PDF is broken.
        # But for now, we'll write a script that the user can run to test their specific PDF
        pass

# This code will be modified to accept a real local file for testing
import fitz # PyMuPDF
import sys

def test_pdf(filepath):
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            # text += page.get_text("text", flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE)
            text += page.get_text()
        print("--- EXTRACTED WITH PYMUPDF ---")
        print(text[:1000])
        print("-------------------------------")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_pdf(sys.argv[1])
    else:
        print("Please provide a PDF path.")
