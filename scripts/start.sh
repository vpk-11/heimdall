#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Ensure the heimdall conda env is active (has correct google-adk + mcp deps)
if [ "${CONDA_DEFAULT_ENV:-}" != "heimdall" ]; then
  CONDA_BASE="$(conda info --base 2>/dev/null || true)"
  if [ -n "$CONDA_BASE" ] && [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
    # shellcheck disable=SC1091
    source "$CONDA_BASE/etc/profile.d/conda.sh"
    conda activate heimdall
  else
    echo "ERROR: 'heimdall' conda env not active and conda not found to activate it."
    echo "Run: conda activate heimdall"
    exit 1
  fi
fi

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
