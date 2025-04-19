from models import PDFResult

class FormatterMD:
    def __init__(self, content: PDFResult):
        self.content = content

    def _check_content(self):
        if not isinstance(self.content, PDFResult):
            raise ValueError("[FORMATTER] Content must be of type PDFResult.")
        if not self.content.text:
            raise ValueError("[FORMATTER] Content is empty or invalid.")