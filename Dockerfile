
# Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Create a non-root user
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

# Application port
EXPOSE 5000

# Start application using Gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "app:create_app()"]

