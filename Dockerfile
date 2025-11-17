# Use an official Python runtime as a parent image
# FROM python:3.11-slim

FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# === Google OAuth ===
ENV GOOGLE_CLIENT_ID="your_google_client_id_here"
ENV GOOGLE_CLIENT_SECRET="your_google_client_secret_here"

# === GitHub OAuth ===
ENV GITHUB_CLIENT_ID="your_github_client_id_here"
ENV GITHUB_CLIENT_SECRET="your_github_client_secret_here"


# Set work directory
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run the application with Gunicorn
CMD gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
