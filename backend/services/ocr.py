from io import BytesIO

from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_image_text(file_bytes: bytes) -> str:
    image = Image.open(BytesIO(file_bytes))
    return pytesseract.image_to_string(image).strip()