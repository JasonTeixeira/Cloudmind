# Production-ready multi-stage Dockerfile for CloudMind

ARG PY_BASE="python:3.11-slim"
FROM ${PY_BASE} AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install build dependencies only in builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application source
COPY . .


FROM ${PY_BASE} AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install only runtime OS dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy prebuilt virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user and set ownership
RUN adduser --disabled-password --gecos '' --uid 10001 cloudmind \
    && chown -R cloudmind:cloudmind /app

# Copy source code (after user creation to chown correctly if needed)
COPY --chown=cloudmind:cloudmind . .

USER 10001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run the application (gunicorn for production; dev may override with compose)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60"]