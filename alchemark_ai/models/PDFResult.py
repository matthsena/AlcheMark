from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, model_validator

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
    width: int
    height: int
    base64: Optional[str] = None
    hash: Optional[str] = None
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


class Table(BaseModel):
    bbox: Union[Rect, List[float]]
    rows: int
    columns: int
    content: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def process_bbox(cls, data):
        if isinstance(data, dict) and 'bbox' in data:
            if isinstance(data['bbox'], list) and len(data['bbox']) == 4:
                data['bbox'] = {
                    'x0': data['bbox'][0],
                    'y0': data['bbox'][1],
                    'x1': data['bbox'][2],
                    'y1': data['bbox'][3]
                }
        return data


class PDFResult(BaseModel):
    metadata: Metadata
    toc_items: List[List[Union[int, str]]]
    tables: List[Table]
    images: List[Image]
    graphics: List[Dict[str, Any]]
    text: str
    words: List[Any]