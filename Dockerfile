# Use Python 3.11 to match CI/CD
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    hunspell \
    hunspell-en-us \
    libhunspell-dev \
    build-essential \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Create input and output directories
RUN mkdir -p input output

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000 \
    FLASK_DEBUG=False \
    PROCESS_TIMESTAMP=""

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "app.main"]