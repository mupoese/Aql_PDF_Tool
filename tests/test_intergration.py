import unittest
import os
from app.main import app
from app.language_check import LanguageChecker
from app.ocr import pdf_to_images, ocr_image

class TestIntegration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.lang_checker = LanguageChecker()

    def test_upload_endpoint(self):
        # Test file upload with both formats
        test_pdf_path = "tests/test_files/test.pdf"
        if os.path.exists(test_pdf_path):
            with open(test_pdf_path, 'rb') as pdf:
                for fmt in ['txt', 'json']:
                    response = self.client.post(
                        '/uploader',
                        data={
                            'file': (pdf, 'test.pdf'),
                            'format': fmt
                        },
                        content_type='multipart/form-data'
                    )
                    self.assertEqual(response.status_code, 200)

    def test_language_detection(self):
        # Test language detection for supported languages
        test_texts = {
            'en': 'This is English text.',
            'ar': 'هذا نص باللغة العربية',
            'he': 'זהו טקסט בעברית',
            'fa': 'این متن فارسی است',
            'ur': 'یہ اردو متن ہے'
        }
        
        for lang, text in test_texts.items():
            result = self.lang_checker.detect_language(text)
            self.assertEqual(result['language'], lang)

if __name__ == '__main__':
    unittest.main()