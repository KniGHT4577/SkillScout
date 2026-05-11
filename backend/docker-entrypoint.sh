#!/bin/bash
set -e

echo "Applying database migrations..."
alembic upgrade head

echo "Starting Uvicorn server..."
# Use the $PORT environment variable provided by Cloud Run, default to 8080
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}"
