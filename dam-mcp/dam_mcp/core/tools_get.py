"""get_asset tool — get full metadata for a single asset."""

import json

from .config import config
from .gcs import blob_to_metadata_dict, get_blob
from .server import mcp_server


@mcp_server.tool()
async def get_asset(asset_id: str) -> str:
    """Get full metadata for a specific asset by its ID.

    Args:
        asset_id: The asset ID (GCS object path, e.g. "campaigns/summer/hero-1080x1080.png")
    """
    error = config.validate()
    if error:
        return json.dumps({"error": error}, indent=2)

    blob = get_blob(asset_id)
    if blob is None:
        return json.dumps({"error": f"Asset not found: {asset_id}"}, indent=2)

    return json.dumps(blob_to_metadata_dict(blob), indent=2)
