FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.2

RUN pip install poetry==${POETRY_VERSION}


WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-root

COPY ./backend ./backend

ENV TEMPLATE_DIR=/app/backend/templates

RUN chmod +x /app/backend/entrypoint.sh

ENTRYPOINT ["/app/backend/entrypoint.sh"]
