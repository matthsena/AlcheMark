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

__version__ = "0.1.5"

# Define what gets imported with 'from alchemark_ai import *'
__all__ = ['PDF2MarkDown', 'FormatterMD', 'FormattedResult', 'FormattedMetadata', 'FormattedElements', 'pdf2md']

def pdf2md(
    pdf_file_path: str, 
    process_images: bool = False
) -> List[FormattedResult]:
    """
    Convert a PDF file to markdown and format the results.
    
    Args:
        pdf_file_path: Path to the PDF file
        process_images: Whether to extract and process images
        
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
    formatter = FormatterMD(markdown_content)
    return formatter.format() 