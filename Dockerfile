# Dockerfile for Secure CipherStegno Tool Web Interface
# Suitable for deployment on Docker, Railway, Render, or any container platform

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Create necessary directories
RUN mkdir -p /app/temp && \
    chmod 755 /app/temp

# Expose port
EXPOSE $PORT

# Health check - using curl which is available in the base image
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/api/health', timeout=2)"

# Run the application with gunicorn for production
CMD uvicorn src.web.api:app --host 0.0.0.0 --port $PORT --workers 2 --log-level info
