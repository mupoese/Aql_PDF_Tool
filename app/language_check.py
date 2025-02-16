from langdetect import detect, DetectorFactory
from typing import Dict, List, Optional
import re
from collections import Counter
import hunspell

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Language configurations
SUPPORTED_LANGUAGES = {
    'ar': {
        'name': 'Arabic',
        'direction': 'rtl',
        'hunspell_dict': 'ar',
        'tesseract_lang': 'ara',
        'variants': ['ara', 'ar-EG', 'ar-SA', 'ar-IQ', 'ar-SY']
    },
    'he': {
        'name': 'Hebrew',
        'direction': 'rtl',
        'hunspell_dict': 'he',
        'tesseract_lang': 'heb',
        'variants': ['heb', 'he-IL']
    },
    'fa': {
        'name': 'Persian/Farsi',
        'direction': 'rtl',
        'hunspell_dict': 'fa',
        'tesseract_lang': 'fas',
        'variants': ['fas', 'fa-IR']
    },
    'ur': {
        'name': 'Urdu',
        'direction': 'rtl',
        'hunspell_dict': 'ur',
        'tesseract_lang': 'urd',
        'variants': ['urd', 'ur-PK']
    },
    'en': {
        'name': 'English',
        'direction': 'ltr',
        'hunspell_dict': 'en_US',
        'tesseract_lang': 'eng',
        'variants': ['eng', 'en-US', 'en-GB']
    }
}

class LanguageChecker:
    def __init__(self):
        # Initialize Hunspell dictionaries
        self.spellcheckers = {}
        for lang_code, config in SUPPORTED_LANGUAGES.items():
            try:
                self.spellcheckers[lang_code] = hunspell.HunSpell(
                    f"/usr/share/hunspell/{config['hunspell_dict']}.dic",
                    f"/usr/share/hunspell/{config['hunspell_dict']}.aff"
                )
            except:
                print(f"Warning: Could not load {lang_code} dictionary")

    def detect_language(self, text: str) -> Dict[str, any]:
        """
        Detect the language of the text with confidence score and direction.
        """
        if not text.strip():
            return {
                'language': 'unknown',
                'confidence': 0.0,
                'direction': 'ltr',
                'name': 'Unknown'
            }

        try:
            detected = detect(text)
            lang_config = SUPPORTED_LANGUAGES.get(detected, SUPPORTED_LANGUAGES['en'])
            
            return {
                'language': detected,
                'confidence': self._calculate_confidence(text, detected),
                'direction': lang_config['direction'],
                'name': lang_config['name']
            }
        except:
            return {
                'language': 'en',
                'confidence': 0.5,
                'direction': 'ltr',
                'name': 'English (fallback)'
            }

    def _calculate_confidence(self, text: str, detected_lang: str) -> float:
        """
        Calculate confidence score based on word recognition and character sets.
        """
        if detected_lang not in self.spellcheckers:
            return 0.5

        words = self._tokenize(text)
        if not words:
            return 0.0

        recognized_words = sum(1 for word in words 
                             if self.spellcheckers[detected_lang].spell(word))
        return recognized_words / len(words) if words else 0.0

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words, handling both RTL and LTR scripts.
        """
        # Remove numbers and special characters
        text = re.sub(r'[\d_]', ' ', text)
        # Split on whitespace and remove empty strings
        return [word for word in text.split() if word.strip()]

    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        Comprehensive text analysis including language detection,
        script identification, and mixed language detection.
        """
        paragraphs = text.split('\n')
        paragraph_analysis = []
        
        for para in paragraphs:
            if para.strip():
                lang_info = self.detect_language(para)
                paragraph_analysis.append({
                    'text': para,
                    'language': lang_info,
                    'word_count': len(self._tokenize(para))
                })

        # Determine dominant language
        lang_counts = Counter(p['language']['language'] 
                            for p in paragraph_analysis)
        dominant_lang = lang_counts.most_common(1)[0][0]

        return {
            'dominant_language': SUPPORTED_LANGUAGES[dominant_lang]['name'],
            'language_distribution': dict(lang_counts),
            'paragraph_analysis': paragraph_analysis,
            'total_words': sum(p['word_count'] for p in paragraph_analysis)
        }

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Return list of supported languages with their configurations.
        """
        return [{
            'code': code,
            'name': config['name'],
            'direction': config['direction'],
            'tesseract_lang': config['tesseract_lang']
        } for code, config in SUPPORTED_LANGUAGES.items()]

    def check_spelling(self, text: str, lang_code: str) -> Dict[str, any]:
        """
        Check spelling for the given text in the specified language.
        """
        if lang_code not in self.spellcheckers:
            return {
                'error': f'Spellchecker not available for {lang_code}',
                'words_checked': 0,
                'misspelled_words': []
            }

        words = self._tokenize(text)
        misspelled = [word for word in words 
                     if not self.spellcheckers[lang_code].spell(word)]

        return {
            'words_checked': len(words),
            'misspelled_words': misspelled,
            'misspelled_count': len(misspelled),
            'suggestions': {
                word: self.spellcheckers[lang_code].suggest(word)
                for word in misspelled[:10]  # Limit suggestions to first 10 words
            }
        }