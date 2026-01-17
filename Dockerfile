# Use a lightweight Python base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable live logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED True

# Set the working directory
WORKDIR /app

# Install system-level dependencies for C-based AI libraries
RUN apt-get update && apt-get install -y --no-install-recommends 
    build-essential 
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Using --no-cache-dir keeps the final image size small
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy models and application code
COPY . ./

# Run the web service using Gunicorn.
# We use 1 worker and 8 threads to manage memory for AI models.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
