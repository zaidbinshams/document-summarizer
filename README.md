# Document Summary Assistant

An AI-powered web application that accepts PDF and image documents, extracts their text using PDF parsing or OCR, and generates concise summaries with key points.

## Approach

See [APPROACH.md](APPROACH.md) for the brief project approach and implementation details.

## Features

- Upload PDF and image files
- Drag-and-drop file upload
- PDF text extraction
- OCR for images and scanned PDFs
- AI-generated summaries
- Short, medium, and long summary lengths
- Key point extraction
- Loading and error states
- Responsive interface

## Tech Stack

### Frontend
- React
- Vite
- CSS

### Backend
- Python
- FastAPI
- PyMuPDF
- Tesseract OCR
- Pillow
- Google Gemini API

## Project Structure

```text
document-summary-assistant/
├── frontend/
└── backend/