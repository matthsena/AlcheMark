from typing import List, Dict, Any, Optional, Tuple, Union
from pydantic import BaseModel, Field, model_validator

class Rect(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float

class Metadata(BaseModel):
    format: str
    title: str = ""
    author: str = ""
    subject: str = ""
    keywords: str = ""
    creator: str = ""
    producer: str = ""
    creationDate: str = ""
    modDate: str = ""
    trapped: str = ""
    encryption: Optional[Any] = None
    file_path: str
    page_count: int
    page: int


class Image(BaseModel):
    number: int
    bbox: Rect
    transform: Tuple[float, float, float, float, float, float]
    width: int
    height: int
    colorspace: int
    cs_name: str = Field(..., alias='cs-name')
    xres: int
    yres: int
    bpc: int
    size: int
    has_mask: bool = Field(..., alias='has-mask')

    @model_validator(mode='before')
    @classmethod
    def process_rect(cls, data):
        if isinstance(data, dict) and 'bbox' in data and hasattr(data['bbox'], 'x0'):
            bbox = data['bbox']
            data['bbox'] = {
                'x0': bbox.x0,
                'y0': bbox.y0,
                'x1': bbox.x1,
                'y1': bbox.y1
            }
        return data


class PDFResult(BaseModel):
    metadata: Metadata
    toc_items: List[List[Union[int, str]]]
    tables: List[Dict[str, Any]]
    images: List[Image]
    graphics: List[Dict[str, Any]]
    text: str
    words: List[Any]