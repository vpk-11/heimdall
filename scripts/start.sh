#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check for .env
if [ ! -f ".env" ]; then
  echo "ERROR: .env not found. Copy .env.example and fill in your keys."
  exit 1
fi

# Check for required env var
set -a
source .env
set +a

if [ -z "${GOOGLE_API_KEY:-}" ] && [ -z "${GEMINI_API_KEY:-}" ]; then
  echo "ERROR: Set GOOGLE_API_KEY or GEMINI_API_KEY in .env"
  exit 1
fi

# Determine run mode
MODE="${1:-cli}"

case "$MODE" in
  cli)
    echo "Starting Heimdall CLI..."
    python -m app.main
    ;;
  web)
    echo "Starting Heimdall in ADK web UI..."
    adk web
    ;;
  *)
    echo "Usage: $0 [cli|web]"
    echo "  cli  - interactive CLI (default)"
    echo "  web  - ADK built-in web UI for demo/testing"
    exit 1
    ;;
esac
