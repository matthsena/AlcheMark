import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alchemark_ai.pdf2md.pdf2md import PDF2MarkDown
from alchemark_ai.models import PDFResult


def test_init_pdf2md():
    file_path = "some/path/to/file.pdf"
    pdf2md = PDF2MarkDown(file_path)
    
    assert pdf2md.file_path == file_path
    assert pdf2md.page_chunks is True
    assert pdf2md.process_images is False
    
    pdf2md = PDF2MarkDown(file_path, process_images=True)
    assert pdf2md.process_images is True


def test_check_file_not_found(invalid_pdf_path):
    pdf2md = PDF2MarkDown(invalid_pdf_path)
    
    with pytest.raises(ValueError) as excinfo:
        pdf2md._check_file()
    
    assert "does not exist" in str(excinfo.value)


def test_check_file_not_pdf(non_pdf_file_path):
    pdf2md = PDF2MarkDown(non_pdf_file_path)
    
    with pytest.raises(ValueError) as excinfo:
        pdf2md._check_file()
    
    assert "not a PDF file" in str(excinfo.value)


def test_check_file_success(sample_pdf_path):
    pdf2md = PDF2MarkDown(sample_pdf_path)
    
    pdf2md._check_file()


def test_convert_success(sample_pdf_path, monkeypatch):
    mock_result = [{
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
        "text": "Sample text",
        "words": []
    }]
    
    def mock_to_markdown(*args, **kwargs):
        return mock_result
    
    monkeypatch.setattr("pymupdf4llm.to_markdown", mock_to_markdown)
    
    pdf2md = PDF2MarkDown(sample_pdf_path)
    result = pdf2md.convert()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PDFResult)
    assert result[0].metadata.title == "Sample"
    assert result[0].text == "Sample text"


def test_convert_not_list_result(sample_pdf_path, monkeypatch):
    mock_result = {
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
        "text": "Sample text",
        "words": []
    }
    
    def mock_to_markdown(*args, **kwargs):
        return mock_result
    
    monkeypatch.setattr("pymupdf4llm.to_markdown", mock_to_markdown)
    
    pdf2md = PDF2MarkDown(sample_pdf_path)
    result = pdf2md.convert()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PDFResult)


def test_convert_error(invalid_pdf_path):
    pdf2md = PDF2MarkDown(invalid_pdf_path)
    
    with pytest.raises(ValueError) as excinfo:
        pdf2md.convert()
    
    assert "Error converting PDF to Markdown" in str(excinfo.value)


def test_check_file_generic_error(monkeypatch, sample_pdf_path):
    pdf2md = PDF2MarkDown(sample_pdf_path)
    
    def mock_isfile_error(*args, **kwargs):
        raise Exception("Generic test error")
    
    monkeypatch.setattr("os.path.isfile", mock_isfile_error)
    
    with pytest.raises(ValueError) as excinfo:
        pdf2md._check_file()
    
    assert "Invalid file" in str(excinfo.value)
    assert "Generic test error" in str(excinfo.value)


def test_convert_with_images(sample_pdf_path, monkeypatch):
    def mock_to_markdown(*args, **kwargs):
        # Check if process_images parameter is correctly passed to the underlying library
        assert kwargs.get('embed_images') is True
        
        return [{
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
            "images": [
                {
                    "number": 1,
                    "bbox": {"x0": 0, "y0": 0, "x1": 100, "y1": 100},
                    "width": 100,
                    "height": 100
                }
            ],
            "graphics": [],
            "text": "Sample text with image: ![Image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=)",
            "words": []
        }]
    
    monkeypatch.setattr("pymupdf4llm.to_markdown", mock_to_markdown)
    
    pdf2md = PDF2MarkDown(sample_pdf_path, process_images=True)
    result = pdf2md.convert()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PDFResult)
    assert len(result[0].images) == 1
    assert result[0].images[0].number == 1
    assert result[0].images[0].width == 100
    assert result[0].images[0].height == 100
    assert "data:image/png;base64," in result[0].text 