# Multi-service Dockerfile: FastAPI backend + static webapp
# Build stage for Python deps (allows caching)
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=on

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy and install python deps
COPY requirements.txt ./
COPY backend/requirements.txt ./backend-requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r backend-requirements.txt

# Copy app code
COPY backend/ ./backend/
COPY webapp/ ./webapp/

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Default environment (override in deployment)
ENV BACKEND_URL="http://localhost:8000" \
    CORS_ORIGINS="*" \
    DB_PATH="/app/backend/telegram_bot.db"

# Start FastAPI with uvicorn
CMD ["python", "-m", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
