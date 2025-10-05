FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application files
COPY backend/ /app/backend/
COPY telegram-bot/ /app/telegram-bot/

# Create database directory
RUN mkdir -p /app/data

# Set environment variables
ENV DB_PATH=/app/data/telegram_bot.db
ENV PYTHONUNBUFFERED=1

# Initialize database
RUN cd /app/backend && python3 db.py

# Expose port
EXPOSE 8000

# Start backend
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]