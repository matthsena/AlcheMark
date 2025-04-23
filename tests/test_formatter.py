import pytest
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alchemark_ai.formatter.formatter_md import FormatterMD
from alchemark_ai.models import PDFResult, FormattedResult, Table, Image


@pytest.fixture
def mock_pdf_result():
    return PDFResult(
        metadata={
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
            "file_path": "/path/to/sample.pdf",
            "page_count": 1,
            "page": 1
        },
        toc_items=[],
        tables=[],
        images=[],
        graphics=[],
        text="# Sample Document\n\nThis is a sample text with a [link](https://example.com).\n\n- Item 1\n- Item 2\n\n1. Numbered item 1\n2. Numbered item 2",
        words=[]
    )


@pytest.fixture
def mock_pdf_result_empty_text():
     return PDFResult(
        metadata={
            "format": "PDF 1.7",
            "title": "Empty",
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "",
            "producer": "",
            "creationDate": "",
            "modDate": "",
            "trapped": "",
            "encryption": None,
            "file_path": "/path/to/empty.pdf",
            "page_count": 1,
            "page": 1
        },
        toc_items=[],
        tables=[],
        images=[],
        graphics=[],
        text="",
        words=[]
    )


@pytest.fixture
def mock_pdf_result_with_table():
    return PDFResult(
        metadata={
            "format": "PDF 1.7",
            "title": "Sample Table",
            "author": "Author",
            "subject": "",
            "keywords": "",
            "creator": "Creator",
            "producer": "Producer",
            "creationDate": "2023-01-01",
            "modDate": "2023-01-01",
            "trapped": "",
            "encryption": None,
            "file_path": "/path/to/sample_table.pdf",
            "page_count": 1,
            "page": 1
        },
        toc_items=[],
        tables=[Table(bbox=[0,0,100,100], rows=2, columns=2)],
        images=[],
        graphics=[],
        text="""# Sample Document with Table

Here is a simple table:

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

Some more text.
""",
        words=[]
    )


@pytest.fixture
def mock_pdf_result_with_images():
    return PDFResult(
        metadata={
            "format": "PDF 1.7",
            "title": "Sample Images",
            "author": "Author",
            "subject": "",
            "keywords": "",
            "creator": "Creator",
            "producer": "Producer",
            "creationDate": "2023-01-01",
            "modDate": "2023-01-01",
            "trapped": "",
            "encryption": None,
            "file_path": "/path/to/sample_images.pdf",
            "page_count": 1,
            "page": 1
        },
        toc_items=[],
        tables=[],
        images=[
            Image(
                number=1,
                bbox={"x0": 0, "y0": 0, "x1": 100, "y1": 100},
                width=100,
                height=100
            ),
            Image(
                number=2,
                bbox={"x0": 0, "y0": 0, "x1": 200, "y1": 200},
                width=200,
                height=200
            )
        ],
        graphics=[],
        text="""# Sample Document with Images

Here is a sample image:

![Image 1](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=)

Some text in between images.

![Image 2](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD+/iiiigD/2Q==)
""",
        words=[]
    )


def test_init_formatter(mock_pdf_result):
    formatter = FormatterMD([mock_pdf_result])
    assert formatter.content == [mock_pdf_result]
    assert hasattr(formatter, 'encoding')


def test_check_content_valid(mock_pdf_result):
    formatter = FormatterMD([mock_pdf_result])
    formatter._check_content()


def test_check_content_not_list():
    formatter = FormatterMD("not a list")
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content must be a List of PDFResult" in str(excinfo.value)


def test_check_content_empty_list():
    formatter = FormatterMD([])
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content is empty" in str(excinfo.value)


def test_check_content_invalid_item():
    formatter = FormatterMD(["not a PDFResult"])
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content must be a List of PDFResult" in str(excinfo.value)


def test_check_content_empty_text(mock_pdf_result_empty_text):
    formatter = FormatterMD([mock_pdf_result_empty_text])
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content text is empty" in str(excinfo.value)


def test_count_markdown_elements():
    formatter = FormatterMD([])
    
    markdown_text = """# Title
## Subtitle

- Item 1
- Item 2

1. First
2. Second

[Link 1](https://example.com)
<https://example.org>
"""
    
    elements = formatter._count_markdown_elements(markdown_text)
    
    assert len(elements['titles']) == 2
    assert len(elements['lists']) == 4
    assert len(elements['links']) == 2
    assert elements['links'][0].text == "Link 1"
    assert elements['links'][0].url == "https://example.com"
    assert elements['links'][1].text == "https://example.org"
    assert elements['links'][1].url == "https://example.org"


def test_count_markdown_elements_empty():
    formatter = FormatterMD([])
    
    elements = formatter._count_markdown_elements("")
    
    assert len(elements['titles']) == 0
    assert len(elements['lists']) == 0
    assert len(elements['links']) == 0


def test_count_markdown_elements_error():
    formatter = FormatterMD([])
    
    def mock_findall_error(*args, **kwargs):
        raise Exception("Test exception")
    
    original_findall = re.findall
    re.findall = mock_findall_error
    
    try:
        with pytest.raises(ValueError) as excinfo:
            formatter._count_markdown_elements("Test text")
        
        assert "Error counting markdown elements" in str(excinfo.value)
    finally:
        re.findall = original_findall


def test_format_success(mock_pdf_result, monkeypatch):
    formatter = FormatterMD([mock_pdf_result])
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    result = formatter.format()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FormattedResult)
    assert result[0].metadata.file_path == "/path/to/sample.pdf"
    assert result[0].metadata.page == 1
    assert len(result[0].elements.titles) == 1
    assert len(result[0].elements.lists) == 4
    assert len(result[0].elements.links) == 1
    assert result[0].language == "en"
    assert result[0].tokens > 0


def test_format_with_missing_attributes(mock_pdf_result, monkeypatch):
    delattr(mock_pdf_result, 'tables')
    
    formatter = FormatterMD([mock_pdf_result])
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    result = formatter.format()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FormattedResult)
    assert isinstance(result[0].elements.tables, list)
    assert len(result[0].elements.tables) == 0 


def test_format_with_table(mock_pdf_result_with_table, monkeypatch):
    formatter = FormatterMD([mock_pdf_result_with_table])
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    result = formatter.format()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FormattedResult)
    assert result[0].metadata.file_path == "/path/to/sample_table.pdf"
    assert len(result[0].elements.tables) == 1
    
    table = result[0].elements.tables[0]
    assert isinstance(table, Table)
    assert table.rows == 2
    assert table.columns == 2
    assert table.content == "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |\n"
    assert result[0].language == "en"
    assert result[0].tokens > 0


def test_format_error():
    formatter = FormatterMD(["not a PDFResult"])
    
    with pytest.raises(ValueError) as excinfo:
        formatter.format()
    
    assert "Error formatting content" in str(excinfo.value)


def test_format_with_inline_images(mock_pdf_result_with_images, monkeypatch):
    formatter = FormatterMD([mock_pdf_result_with_images], keep_images_inline=True)
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    result = formatter.format()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FormattedResult)
    assert len(result[0].elements.images) == 2
    assert result[0].elements.images[0].base64.startswith("data:image/png;base64,")
    assert result[0].elements.images[1].base64.startswith("data:image/jpeg;base64,")
    
    # Verify images are kept inline when keep_images_inline=True
    assert "![Image 1](data:image/png;base64," in result[0].text
    assert "![Image 2](data:image/jpeg;base64," in result[0].text


def test_format_with_image_references(mock_pdf_result_with_images, monkeypatch):
    formatter = FormatterMD([mock_pdf_result_with_images], keep_images_inline=False)
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    result = formatter.format()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FormattedResult)
    assert len(result[0].elements.images) == 2
    
    # Verify image hashes exist
    assert result[0].elements.images[0].hash is not None
    assert result[0].elements.images[1].hash is not None
    
    # Verify inline images are replaced with references
    assert "![Image 1](data:image/png;base64," not in result[0].text
    assert "![Image 2](data:image/jpeg;base64," not in result[0].text
    # Instead of checking for exact hash values, just check for [IMAGE] format
    assert "[IMAGE](" in result[0].text
    # Make sure there are two IMAGE references (one for each image)
    assert result[0].text.count("[IMAGE](") == 2


def test_extract_images(mock_pdf_result_with_images):
    formatter = FormatterMD([mock_pdf_result_with_images])
    
    text = mock_pdf_result_with_images.text
    extracted_images = formatter._extract_images(text)
    
    assert len(extracted_images) == 2
    # The regex returns tuples with two capture groups, one of which will be empty
    assert extracted_images[0][0].startswith("data:image/png;base64,")
    assert extracted_images[1][0].startswith("data:image/jpeg;base64,")


def test_format_error_with_images():
    # Test error handling when extracting images
    formatter = FormatterMD([])
    
    with pytest.raises(ValueError) as excinfo:
        formatter._extract_images(123)  # Passing non-string should raise error
    
    assert "Error extracting images from text" in str(excinfo.value)