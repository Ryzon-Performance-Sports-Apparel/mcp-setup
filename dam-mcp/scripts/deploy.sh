#!/bin/bash
# Deploy dam-mcp to Google Cloud Run

set -e

PROJECT_ID="gold-blueprint-357814"
SERVICE_NAME="dam-mcp"
REGION="europe-west3"

# Get existing service URL (if redeploying)
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --project=$PROJECT_ID --region=$REGION --format='value(status.url)' 2>/dev/null || echo "")

# For first deploy, derive URL from existing services
if [ -z "$SERVICE_URL" ]; then
  PROJECT_HASH=$(gcloud run services list --project=$PROJECT_ID --region=$REGION --format='value(status.url)' --limit=1 2>/dev/null | sed -n 's/.*-\([a-z0-9]*\)-ew\.a\.run\.app.*/\1/p' || echo "")
  if [ -n "$PROJECT_HASH" ]; then
    SERVICE_URL="https://${SERVICE_NAME}-${PROJECT_HASH}-ew.a.run.app"
  else
    SERVICE_URL="https://${SERVICE_NAME}-k43m4vhxuq-ew.a.run.app"
  fi
fi

# OAuth credentials (read from environment or prompt)
OAUTH_CLIENT_ID="${DAM_OAUTH_CLIENT_ID:?Set DAM_OAUTH_CLIENT_ID env var}"
OAUTH_CLIENT_SECRET="${DAM_OAUTH_CLIENT_SECRET:?Set DAM_OAUTH_CLIENT_SECRET env var}"
FIGMA_PAT="${DAM_FIGMA_PAT:?Set DAM_FIGMA_PAT env var}"

# Write env vars to temp YAML file
ENV_FILE=$(mktemp /tmp/dam-mcp-env.XXXXXX.yaml)
cat > "$ENV_FILE" <<EOF
BASE_URL: '${SERVICE_URL}'
OAUTH_CLIENT_ID: '${OAUTH_CLIENT_ID}'
OAUTH_CLIENT_SECRET: '${OAUTH_CLIENT_SECRET}'
OAUTH_ALLOWED_DOMAIN: 'ryzon.net'
GCP_PROJECT_ID: '${PROJECT_ID}'
GCS_BUCKET_NAME: 'ryzon-dam'
GDRIVE_FOLDER_ID: '1SPknjndspaBH3-HWSdAomM9_HjEuSzM3'
SIGNED_URL_EXPIRY_MINUTES: '60'
FIGMA_PAT: '${FIGMA_PAT}'
EOF

echo "Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --project=$PROJECT_ID \
  --region=$REGION \
  --source=. \
  --env-vars-file="$ENV_FILE" \
  --allow-unauthenticated \
  --memory=256Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=1 \
  --timeout=300 \
  --service-account=dam-mcp@${PROJECT_ID}.iam.gserviceaccount.com

rm -f "$ENV_FILE"

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --project=$PROJECT_ID --region=$REGION --format='value(status.url)')

echo ""
echo "========================================="
echo "Deployed! Service URL: $SERVICE_URL"
echo "========================================="
echo ""
echo "For claude.ai — Add as remote MCP server:"
echo "  Server URL: ${SERVICE_URL}/mcp"
echo ""
echo "For Claude Desktop / Claude Code — add to MCP config:"
cat <<JSONEOF

{
  "mcpServers": {
    "dam": {
      "type": "url",
      "url": "${SERVICE_URL}/mcp"
    }
  }
}

JSONEOF
echo "Access restricted to @ryzon.net Google accounts."
