# Base image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ ./app
COPY worker/ ./worker

# Set environment variables defaults (override in ECS)
ENV PYTHONUNBUFFERED=1

# Command to start the worker
CMD ["python", "-m", "worker.main"]
