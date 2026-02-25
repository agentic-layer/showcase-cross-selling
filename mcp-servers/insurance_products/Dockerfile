FROM python:3.13-slim-trixie

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /bin/uv

# Install dependencies in a separate layer for better caching
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --link-mode=copy

# Copy source code and install the project
COPY src/ ./src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --link-mode=copy

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "insurance_products"]
