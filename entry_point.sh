#!/bin/sh
set -e
echo "Running migrations"
migrate -verbose -database $POSTGRESQL_URL -path migrations up;

echo "Starting server"
uvicorn app:app --host 0.0.0.0 --port 8000