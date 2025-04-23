"""
AlcheMark AI - PDF to Markdown Conversion Library

A toolkit that converts PDF documents into structured Markdown 
with rich metadata and markdown element annotations.
"""

# Use relative imports for internal package structure
from .pdf2md.pdf2md import PDF2MarkDown
from .formatter.formatter_md import FormatterMD
from .models.FormattedResult import FormattedResult, FormattedMetadata, FormattedElements
from typing import List

__version__ = "0.1.6"

# Define what gets imported with 'from alchemark_ai import *'
__all__ = ['FormattedResult', 'pdf2md']

def pdf2md(
    pdf_file_path: str, 
    process_images: bool = False,
    keep_images_inline: bool = False
) -> List[FormattedResult]:
    """
    Convert a PDF file to markdown and format the results.
    
    Args:
        pdf_file_path: Path to the PDF file
        process_images: Whether to extract and process images
        keep_images_inline: Whether to keep images inline in the markdown text or to use a reference to the image (Image hash)
    Returns:
        List of FormattedResult objects with the following structure:
        
        FormattedResult:
            metadata: FormattedMetadata
                file_path: str
                page: int
                page_count: int
                text_length: int
                processed_timestamp: float
            elements: FormattedElements
                tables: List[Table]
                images: List[Image]
                titles: List[str]
                lists: List[str]
                links: List[Link]
            text: str
            tokens: int
            language: str
    """
    pdf_converter = PDF2MarkDown(pdf_file_path, process_images)
    markdown_content = pdf_converter.convert()
    formatter = FormatterMD(markdown_content, keep_images_inline)
    return formatter.format() 