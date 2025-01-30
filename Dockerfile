# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn requests semantic_version

# Expose FastAPI's default port
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]