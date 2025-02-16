# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set build arguments for version labels
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Add metadata labels
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="Aql PDF Tool" \
      org.label-schema.description="Multilingual PDF Processing Tool" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0" \
      maintainer="mupoese"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000 \
    FLASK_DEBUG=False \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Install system dependencies and language packs
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    tesseract-ocr-ara-ext \
    fonts-arabeyes \
    fonts-hosny-amiri \
    # Add security packages
    ca-certificates \
    # Add optimization packages
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p input output logs \
    && chown -R appuser:appuser /app

# Copy requirements first for better caching
COPY --chown=appuser:appuser requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Use entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120", "app.main:app"]