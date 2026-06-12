#!/bin/bash
set -e

APP_PORT=${APP_PORT:-3040}
BACKEND_PORT=$((${APP_PORT:-3040} + 100))

if [ -f /usr/local/lib/workshop-devguard.sh ]; then
    source /usrj/local/lib/workshop-devguard.sh
    devguard_acquire "$APP_PORT" "$BACKEND_PORT"
fi

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Start backend
echo "Starting backend on port $BACKEND_PORT..."
cd "$ROOT_DIR/backend"
UV_BIN="${HOME}/.local/bin/uv"
"$UV_BIN" run uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &
BACKEND_PID=$!
cd "$ROOT_DIR"

# Serve the pre-built Next.js static export
echo "Serving frontend on port $APP_PORT..."
python3 -m http.server $APP_PORT --directory "$ROOT_DIR/out" &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

wait
