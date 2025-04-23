# AlcheMark.

Your files ready for Gen AI ✨🚀

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
# pdf_file_path: Path to the PDF document to be converted
# process_images: When True, extracts images from the PDF (default: False)
# keep_images_inline: When True, keeps base64 images inline in markdown; when False, 
#                     replaces with references to image hashes (default: False)
results = pdf2md("path/to/document.pdf", process_images=True, keep_images_inline=True)

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
#     "images": List[Image],  # Images extracted from the page (with optional base64 data)
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

## Google Colab Example

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16l9e60fktbmu_0fo9rfOxZpWbpq2weZH?usp=sharing)

Try AlcheMark AI directly in your browser with our interactive Google Colab notebook!

## Overview

AlcheMark AI provides a seamless solution for converting PDF documents into well-structured Markdown format. The tool not only extracts the text content but also analyzes and catalogs various elements like tables, images, headings, lists, and links while tracking token counts for LLM compatibility.

## Key Features

- **PDF to Markdown Conversion**: Transform PDF documents into clean, organized Markdown
- **Rich Metadata Extraction**: Preserve document metadata including title, author, creation date
- **Element Analysis**: Automatic detection and counting of markdown elements (headings, lists, links)
- **Table & Image Support**: Extract and format tables and images from PDFs
- **Inline Image Handling**: Option to keep images inline as base64 or replace with image references
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
| **elements.images** | `List[Image]` | Images extracted from the page with their metadata, including optional base64 content and hash |
| **elements.titles** | `List[str]` | Headings and titles detected in the page |
| **elements.lists** | `List[str]` | List items (ordered and unordered) found in the page |
| **elements.links** | `List[Link]` | Hyperlinks with their display text and target URLs |
| **text** | `str` | The complete markdown text content of the page |
| **tokens** | `int` | Token count for the page (useful for LLM context planning) |
| **language** | `str` | Detected language of the page content |

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| **process_images** | `False` | Enable extraction and processing of images from the PDF |
| **keep_images_inline** | `False` | Keep images inline as base64 in the markdown text. When set to `False`, images are replaced with references (`[IMAGE](hash)`) |

## Test Coverage

AlcheMark AI maintains a high test coverage to ensure reliability:

```
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
alchemark_ai/configs/logger.py               2      0   100%
alchemark_ai/formatter/formatter_md.py      80      2    98%
alchemark_ai/models/FormattedResult.py      25      0   100%
alchemark_ai/models/PDFResult.py            56      0   100%
alchemark_ai/pdf2md/pdf2md.py               30      0   100%
------------------------------------------------------------
TOTAL                                      193      2    99%
```

Current test suite includes 37 tests covering all major functionality, with an overall coverage of 99%.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
