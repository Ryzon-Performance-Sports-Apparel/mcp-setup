"""upload_asset tool — upload assets to GCS."""

import json
from typing import Optional

import httpx

from .config import config
from .gcs import DAM_META_PREFIX, blob_to_metadata_dict, upload_blob
from .server import mcp_server
from .utils import (
    decode_asset_data,
    detect_content_type,
    generate_asset_id,
    logger,
    now_iso,
)


@mcp_server.tool()
async def upload_asset(
    filename: str,
    data: Optional[str] = None,
    source_url: Optional[str] = None,
    campaign: Optional[str] = None,
    tags: Optional[list[str]] = None,
    folder: str = "",
) -> str:
    """Upload a creative asset to the DAM.

    Provide either base64-encoded data or a source URL to fetch from.

    Args:
        filename: Original filename (e.g. "hero-banner.png")
        data: Base64-encoded file content (or data URL like "data:image/png;base64,...")
        source_url: Public URL to fetch the asset from (alternative to data)
        campaign: Campaign name to associate with this asset
        tags: List of tags for categorization (e.g. ["hero", "summer", "1080x1080"])
        folder: Folder path prefix in the bucket (e.g. "campaigns/summer/")
    """
    error = config.validate()
    if error:
        return json.dumps({"error": error}, indent=2)

    if not data and not source_url:
        return json.dumps(
            {"error": "Either 'data' (base64) or 'source_url' must be provided"},
            indent=2,
        )

    content_type = detect_content_type(filename)
    upload_source = "direct"

    if data:
        file_bytes, detected_ct = decode_asset_data(data)
        if detected_ct:
            content_type = detected_ct
    else:
        upload_source = "url"
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.get(source_url)
                resp.raise_for_status()
                file_bytes = resp.content
                if resp.headers.get("content-type"):
                    content_type = resp.headers["content-type"].split(";")[0].strip()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch asset from URL: {e}")
            return json.dumps(
                {"error": f"Failed to fetch asset from URL: {e}"}, indent=2
            )

    asset_id = generate_asset_id()
    folder = folder.strip("/")
    blob_name = f"{folder}/{asset_id}_{filename}" if folder else f"{asset_id}_{filename}"

    metadata = {
        f"{DAM_META_PREFIX}original_filename": filename,
        f"{DAM_META_PREFIX}upload_source": upload_source,
        f"{DAM_META_PREFIX}created_at": now_iso(),
        f"{DAM_META_PREFIX}tags": ",".join(tags) if tags else "",
        f"{DAM_META_PREFIX}campaign": campaign or "",
    }

    blob = upload_blob(blob_name, file_bytes, content_type, metadata)
    blob.reload()

    return json.dumps(
        {
            "success": True,
            "asset": blob_to_metadata_dict(blob),
        },
        indent=2,
    )
