import time
from pydantic import BaseModel, Field

class FormattedMetadata(BaseModel):
    file_path: str
    page: int
    page_count: int
    text_length: int
    processed_timestamp: float = Field(default_factory=time.time)


class FormattedElements(BaseModel):
    tables: int = 0
    images: int = 0
    titles: int = 0
    lists: int = 0
    links: int = 0

class FormattedResult(BaseModel):
    metadata: FormattedMetadata
    elements: FormattedElements
    text: str
    tokens: int
