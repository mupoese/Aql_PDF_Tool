# Use Python 3.11 slim as base image
FROM python:3.11-slim

# ... (previous labels and ENV settings remain the same) ...

# Install system dependencies and language packs
RUN apt-get update && apt-get install -y --no-install-recommends \
    hunspell \
    hunspell-en-us \
    hunspell-ar \
    libhunspell-dev \
    python3-dev \
    build-essential \
    pkg-config \
    tesseract-ocr \
    tesseract-ocr-ara \
    tesseract-ocr-heb \
    tesseract-ocr-fas \
    tesseract-ocr-urd \
    tesseract-ocr-eng \
    tesseract-ocr-ara-ext \
    fonts-arabeyes \
    fonts-hosny-amiri \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ... (user creation and directory setup remain the same) ...

# Install Python dependencies
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir cython==3.0.12 && \
    pip install --no-cache-dir cyhunspell==1.3.4 && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# ... (rest of the Dockerfile remains the same) ...