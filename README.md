# AlcheMark AI. 

<p align="center">
  <img src="assets/icon.png" alt="AlcheMark AI Logo" width="400"/>
</p>

AlcheMark is a lightweight, alchemical-inspired toolkit that transmutes PDF documents into structured Markdown pages—complete with rich metadata and markdown element annotations—empowering you to uncover insights page by page.

## Overview

AlcheMark AI provides a seamless solution for converting PDF documents into well-structured Markdown format. The tool not only extracts the text content but also analyzes and catalogs various elements like tables, images, headings, lists, and links while tracking token counts for LLM compatibility.

## Key Features

- **PDF to Markdown Conversion**: Transform PDF documents into clean, organized Markdown
- **Rich Metadata Extraction**: Preserve document metadata including title, author, creation date
- **Element Analysis**: Automatic detection and counting of markdown elements (headings, lists, links)
- **Table & Image Support**: Extract and format tables and images from PDFs
- **Token Counting**: Built-in token counting using tiktoken for LLM integration
- **Structured Output**: Get page-by-page results with detailed metadata

## Project Structure

- **pdf2md**: Core module for PDF to Markdown conversion using pymupdf4llm
- **formatter**: Processing and analysis of converted markdown content
- **models**: Pydantic data models for standardized input/output
- **configs**: Configuration settings including logging

## Getting Started

```bash
# Clone the repository
git clone https://github.com/matthsena/AlcheMark-ai.git
cd AlcheMark-ai

# Install dependencies
pip install -r requirements.txt

# Run the example
python -m src.main
```

## How It Works

1. **PDF Processing**: The `PDF2MarkDown` class handles the conversion of PDF files to markdown format using pymupdf4llm
2. **Formatting**: The `FormatterMD` class processes the converted markdown to:
   - Count markdown elements (headings, lists, links)
   - Track tables and images
   - Calculate token counts
   - Structure metadata
3. **Output**: Results are returned as `FormattedResult` objects with standardized structure

## Use Cases

- Convert research papers to markdown for easier reference
- Transform documentation into markdown for integration with wikis
- Prepare PDF content for processing with Large Language Models
- Create searchable and analyzable versions of PDF libraries

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
