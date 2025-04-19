from pdf2md import PDF2MarkDown
from configs.logger import logging
import os

def main():
    logging.info("[MAIN] Starting PDF to Markdown conversion.")
    pdf_file_path = os.path.join(os.path.dirname(__file__), '../sample/Sample.pdf')
    process_images = False

    try:
        pdf_converter = PDF2MarkDown(pdf_file_path, process_images)
        markdown_content = pdf_converter.convert()
        logging.info("[MAIN] Conversion successful.")
    except Exception as e:
        logging.error(f"[MAIN] An error occurred: {e}")

if __name__ == "__main__":
    main()