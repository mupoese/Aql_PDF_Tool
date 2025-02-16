from flask import Flask, request, render_template
from ocr import pdf_to_images, ocr_image

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if 'file' not in request.files:
        return 'No file uploaded'
    file = request.files['file']
    images = pdf_to_images(file)
    text = ''
    for img in images:
        text += ocr_image(img)
    return text

if __name__ == '__main__':
    app.run(debug=True)
