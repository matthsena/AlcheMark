import pymupdf4llm
import os
from configs.logger import logging

class PDF2MarkDown:
    def __init__(self, file_path: str, process_images: bool = False):
        self.file_path = file_path
        self.page_chunks = True
        self.process_images = process_images

    def _check_file(self):
        try:
            logging.info(f"[CHECK FILE] Checking if the file {self.file_path} exists and is a PDF.")
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"[CHECK FILE] The file {self.file_path} does not exist.")
            if not self.file_path.lower().endswith('.pdf'):
                raise ValueError(f"[CHECK FILE] The file {self.file_path} is not a PDF file.")
        except Exception as e:
            raise ValueError(f"[CHECK FILE] Invalid file: {self.file_path}")

    def convert(self):
        try:
            logging.info(f"[CONVERT] Converting {self.file_path} to Markdown.")
            self._check_file()
            logging.info(f"[CONVERT] File {self.file_path} is valid. Proceeding with conversion.")
            return pymupdf4llm.to_markdown(
                self.file_path,
                page_chunks=self.page_chunks,
                embed_images=self.process_images)
        except Exception as e:
            raise ValueError(f"[CONVERT] Error converting PDF to Markdown: {e}")