from pypdf import PdfReader
from typing import List
import os

class PDFReaderTool:
    def read_pdf(self, file_path: str) -> str:
        """
        Reads a PDF file and returns its text content.
        """
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."
        
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Simple text chunker.
        """
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
