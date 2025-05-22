FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY blinkit_watcher.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["python", "blinkit_watcher.py"] 