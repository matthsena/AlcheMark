from ..models import PDFResult, FormattedResult, FormattedMetadata, FormattedElements, Link
from typing import List
import tiktoken
from langdetect import detect as detect_language
import re

class FormatterMD:
    def __init__(self, content: List[PDFResult]):
        self.content = content
        self.encoding = tiktoken.encoding_for_model("gpt-4o")

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
        
    def format(self) -> List[FormattedResult]:
        try:
            self._check_content()
            results = []
            for item in self.content:
                markdown_elements = self._count_markdown_elements(item.text)
                formatted_data = FormattedResult(
                    metadata=FormattedMetadata(
                        file_path=item.metadata.file_path,
                        page=item.metadata.page,
                        page_count=item.metadata.page_count,
                        text_length=len(item.text) if item.text else 0,
                    ),
                    elements=FormattedElements(
                        tables=item.tables if hasattr(item, 'tables') and item.tables else [],
                        images=item.images if hasattr(item, 'images') and item.images else [],
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