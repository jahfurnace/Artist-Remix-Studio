#!/bin/bash
set -e

export APP_PORT=${APP_PORT:-3085}

cd "$(dirname "$0")/backend"

source "$HOME/.local/bin/env" 2>/dev/null || true

uv run uvicorn app.main:app --host 0.0.0.0 --port "$APP_PORT" --reload
