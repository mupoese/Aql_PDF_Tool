import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path

def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

def ocr_image(image):
    return pytesseract.image_to_string(image)
