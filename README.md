# Markdown to DOCX Converter

## Overview
The Markdown to DOCX converter is a tool designed to convert markdown files into DOCX documents. This converter is especially useful for users who work with markdown and need to create formal documents in a widely accepted format without losing formatting and structure.

## Features
- **Supports various markdown syntax**: All standard markdown syntax is supported, ensuring that your documents preserve their intended formatting.
- **Customizable output**: Easily customize fonts and line spacing to suit your document's requirements.
- **Batch conversion**: Convert multiple markdown files at once, saving time and effort.

## Installation
To install the Markdown to DOCX converter, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/ShadowC707/MD-to-DOCX-converter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd MD-to-DOCX-converter
   ```
3. Install the necessary dependencies:
   ```bash
   npm install
   ```

## Usage Instructions
To convert a markdown file to DOCX, use the following command:
```bash
node converter.js input.md output.docx
```

Replace `input.md` with the path to your markdown file and `output.docx` with the desired name for the DOCX output file.

## Customization Options
You can customize the output DOCX file by modifying the configuration settings in `config.js`. The following options are available:
- **Fonts**: Change the default font of the document by updating the `fontFamily` property.
   ```javascript
   fontFamily: 'Arial', // Default: 'Times New Roman'
   ```
- **Line Spacing**: Adjust line spacing by modifying the `lineSpacing` property.
   ```javascript
   lineSpacing: 1.5, // Default: 1
   ```

Ensure to review the `config.js` file for further customization options.

## Conclusion
This markdown to DOCX converter tool is a powerful resource for users needing to transition markdown content into professionally formatted DOCX documents. For contributions or issues, feel free to create a pull request or open an issue in this repository.