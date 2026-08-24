import fitz
from io import BytesIO

from PIL import Image
import pytesseract


def extract_pdf_text(file_bytes: bytes) -> str:
    document = fitz.open(stream=file_bytes, filetype="pdf")

    text = []

    for page in document:
        page_text = page.get_text("text")

        if page_text.strip():
            text.append(page_text.strip())

    extracted_text = "\n\n".join(text).strip()

    if extracted_text:
        document.close()
        return extracted_text

    ocr_text = []

    for page in document:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image = Image.open(BytesIO(pixmap.tobytes("png")))

        page_text = pytesseract.image_to_string(image).strip()

        if page_text:
            ocr_text.append(page_text)

    document.close()

    return "\n\n".join(ocr_text).strip()