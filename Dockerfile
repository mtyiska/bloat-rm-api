# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy only requirements first for efficient caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Ensure .env file is copied
COPY .env /app/.env

# Expose FastAPI's default port
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
