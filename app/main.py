import os
from flask import Flask, request, render_template, jsonify
from app.ocr import pdf_to_images, ocr_image
from app.utils import check_folders
from app.language_check import LanguageChecker
import json
from datetime import datetime

app = Flask(__name__)
check_folders()
lang_checker = LanguageChecker()

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if 'file' in request.files and 'format' in request.form:
        file = request.files['file']
        output_format = request.form['format']
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
            
        file_path = os.path.join('input', file.filename)
        file.save(file_path)
        
        try:
            result = process_pdf(file_path, output_format)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'No file uploaded or format not selected'}), 400

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
    
    return output

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)