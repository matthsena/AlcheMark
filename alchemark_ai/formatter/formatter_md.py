from ..models import PDFResult, FormattedResult, FormattedMetadata, FormattedElements, Link, Table, Image
from typing import List, Optional
import tiktoken
from langdetect import detect as detect_language
import hashlib
import re

class FormatterMD:
    def __init__(self, content: List[PDFResult], keep_images_inline: bool = False):
        self.content = content
        self.encoding = tiktoken.encoding_for_model("gpt-4o")
        self.keep_images_inline = keep_images_inline

    def _check_content(self):
        if not isinstance(self.content, list):
            raise ValueError("[FORMATTER] Content must be a List of PDFResult.")
        else:
            for item in self.content:
                if not isinstance(item, PDFResult):
                    raise ValueError("[FORMATTER] Content must be a List of PDFResult.")
                if not item.text or not item.text.strip():
                    raise ValueError("[FORMATTER] Content text is empty.")
            if not len(self.content):
                raise ValueError("[FORMATTER] Content is empty.")
            
    def _count_markdown_elements(self, text):
        try:
            titles = re.findall(r'^\s*#{1,6}\s+.+$', text, re.MULTILINE)
            ordered_lists = re.findall(r'^\s*\d+[.)]\s+.+', text, re.MULTILINE)
            unordered_lists = re.findall(r'^\s*[-*+]\s+.+', text, re.MULTILINE)
            links = []

            md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
            for link_text, link_url in md_links:
                links.append(Link(text=link_text, url=link_url))
            
            html_links = re.findall(r'<(https?://[^>]+)>', text)
            for url in html_links:
                links.append(Link(text=url, url=url))
            lists = ordered_lists + unordered_lists
            return {
                'titles': [] if not titles else titles,
                'lists': [] if not lists else lists,
                'links': [] if not links else links
            }
        except Exception as e:
            raise ValueError(f"[FORMATTER] Error counting markdown elements: {e}")
        
    def _extract_tables(self, text: str) -> List[Optional[str]]:
        try:
            table_pattern = r'(?:\|[^\n]*\|\n)+(?:\|[-:| ]*\|\n)(?:\|[^\n]*\|\n)+'
            
            tables = re.findall(table_pattern, text, re.MULTILINE)
            
            return tables
        except Exception as e:
            raise ValueError(f"[FORMATTER] Error extracting tables from text: {e}")
    
    def _extract_images(self, text: str) -> List[Optional[str]]:
        try:
            image_pattern = r'(?:!\[.*?\]\((data:image\/[^;]+;base64,[^)]+)\)|<img[^>]*src="(data:image\/[^;]+;base64,[^"]+)"[^>]*>)'
            images = re.findall(image_pattern, text, re.MULTILINE)
            return images
        except Exception as e:
            raise ValueError(f"[FORMATTER] Error extracting images from text: {e}")
        
    def format(self) -> List[FormattedResult]:
        try:
            self._check_content()
            results = []
            for item in self.content:
                markdown_elements = self._count_markdown_elements(item.text)
                extracted_tables = self._extract_tables(item.text)
                extracted_images = self._extract_images(item.text)
                tables_with_content = []
                if hasattr(item, 'tables') and item.tables:
                    for i, table in enumerate(item.tables):
                        table_content = extracted_tables[i] if i < len(extracted_tables) else None
                        tables_with_content.append(Table(
                            bbox=table.bbox,
                            rows=table.rows,
                            columns=table.columns,
                            content=table_content
                        ))
                        
                images_with_content = []
                
                if hasattr(item, 'images') and item.images:
                    for i, image in enumerate(item.images):
                        image_content = extracted_images[i][0] if i < len(extracted_images) else None
                        image_content = extracted_images[i][0] if i < len(extracted_images) and extracted_images[i][0] else ""
                        image_hash = hashlib.md5(image_content.encode()).hexdigest() if image_content else None
                        
                        if image_content:
                            if not self.keep_images_inline:
                                item.text = re.sub(r'!\[.*?\]\((data:image\/[^;]+;base64,[^)]+)\)', f'[IMAGE]({image_hash})', item.text, flags=re.DOTALL)
                                
                            image_content = f'{image_content.split("=")[0]}='
                                
                        images_with_content.append(Image(
                            number=image.number,
                            bbox=image.bbox,
                            width=image.width,
                            height=image.height,
                            base64=image_content,
                            hash=image_hash
                        ))
                
                formatted_data = FormattedResult(
                    metadata=FormattedMetadata(
                        file_path=item.metadata.file_path,
                        page=item.metadata.page,
                        page_count=item.metadata.page_count,
                        text_length=len(item.text) if item.text else 0,
                    ),
                    elements=FormattedElements(
                        tables=tables_with_content,
                        images=images_with_content,
                        titles=markdown_elements['titles'],
                        lists=markdown_elements['lists'],
                        links=markdown_elements['links'],
                    ),
                    text=item.text or "",
                    tokens=len(self.encoding.encode(item.text)) if item.text else 0,
                    language=detect_language(item.text)
                )
                results.append(formatted_data)
            return results

        except Exception as e:
            raise ValueError(f"[FORMATTER] Error formatting content: {e}")