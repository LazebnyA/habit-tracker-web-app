#!/bin/sh

# Run Alembic migrations
alembic upgrade head

# Start the application
exec uvicorn src.main:app --host localhost --port 8000