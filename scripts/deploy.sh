#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Required vars
: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT}"
: "${GOOGLE_CLOUD_REGION:?Set GOOGLE_CLOUD_REGION}"

# Optional: overrides the default model in app/agent.py without a redeploy
GEMINI_MODEL="${GEMINI_MODEL:-}"

echo "Deploying Heimdall to Cloud Run..."
echo "  Project: $GOOGLE_CLOUD_PROJECT"
echo "  Region:  $GOOGLE_CLOUD_REGION"
echo "  Model:   ${GEMINI_MODEL:-<default in app/agent.py>}"

ENV_VARS="GOOGLE_GENAI_USE_VERTEXAI=true"
if [ -n "$GEMINI_MODEL" ]; then
  ENV_VARS="$ENV_VARS,GEMINI_MODEL=$GEMINI_MODEL"
fi

adk deploy cloud_run \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="$GOOGLE_CLOUD_REGION" \
  --service_name=heimdall \
  --with_ui \
  app \
  -- \
  --allow-unauthenticated \
  --set-env-vars="$ENV_VARS"

echo "Deploy complete."
