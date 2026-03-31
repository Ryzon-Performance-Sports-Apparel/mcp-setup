"""list_assets tool — list assets with filtering and pagination."""

import json
from typing import Optional

from .config import config
from .gcs import blob_to_metadata_dict, list_blobs
from .server import mcp_server


@mcp_server.tool()
async def list_assets(
    prefix: str = "",
    campaign: Optional[str] = None,
    format: Optional[str] = None,
    page_token: Optional[str] = None,
    page_size: int = 50,
) -> str:
    """List creative assets in the DAM with optional filtering.

    Args:
        prefix: Filter by path prefix (e.g. "campaigns/summer/" or "")
        campaign: Filter by campaign name
        format: Filter by file format (e.g. "png", "jpg", "mp4")
        page_token: Pagination token from a previous response
        page_size: Number of assets per page (default: 50)
    """
    error = config.validate()
    if error:
        return json.dumps({"error": error}, indent=2)

    blobs, next_token = list_blobs(
        prefix=prefix, max_results=page_size, page_token=page_token
    )

    assets = []
    for blob in blobs:
        blob.reload()
        meta = blob_to_metadata_dict(blob)

        if campaign and meta["campaign"].lower() != campaign.lower():
            continue
        if format:
            ct = blob.content_type or ""
            if format.lower() not in ct.lower() and not blob.name.lower().endswith(f".{format.lower()}"):
                continue

        assets.append(meta)

    result = {"assets": assets, "count": len(assets)}
    if next_token:
        result["next_page_token"] = next_token
    return json.dumps(result, indent=2)
