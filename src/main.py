from pdf2md import PDF2MarkDown
from formatter import FormatterMD
from configs.logger import logging
import os

def main():
    logging.info("[MAIN] Starting PDF to Markdown conversion.")
    pdf_file_path = os.path.join(os.path.dirname(__file__), '../sample/Sample.pdf')
    process_images = False

    try:
        pdf_converter = PDF2MarkDown(pdf_file_path, process_images)
        markdown_content = pdf_converter.convert()
        # write in disk
        fmt = FormatterMD(markdown_content)

        formatted_results = fmt.format()
        # write in disk
        for result in formatted_results:
            print(result.model_dump_json(indent=4))
    except Exception as e:
        logging.error(f"[MAIN] An error occurred: {e}")

if __name__ == "__main__":
    main()