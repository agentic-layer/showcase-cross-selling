FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Accept AGENT_NAME as build arg (required)
ARG AGENT_NAME
RUN test -n "$AGENT_NAME" || (echo "AGENT_NAME build arg is required" && false)
ENV AGENT_NAME_ENV=${AGENT_NAME}

# Copy workspace configuration files for dependency resolution
COPY uv.lock pyproject.toml ./

# Copy source code after dependency installation
COPY agents/base ./agents/base
COPY agents/${AGENT_NAME_ENV} ./agents/${AGENT_NAME_ENV}

# Install the project
RUN uv sync --frozen --package ${AGENT_NAME_ENV}

# Expose port
# A2A
EXPOSE 8000
# ADK Web
EXPOSE 8001

# Run the specified agent
CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8001", "agents/insurance_host_agent/src"]