#!/bin/sh
# Railway may still run: uvicorn ... --port '${PORT:-8001}'
exec python /app/start.py
