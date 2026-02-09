# Use Python 3.11 slim base image
FROM python:3.11-slim

# Install system-level dependencies needed for psycopg2-binary
# libpq-dev: PostgreSQL client library headers and static library
# gcc: C compiler needed to build psycopg2-binary on slim images
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
# This means pip install only re-runs if requirements.txt changes
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
