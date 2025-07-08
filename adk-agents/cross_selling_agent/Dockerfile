FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /app

ADD ./pyproject.toml /app
ADD ./uv.lock /app
RUN uv sync --locked

ADD . /app

CMD ["uv", "run", "."]
