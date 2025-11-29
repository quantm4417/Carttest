FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright
RUN pip install --no-cache-dir playwright==1.40.0 && \
    playwright install chromium && \
    playwright install-deps chromium

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Create data directories
RUN mkdir -p /app/data/uploads /app/data/images

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run Flask
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

