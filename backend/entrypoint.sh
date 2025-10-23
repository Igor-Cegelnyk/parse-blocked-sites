#!/bin/bash
set -e

echo "Run apply migrations.."
cd /app/backend
poetry run alembic upgrade head
echo "Migrations applied!"

cd /app

if [ "$1" = "celery-worker" ]; then
  exec poetry run celery -A backend.celery.celery_app worker --loglevel=info -E
elif [ "$1" = "celery-beat" ]; then
  exec poetry run celery -A backend.celery.celery_app beat --loglevel=info
elif [ "$1" = "flower" ]; then
  exec poetry run celery -A backend.celery.celery_app flower --broker=redis://redis:6379/0 --port=5555
else
  exec poetry run uvicorn backend.main:main_app --host "$APP_CONFIG__RUN__HOST" --port "$APP_CONFIG__RUN__PORT"
fi