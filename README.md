# AlcheMark AI. 

<p align="center">
  <img src="assets/icon.png" alt="AlcheMark AI Logo" width="400"/>
</p>

AlcheMark is a lightweight PDF to Markdown, alchemical-inspired toolkit that transmutes PDF documents into structured Markdown pages—complete with rich metadata and markdown element annotations—empowering you to uncover insights page by page.

## Installation

```bash
# Install from PyPI
pip install alchemark-ai

# Or install from source
git clone https://github.com/matthsena/AlcheMark-ai.git
cd AlcheMark-ai
pip install -e .
```

## Usage

```python
from alchemark_ai import pdf2md

# Convert PDF to markdown
results = pdf2md("path/to/document.pdf", process_images=True)

# Each result is a FormattedResult object with the structure:
# {
#   "metadata": {
#     "file_path": str,       # Path to the PDF file
#     "page": int,            # Page number
#     "page_count": int,      # Total number of pages
#     "text_length": int,     # Length of the extracted text
#     "processed_timestamp": float  # Processing timestamp
#   },
#   "elements": {
#     "tables": List[Table],  # Tables extracted from the page
#     "images": List[Image],  # Images extracted from the page
#     "titles": List[str],    # Titles/headers detected
#     "lists": List[str],     # List items detected
#     "links": List[Link]     # Links with text and URL
#   },
#   "text": str,              # Markdown text content
#   "tokens": int,            # Number of tokens in the text
#   "language": str           # Detected language
# }

# Access the markdown text of the first page
markdown_text = results[0].text

# Get metadata for the first page
page_number = results[0].metadata.page
total_pages = results[0].metadata.page_count

# Check elements detected in the page
tables_count = len(results[0].elements.tables)
images_count = len(results[0].elements.images)
```

## Overview

AlcheMark AI provides a seamless solution for converting PDF documents into well-structured Markdown format. The tool not only extracts the text content but also analyzes and catalogs various elements like tables, images, headings, lists, and links while tracking token counts for LLM compatibility.

## Key Features

- **PDF to Markdown Conversion**: Transform PDF documents into clean, organized Markdown
- **Rich Metadata Extraction**: Preserve document metadata including title, author, creation date
- **Element Analysis**: Automatic detection and counting of markdown elements (headings, lists, links)
- **Table & Image Support**: Extract and format tables and images from PDFs
- **Token Counting**: Built-in token counting using tiktoken for LLM integration
- **Structured Output**: Get page-by-page results with detailed metadata

## Extracted Data Fields

| Field | Type | Description |
|-------|------|-------------|
| **metadata.file_path** | `str` | Path to the original PDF file |
| **metadata.page** | `int` | Current page number |
| **metadata.page_count** | `int` | Total number of pages in the document |
| **metadata.text_length** | `int` | Character count of the extracted text |
| **metadata.processed_timestamp** | `float` | Unix timestamp when the page was processed |
| **elements.tables** | `List[Table]` | Tables extracted from the page with their structure preserved |
| **elements.images** | `List[Image]` | Images extracted from the page with their metadata |
| **elements.titles** | `List[str]` | Headings and titles detected in the page |
| **elements.lists** | `List[str]` | List items (ordered and unordered) found in the page |
| **elements.links** | `List[Link]` | Hyperlinks with their display text and target URLs |
| **text** | `str` | The complete markdown text content of the page |
| **tokens** | `int` | Token count for the page (useful for LLM context planning) |
| **language** | `str` | Detected language of the page content |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
