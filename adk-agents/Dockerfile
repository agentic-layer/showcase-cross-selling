FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /app

ADD ./pyproject.toml /app
ADD ./uv.lock /app
RUN uv sync --locked

COPY ./insurance_host_agent /app/insurance_host_agent/
#COPY --from=agents-folder ./insurance_host_agent /app/insurance_host_agent/

CMD ["uv", "run", "adk", "web"]
