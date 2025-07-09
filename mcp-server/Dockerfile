# MCP Server Dockerfile
FROM python:3.13-slim as base

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user early
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Install system dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files first (for better layer caching)
COPY --chown=app:app pyproject.toml uv.lock ./

# Install dependencies as root, then change ownership
RUN uv sync --frozen --no-dev && \
    chown -R app:app /app/.venv

# Copy MCP server source code
COPY --chown=app:app mcp-server/. ./

# Switch to non-root user
USER app

# Expose port (will be overridden by docker-compose)
EXPOSE 8000

# Default command (will be overridden by docker-compose)
CMD ["uv", "run", "fastmcp", "run", "-t", "http", "-p", "8000", "./main.py"]
