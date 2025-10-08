FROM ghcr.io/astral-sh/uv:python3.10-alpine

WORKDIR /app

ENV UV_PROJECT_ENV=.venv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
