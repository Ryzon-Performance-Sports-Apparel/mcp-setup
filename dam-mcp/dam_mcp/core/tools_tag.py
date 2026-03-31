"""tag_asset tool — update metadata/tags on assets."""

import json
from typing import Optional

from .config import config
from .gcs import DAM_META_PREFIX, blob_to_metadata_dict, get_blob, set_blob_metadata
from .server import mcp_server


@mcp_server.tool()
async def tag_asset(
    asset_id: str,
    tags: Optional[list[str]] = None,
    campaign: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> str:
    """Add or update metadata tags on an asset.

    Args:
        asset_id: The asset ID (GCS object path)
        tags: New list of tags (replaces existing tags)
        campaign: Campaign name to associate
        metadata: Additional custom key-value metadata to set
    """
    error = config.validate()
    if error:
        return json.dumps({"error": error}, indent=2)

    blob = get_blob(asset_id)
    if blob is None:
        return json.dumps({"error": f"Asset not found: {asset_id}"}, indent=2)

    updates = {}
    if tags is not None:
        updates[f"{DAM_META_PREFIX}tags"] = ",".join(tags)
    if campaign is not None:
        updates[f"{DAM_META_PREFIX}campaign"] = campaign
    if metadata:
        for k, v in metadata.items():
            updates[f"{DAM_META_PREFIX}{k}"] = v

    if not updates:
        return json.dumps({"error": "No updates provided"}, indent=2)

    set_blob_metadata(asset_id, updates)
    blob = get_blob(asset_id)

    return json.dumps(
        {
            "success": True,
            "asset": blob_to_metadata_dict(blob),
        },
        indent=2,
    )
