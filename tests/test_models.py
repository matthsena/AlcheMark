import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import PDFResult, FormattedResult, FormattedMetadata, FormattedElements, Link
from models.PDFResult import Rect, Metadata, Image, Table


def test_rect_model():
    rect = Rect(x0=1.0, y0=2.0, x1=3.0, y1=4.0)
    assert rect.x0 == 1.0
    assert rect.y0 == 2.0
    assert rect.x1 == 3.0
    assert rect.y1 == 4.0


def test_metadata_model():
    metadata = Metadata(
        format="PDF 1.7",
        title="Sample",
        author="Author",
        subject="Subject",
        keywords="Keywords",
        creator="Creator",
        producer="Producer",
        creationDate="2023-01-01",
        modDate="2023-01-01",
        trapped="False",
        encryption=None,
        file_path="/path/to/sample.pdf",
        page_count=10,
        page=1
    )
    
    assert metadata.format == "PDF 1.7"
    assert metadata.title == "Sample"
    assert metadata.author == "Author"
    assert metadata.subject == "Subject"
    assert metadata.keywords == "Keywords"
    assert metadata.creator == "Creator"
    assert metadata.producer == "Producer"
    assert metadata.creationDate == "2023-01-01"
    assert metadata.modDate == "2023-01-01"
    assert metadata.trapped == "False"
    assert metadata.encryption is None
    assert metadata.file_path == "/path/to/sample.pdf"
    assert metadata.page_count == 10
    assert metadata.page == 1


def test_image_model():
    image = Image(
        number=1,
        bbox=Rect(x0=1.0, y0=2.0, x1=3.0, y1=4.0),
        width=100,
        height=200
    )
    
    assert image.number == 1
    assert isinstance(image.bbox, Rect)
    assert image.bbox.x0 == 1.0
    assert image.width == 100
    assert image.height == 200


def test_image_model_with_dict_bbox():
    image_data = {
        "number": 1,
        "bbox": {"x0": 1.0, "y0": 2.0, "x1": 3.0, "y1": 4.0},
        "width": 100,
        "height": 200,
    }
    
    image = Image.model_validate(image_data)
    
    assert image.number == 1
    assert isinstance(image.bbox, Rect)
    assert image.bbox.x0 == 1.0
    assert image.width == 100
    assert image.height == 200


def test_table_model():
    table = Table(
        bbox=Rect(x0=1.0, y0=2.0, x1=3.0, y1=4.0),
        rows=5,
        columns=3,
        content="Cell 1 Cell 2 Cell 3 Cell 4 Cell 5 Cell 6"
    )
    
    assert isinstance(table.bbox, Rect)
    assert table.bbox.x0 == 1.0
    assert table.rows == 5
    assert table.columns == 3
    assert table.content == "Cell 1 Cell 2 Cell 3 Cell 4 Cell 5 Cell 6"

def test_table_model_with_list_bbox():
    table_data = {
        "bbox": [1.0, 2.0, 3.0, 4.0],
        "rows": 5,
        "columns": 3,
        "content": "Cell 1 Cell 2 Cell 3 Cell 4 Cell 5 Cell 6"
    }
    
    table = Table.model_validate(table_data)
    
    assert isinstance(table.bbox, Rect)
    assert table.bbox.x0 == 1.0
    assert table.bbox.y0 == 2.0
    assert table.bbox.x1 == 3.0
    assert table.bbox.y1 == 4.0
    assert table.rows == 5
    assert table.columns == 3
    assert table.content == "Cell 1 Cell 2 Cell 3 Cell 4 Cell 5 Cell 6"

def test_pdf_result_model():
    pdf_result = PDFResult(
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
        text="Sample text",
        words=[]
    )
    
    assert isinstance(pdf_result.metadata, Metadata)
    assert pdf_result.metadata.title == "Sample"
    assert pdf_result.metadata.file_path == "/path/to/sample.pdf"
    assert isinstance(pdf_result.toc_items, list)
    assert isinstance(pdf_result.tables, list)
    assert isinstance(pdf_result.images, list)
    assert isinstance(pdf_result.graphics, list)
    assert pdf_result.text == "Sample text"
    assert isinstance(pdf_result.words, list)


def test_formatted_result_model():
    formatted_result = FormattedResult(
        metadata=FormattedMetadata(
            file_path="/path/to/sample.pdf",
            page=1,
            page_count=10,
            text_length=100
        ),
        elements=FormattedElements(
            tables=[],
            images=[],
            titles=["# Title"],
            lists=["- Item 1"],
            links=[Link(text="Link", url="https://example.com")]
        ),
        text="Sample text",
        tokens=20,
        language="en"
    )
    
    assert isinstance(formatted_result.metadata, FormattedMetadata)
    assert formatted_result.metadata.file_path == "/path/to/sample.pdf"
    assert formatted_result.metadata.page == 1
    assert formatted_result.metadata.page_count == 10
    assert formatted_result.metadata.text_length == 100
    
    assert isinstance(formatted_result.elements, FormattedElements)
    assert isinstance(formatted_result.elements.tables, list)
    assert isinstance(formatted_result.elements.images, list)
    assert formatted_result.elements.titles == ["# Title"]
    assert formatted_result.elements.lists == ["- Item 1"]
    assert len(formatted_result.elements.links) == 1
    assert formatted_result.elements.links[0].text == "Link"
    assert formatted_result.elements.links[0].url == "https://example.com"
    
    assert formatted_result.text == "Sample text"
    assert formatted_result.tokens == 20
    assert formatted_result.language == "en" 