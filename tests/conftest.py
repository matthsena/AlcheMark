import os
import pytest

@pytest.fixture
def sample_pdf_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample', 'Sample.pdf')

@pytest.fixture
def invalid_pdf_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample', 'NonExistent.pdf')

@pytest.fixture
def non_pdf_file_path(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("This is not a PDF file")
    return str(file_path) 