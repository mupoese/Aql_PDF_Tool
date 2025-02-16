FROM python:3.11-slim

# Install system dependencies and language packs
RUN apt-get update && apt-get install -y \
    hunspell \
    hunspell-en-us \
    hunspell-ar \
    libhunspell-dev \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-ara \
    tesseract-ocr-heb \
    tesseract-ocr-fas \
    tesseract-ocr-urd \
    tesseract-ocr-eng \
    # Additional Arabic dialect support
    tesseract-ocr-ara-ext \
    # Support for Arabic script
    fonts-arabeyes \
    fonts-hosny-amiri \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create input and output directories
RUN mkdir -p input output

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000 \
    FLASK_DEBUG=False \
    PROCESS_TIMESTAMP=""

EXPOSE 5000

CMD ["python", "-m", "app.main"]