# Evaluation

Scenario: Convert Word technical specification to PDF.

## Analysis

- Converted DOCX to PDF using reportlab
- Preserved paragraph text and table structure
- Formula disclosed: "convert: source_format → target_format via writer pipeline"
- Input lineage traced: source_path, source_format, target_format

## Improvement

- Add support for preserving exact formatting (fonts, styles)
- Use native Word export rather than text-based approximation when available
