from io import BytesIO
import shutil

from PIL import Image
import pytesseract


tesseract_path = shutil.which("tesseract")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_image_text(file_bytes: bytes) -> str:
    image = Image.open(BytesIO(file_bytes))

    image.load()

    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    text = pytesseract.image_to_string(image)

    return text.strip()