from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pytesseract

from services.pdf_extractor import extract_pdf_text
from services.ocr import extract_image_text
from services.summarizer import generate_summary


app = FastAPI(title="Document Summary Assistant")

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://document-summarizer.pages.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummaryRequest(BaseModel):
    text: str
    length: str = "medium"


@app.get("/")
def root():
    return {
        "message": "Document Summary Assistant API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/api/extract")
async def extract_text(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, PNG and WEBP files are supported."
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10 MB."
        )

    try:
        if file.content_type == "application/pdf":
            text = extract_pdf_text(file_bytes)
        else:
            text = extract_image_text(file_bytes)

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract any text from the document."
            )

        return {
            "filename": file.filename,
            "text": text,
            "characters": len(text),
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to extract text from this document."
        )


@app.post("/api/summarize")
async def summarize_document(request: SummaryRequest):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="No document text provided."
        )

    if request.length not in ["short", "medium", "long"]:
        raise HTTPException(
            status_code=400,
            detail="Summary length must be short, medium, or long."
        )

    try:
        result = generate_summary(
            request.text,
            request.length
        )

        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to extract text from this document."
        )