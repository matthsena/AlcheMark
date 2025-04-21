import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pdf2md.pdf2md import PDF2MarkDown
from src.formatter.formatter_md import FormatterMD
from src.models import PDFResult, FormattedResult


def test_pdf_to_formatted_markdown_integration(sample_pdf_path, monkeypatch):
    mock_pdf_result = [{
        "metadata": {
            "format": "PDF 1.7",
            "title": "Sample",
            "author": "Author",
            "subject": "",
            "keywords": "",
            "creator": "Creator",
            "producer": "Producer",
            "creationDate": "2023-01-01",
            "modDate": "2023-01-01",
            "trapped": "",
            "encryption": None,
            "file_path": sample_pdf_path,
            "page_count": 1,
            "page": 1
        },
        "toc_items": [],
        "tables": [],
        "images": [],
        "graphics": [],
        "text": "# Sample Document\n\nThis is a sample text with a [link](https://example.com).\n\n- Item 1\n- Item 2\n\n1. Numbered item 1\n2. Numbered item 2",
        "words": []
    }]
    
    def mock_to_markdown(*args, **kwargs):
        return mock_pdf_result
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("pymupdf4llm.to_markdown", mock_to_markdown)
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    pdf_converter = PDF2MarkDown(sample_pdf_path)
    markdown_content = pdf_converter.convert()
    
    assert isinstance(markdown_content, list)
    assert len(markdown_content) == 1
    assert isinstance(markdown_content[0], PDFResult)
    assert markdown_content[0].text.startswith("# Sample Document")
    
    formatter = FormatterMD(markdown_content)
    formatted_results = formatter.format()
    
    assert isinstance(formatted_results, list)
    assert len(formatted_results) == 1
    assert isinstance(formatted_results[0], FormattedResult)
    
    assert formatted_results[0].metadata.file_path == sample_pdf_path
    assert formatted_results[0].metadata.page == 1
    assert formatted_results[0].metadata.page_count == 1
    assert formatted_results[0].metadata.text_length > 0
    
    assert len(formatted_results[0].elements.titles) == 1
    assert len(formatted_results[0].elements.lists) == 4
    assert len(formatted_results[0].elements.links) == 1
    
    assert formatted_results[0].text.startswith("# Sample Document")
    assert formatted_results[0].tokens > 0
    assert formatted_results[0].language == "en" 