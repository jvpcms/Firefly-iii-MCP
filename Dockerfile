FROM python:3.12.9-slim-bookworm AS base

FROM base AS builder

RUN pip install uv
WORKDIR /app

ENV PYTHONBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON=python3.12

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .

RUN uv sync --frozen --no-dev

FROM base AS runtime
# Copy the environment, but not the source code
WORKDIR /app
COPY --from=builder /app ./
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

ENV PYTHONPATH="/app/src"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

