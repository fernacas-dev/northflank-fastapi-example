#!/bin/sh

# Ensure migrations are run (if any)
# python -m alembic upgrade head

# Start application with Gunicorn (production)
if [ "$ENVIRONMENT" = "production" ]; then
    exec gunicorn -k uvicorn.workers.UvicornWorker \
                 --bind 0.0.0.0:$PORT \
                 --workers 4 \
                 --worker-connections 1000 \
                 --timeout 120 \
                 --keep-alive 5 \
                 --access-logfile - \
                 --error-logfile - \
                 main:app
else
    # Development mode
    exec uvicorn main:app --host 0.0.0.0 --port $PORT --reload
fi
