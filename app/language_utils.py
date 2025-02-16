from langdetect import detect
from typing import List, Dict
import pytesseract
from bidi.algorithm import get_display
import arabic_reshaper
import re
import hunspell

# Language mapping for Tesseract
LANGUAGE_MAPPING = {
    'ar': 'ara',    # Arabic
    'he': 'heb',    # Hebrew
    'fa': 'fas',    # Persian/Farsi
    'ur': 'urd',    # Urdu
    'en': 'eng',    # English
}

# RTL languages
RTL_LANGUAGES = {'ar', 'he', 'fa', 'ur'}

def detect_language(text: str) -> str:
    """Detect the primary language of the text."""
    try:
        return detect(text)
    except:
        return 'en'  # Default to English if detection fails

def is_rtl_language(lang_code: str) -> bool:
    """Check if the language is RTL."""
    return lang_code in RTL_LANGUAGES

def get_tesseract_lang_string(detected_lang: str) -> str:
    """Convert detected language code to Tesseract language code."""
    return LANGUAGE_MAPPING.get(detected_lang, 'eng')

def process_rtl_text(text: str, lang_code: str) -> str:
    """Process RTL text appropriately."""
    if is_rtl_language(lang_code):
        # Reshape Arabic text
        if lang_code == 'ar':
            text = arabic_reshaper.reshape(text)
        # Apply RTL algorithm
        text = get_display(text)
    return text

def ocr_with_language_support(image_path: str) -> Dict[str, str]:
    """Perform OCR with language detection and appropriate processing."""
    # Try OCR with multiple languages
    text = pytesseract.image_to_string(
        image_path,
        lang='+'.join(LANGUAGE_MAPPING.values()),
        config='--psm 3'
    )
    
    # Detect the primary language
    lang_code = detect_language(text)
    
    # Process text according to detected language
    processed_text = process_rtl_text(text, lang_code)
    
    return {
        'text': processed_text,
        'detected_language': lang_code,
        'language_name': LANGUAGE_MAPPING.get(lang_code, 'Unknown')
    }

def get_font_for_language(language_code: str) -> str:
    """Return appropriate font for the given language."""
    rtl_languages = {'ar', 'he', 'fa', 'ur'}
    
    if language_code in rtl_languages:
        return 'Amiri'  # For Arabic, Hebrew, Persian, and Urdu
    return 'DejaVu'     # Default font for Latin scripts

def get_text_direction(language_code: str) -> str:
    """Return text direction for the given language."""
    rtl_languages = {'ar', 'he', 'fa', 'ur'}
    return 'rtl' if language_code in rtl_languages else 'ltr'