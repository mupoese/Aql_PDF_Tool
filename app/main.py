import os
from flask import Flask, request, render_template
from app.ocr import pdf_to_images, ocr_image
from app.utils import check_folders
import json

app = Flask(__name__)
check_folders()

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if 'file' in request.files and 'format' in request.form:
        file = request.files['file']
        output_format = request.form['format']
        
        # Validate file extension
        if not file.filename.lower().endswith('.pdf'):
            return 'Only PDF files are allowed.'
            
        file_path = os.path.join('input', file.filename)
        file.save(file_path)
        try:
            process_pdf(file_path, output_format)
            return f"File {file.filename} processed and saved as {output_format}."
        except Exception as e:
            return f"Error processing file: {str(e)}"
    return 'No file uploaded or format not selected.'

def process_pdf(file_path, output_format):
    images = pdf_to_images(file_path)
    text_output = ""
    for img in images:
        text_output += ocr_image(img)

    base_name = os.path.splitext(os.path.basename(file_path))[0]

    if output_format == 'txt':
        output_path = os.path.join('output', f"{base_name}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_output)

    elif output_format == 'json':
        output_path = os.path.join('output', f"{base_name}.json")
        json_output = {
            "input_file": file_path,
            "output_text": text_output,
            "metadata": {
                "pages_processed": len(images),
                "tool": "OCR PDF Tool",
                "format": "JSON for LLM training",
                "timestamp": os.environ.get('PROCESS_TIMESTAMP', '')
            }
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # For Docker deployment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)