"""
Basic usage example for AlcheMark-AI

This example shows how to use the AlcheMark-AI library to convert a PDF to Markdown.
"""
import os
from alchemark_ai import convert_pdf_to_markdown

def main():
    # Path to the PDF file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_file_path = os.path.join(current_dir, '../sample/Sample.pdf')
    
    # Convert PDF to Markdown with images disabled
    process_images = False
    
    try:
        # Use the library's main function to convert PDF to markdown
        formatted_results = convert_pdf_to_markdown(pdf_file_path, process_images)
        
        # Print results
        print(f"Successfully processed {len(formatted_results)} pages from PDF")
        
        # Access the first page result
        if formatted_results:
            first_page = formatted_results[0]
            print(f"\nPage 1 metadata:")
            print(f"  - File: {first_page.metadata.file_path}")
            print(f"  - Page: {first_page.metadata.page}/{first_page.metadata.page_count}")
            print(f"  - Text length: {first_page.metadata.text_length}")
            print(f"  - Token count: {first_page.tokens}")
            print(f"  - Language: {first_page.language}")
            
            print("\nMarkdown elements:")
            print(f"  - Titles: {len(first_page.elements.titles)}")
            print(f"  - Lists: {len(first_page.elements.lists)}")
            print(f"  - Links: {len(first_page.elements.links)}")
            print(f"  - Tables: {len(first_page.elements.tables)}")
            print(f"  - Images: {len(first_page.elements.images)}")
            
            # Print a sample of the markdown text (first 100 characters)
            print(f"\nMarkdown text sample: \n{first_page.text[:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 