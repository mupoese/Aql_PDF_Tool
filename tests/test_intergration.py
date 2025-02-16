import unittest
import os
import shutil
from datetime import datetime
from app.main import app
from app.language_check import LanguageChecker
from app.ocr import pdf_to_images, ocr_image

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests."""
        # Ensure input and output directories exist
        for directory in ['input', 'output']:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Create a timestamp for file naming
        cls.timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

    def setUp(self):
        """Set up before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.test_filename = f'test_{self.timestamp}.pdf'
        self.test_filepath = os.path.join('input', self.test_filename)
        
        # Create a test PDF file if it doesn't exist
        if not os.path.exists(self.test_filepath):
            self._create_test_pdf()

    def _create_test_pdf(self):
        """Create a sample PDF file for testing."""
        # Using reportlab to create a test PDF
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(self.test_filepath, pagesize=letter)
        
        # Add multilingual text
        c.drawString(100, 750, "English Text for Testing")
        c.drawString(100, 700, "هذا نص عربي للاختبار")  # Arabic
        c.drawString(100, 650,