# =========================
# Builder stage
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create virtualenv + install deps
RUN uv sync --frozen --no-dev

# =========================
# Runtime stage
# =========================
FROM python:3.11-slim

WORKDIR /app

# Create non-root user (security)
RUN useradd -m appuser
USER appuser

# Copy venv from builder
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy app code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
