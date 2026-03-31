"""get_asset_download_url tool — generate signed download URLs."""

import json
from datetime import datetime, timedelta, timezone

from .config import config
from .gcs import generate_signed_url, get_blob
from .server import mcp_server


@mcp_server.tool()
async def get_asset_download_url(
    asset_id: str,
    expiry_minutes: int = 60,
) -> str:
    """Generate a time-limited signed URL for downloading an asset.

    This is the key integration point — other MCP servers (meta-ads-mcp,
    google-ads-mcp) use the returned URL to fetch creative assets for ad creation.

    Args:
        asset_id: The asset ID (GCS object path)
        expiry_minutes: URL lifetime in minutes (default: 60)
    """
    error = config.validate()
    if error:
        return json.dumps({"error": error}, indent=2)

    blob = get_blob(asset_id)
    if blob is None:
        return json.dumps({"error": f"Asset not found: {asset_id}"}, indent=2)

    url = generate_signed_url(asset_id, expiry_minutes)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)

    return json.dumps(
        {
            "asset_id": asset_id,
            "url": url,
            "expires_at": expires_at.isoformat(),
            "content_type": blob.content_type,
            "size_bytes": blob.size,
        },
        indent=2,
    )
