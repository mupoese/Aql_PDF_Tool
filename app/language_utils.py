import pytesseract
from .language_check import LanguageChecker

# Initialize language checker
lang_checker = LanguageChecker()

def ocr_with_language_support(image_path: str) -> dict:
    """
    Perform OCR with language detection and support for multiple languages.
    """
    # First try with all supported languages
    text = pytesseract.image_to_string(
        image_path,
        lang='+'.join(['eng', 'ara', 'heb', 'fas', 'urd']),
        config='--psm 3'
    )
    
    # Analyze the text for language
    if text.strip():
        analysis = lang_checker.analyze_text(text)
        dominant_lang = analysis['dominant_language']
        
        # If confident about language, retry OCR with specific language
        if analysis.get('confidence', 0) > 0.5:
            text = pytesseract.image_to_string(
                image_path,
                lang=dominant_lang,
                config='--psm 3'
            )
    
    return {
        'text': text,
        'language_analysis': analysis if text.strip() else None
    }