import alchemark_ai
from pathlib import Path

def main():
    pdf_file_path = Path(__file__).parent / '../sample/Sample.pdf'
    process_images = True

    try:
        results = alchemark_ai.pdf2md(str(pdf_file_path.resolve()), process_images, keep_images_inline=True)

        for result in results:
            print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"[MAIN] An error occurred: {e}")

if __name__ == "__main__":
    main()