#!/bin/bash
set -e

APP_PORT=${APP_PORT:-3000}
BACKEND_PORT=8000

# Start backend
echo "Starting backend on port $BACKEND_PORT..."
cd "$(dirname "$0")/backend"
uv run uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &
BACKEND_PID=$!
cd - > /dev/null

# Serve static frontend from out/
echo "Starting frontend on port $APP_PORT..."
cd "$(dirname "$0")"
bunx serve out -l $APP_PORT &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID (port $BACKEND_PORT)"
echo "Frontend PID: $FRONTEND_PID (port $APP_PORT)"

# Wait for either process to exit
wait $BACKEND_PID $FRONTEND_PID
