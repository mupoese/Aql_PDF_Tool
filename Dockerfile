# Use Python 3.11 to match CI/CD
FROM python:3.11-slim

# Install system dependencies for hunspell and tesseract
RUN apt-get update && apt-get install -y \
    hunspell \
    hunspell-en-us \
    libhunspell-dev \
    build-essential \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Run the application
CMD ["python", "main.py"]