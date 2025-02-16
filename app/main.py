import os
from flask import Flask, request, render_template
from app.ocr import pdf_to_images, ocr_image
from app.utils import check_folders

app = Flask(__name__)
check_folders()

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if 'file' in request.files:
        file = request.files['file']
        file_path = os.path.join('input', file.filename)
        file.save(file_path)
        process_pdf(file_path)
        return f"File {file.filename} processed and saved in output folder."
    return 'No file uploaded'

def process_pdf(file_path):
    images = pdf_to_images(file_path)
    text_output = ""
    for img in images:
        text_output += ocr_image(img)
    output_path = os.path.join('output', os.path.basename(file_path) + '.txt')
    with open(output_path, 'w') as f:
        f.write(text_output)

@app.route('/process_all')
def process_all_files():
    input_dir = 'input'
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(input_dir, file_name)
            process_pdf(file_path)
    return 'All files in the input folder have been processed.'

if __name__ == '__main__':
    app.run(debug=True)