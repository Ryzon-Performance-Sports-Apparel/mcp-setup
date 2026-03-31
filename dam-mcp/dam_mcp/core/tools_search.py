"""search_assets tool — search assets by metadata."""

import json
from typing import Optional

from .config import config
from .gcs import search_blobs
from .server import mcp_server


@mcp_server.tool()
async def search_assets(
    query: str = "",
    tags: Optional[list[str]] = None,
    format: Optional[str] = None,
    campaign: Optional[str] = None,
    min_width: Optional[int] = None,
    min_height: Optional[int] = None,
    limit: int = 50,
) -> str:
    """Search creative assets by name, tags, format, campaign, or dimensions.

    Args:
        query: Free-text search across asset name, tags, and campaign
        tags: Filter by tags (all must match)
        format: Filter by file format (e.g. "png", "jpg", "mp4")
        campaign: Filter by campaign name
        min_width: Minimum width in pixels
        min_height: Minimum height in pixels
        limit: Maximum results to return (default: 50)
    """
    error = config.validate()
    if error:
        return json.dumps({"error": error}, indent=2)

    results = search_blobs(
        query=query,
        tags=tags,
        format=format,
        campaign=campaign,
        min_width=min_width,
        min_height=min_height,
        limit=limit,
    )

    return json.dumps({"assets": results, "count": len(results)}, indent=2)
