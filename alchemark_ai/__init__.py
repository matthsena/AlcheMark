"""
AlcheMark AI - PDF to Markdown Conversion Library

A toolkit that converts PDF documents into structured Markdown 
with rich metadata and markdown element annotations.
"""

from .pdf2md import PDF2MarkDown
from .formatter import FormatterMD
from .models import FormattedResult
from typing import List, Optional

__version__ = "0.1.0"

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