# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
# This means pip install only re-runs if requirements.txt changes
COPY requirements.txt .

# Install system dependencies and Python packages in one layer, then clean up
# Build dependencies (can be removed after install): libpq-dev, gcc
# Runtime dependencies (must remain): libpq5
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        libpq5 \
        gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
