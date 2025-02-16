# Add FPDF2 for high-quality PDF generation
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
from app.language_utils import get_font_for_language

class MultilingualPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
        self.add_font('Amiri', '', 'fonts/Amiri-Regular.ttf', uni=True)
        
    def add_multilingual_text(self, text, language_info):
        """Add text with appropriate font and direction handling."""
        if language_info['direction'] == 'rtl':
            # Reshape Arabic text if needed
            if language_info['language'] in ['ar', 'fa', 'ur']:
                text = arabic_reshaper.reshape(text)
            text = get_display(text)
            
        font = get_font_for_language(language_info['language'])
        self.set_font(font, size=12)
        self.multi_cell(0, 10, text)
        self.ln(10)

def process_pdf(file_path: str, output_format: str) -> dict:
    """Process PDF with language support and OCR."""
    images = pdf_to_images(file_path)
    pages_results = []
    
    for page_num, img in enumerate(images, 1):
        ocr_result = ocr_image(img)
        pages_results.append({
            'page_number': page_num,
            'text': ocr_result['text'],
            'language_analysis': ocr_result.get('language_analysis', {})
        })

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Aggregate results
    output = {
        'input_file': file_path,
        'pages': pages_results,
        'metadata': {
            'pages_processed': len(images),
            'tool': 'OCR PDF Tool',
            'timestamp': datetime.utcnow().isoformat(),
            'supported_languages': lang_checker.get_supported_languages()
        }
    }

    # Save in requested format
    if output_format == 'txt':
        output_path = os.path.join('output', f"{base_name}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            for page in pages_results:
                f.write(f"=== Page {page['page_number']} ===\n")
                if page['language_analysis']:
                    f.write(f"Language: {page['language_analysis']['dominant_language']}\n\n")
                f.write(page['text'])
                f.write('\n\n')
    
    elif output_format == 'json':
        output_path = os.path.join('output', f"{base_name}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
    
    elif output_format == 'pdf':
        output_path = os.path.join('output', f"{base_name}_processed.pdf")
        pdf = MultilingualPDF()
        
        for page in pages_results:
            pdf.add_page()
            
            # Add page number
            pdf.set_font('DejaVu', size=10)
            pdf.cell(0, 10, f'Page {page["page_number"]}', ln=True, align='C')
            
            if page['language_analysis']:
                # Add language information
                pdf.set_font('DejaVu', size=10)
                pdf.cell(0, 10, 
                        f'Language: {page["language_analysis"]["dominant_language"]}', 
                        ln=True)
            
            # Add the OCR text with proper language handling
            if page['text'].strip():
                pdf.add_multilingual_text(
                    page['text'],
                    page['language_analysis']
                )
        
        pdf.output(output_path)
    
    return output