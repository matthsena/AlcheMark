import time
from pydantic import BaseModel, Field

class FormattedMetadata(BaseModel):
    file_path: str
    page: int
    page_count: int
    processed_timestamp: float = Field(default_factory=time.time)

class FormattedResult(BaseModel):
    metadata: FormattedMetadata
    tables: int
    images: int
    text: str
    text_length: int
    titles: int
    lists: int
    links: int
