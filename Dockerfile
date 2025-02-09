# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a directory for the database
RUN mkdir -p /app/data

# Generate a secure secret key if not provided
RUN python3 -c "import secrets; import os; open('.env', 'a').write(f'SECRET_KEY={secrets.token_hex(32)}\n')"

# Prepare the .env file with default settings
RUN echo "ALGORITHM=HS256" >> .env && \
    echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env && \
    echo "DATABASE_URL=sqlite+aiosqlite:////app/data/auth.db" >> .env && \
    echo "HOST=0.0.0.0" >> .env && \
    echo "PORT=8000" >> .env && \
    echo "DEBUG=False" >> .env

# Expose the port the app runs on
EXPOSE 8000

# Run database migrations
RUN alembic upgrade head

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 