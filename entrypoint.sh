#!/bin/sh
set -e


# Run DB migrations
echo "Running Flask database migrations..."
flask --app backend/app db upgrade


# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn --chdir backend -b 0.0.0.0:5000 -w 4 app:app --timeout 300 --log-level debug