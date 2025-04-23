import alchemark_ai
import os

def main():
    pdf_file_path = os.path.join(os.path.dirname(__file__), '../sample/Sample.pdf')
    process_images = True

    try:
        results = alchemark_ai.pdf2md(pdf_file_path, process_images, keep_images_inline=True)

        for result in results:
            print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"[MAIN] An error occurred: {e}")

if __name__ == "__main__":
    main()