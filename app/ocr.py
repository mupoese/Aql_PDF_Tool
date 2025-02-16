import fitz
from PIL import Image
import io
from .language_utils import ocr_with_language_support
import os
import tempfile

def pdf_to_images(pdf_path: str) -> list:
    """Convert PDF pages to images."""
    images = []
    pdf_document = fitz.open(pdf_path)
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    
    return images

def ocr_image(image) -> dict:
    """Perform OCR on an image with language support."""
    # Save image temporarily
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        image.save(tmp_file.name)
        result = ocr_with_language_support(tmp_file.name)
    
    # Clean up
    os.unlink(tmp_file.name)
    return result