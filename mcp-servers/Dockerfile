FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Accept MCP_SERVER_NAME as build arg (required)
ARG MCP_SERVER_NAME
RUN test -n "MCP_SERVER_NAME" || (echo "MCP_SERVER_NAME build arg is required" && false)
ENV MCP_SERVER_NAME_ENV=${MCP_SERVER_NAME}

# Copy workspace configuration files for dependency resolution
COPY uv.lock pyproject.toml ./

# Copy source code
COPY mcp-servers/${MCP_SERVER_NAME_ENV} ./mcp-servers/${MCP_SERVER_NAME_ENV}

# Install the project
RUN uv sync --frozen --package ${MCP_SERVER_NAME_ENV}

# Expose port
EXPOSE 8000

# Run the specified mcp server
CMD ["uv", "run", "--package", "${MCP_SERVER_NAME_ENV}", "${MCP_SERVER_NAME_ENV}"]