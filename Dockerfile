FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application with multiple workers for High Availability
# 4 workers is a good default for a 2-core machine, but can be scaled
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "ikea_recommender.app.main:app", "--bind", "0.0.0.0:8000"]
