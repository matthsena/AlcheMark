import time
from pydantic import BaseModel, Field
from typing import List, Any
from .PDFResult import Image, Table

class Link(BaseModel):
    text: str
    url: str

class FormattedMetadata(BaseModel):
    file_path: str
    page: int
    page_count: int
    text_length: int
    processed_timestamp: float = Field(default_factory=time.time)


class FormattedElements(BaseModel):
    tables: List[Table] = []
    images: List[Image] = []
    titles: List[str] = []
    lists: List[str] = []
    links: List[Link] = []

class FormattedResult(BaseModel):
    metadata: FormattedMetadata
    elements: FormattedElements
    text: str
    tokens: int
    language: str
