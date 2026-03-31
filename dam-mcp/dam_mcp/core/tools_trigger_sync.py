"""trigger_sync tool — on-demand Drive-to-GCS sync."""

import json
from typing import Optional

from .config import config
from .drive_sync import sync_drive_to_gcs
from .server import mcp_server


@mcp_server.tool()
async def trigger_sync(folder_id: Optional[str] = None) -> str:
    """Trigger a Google Drive to GCS sync immediately.

    Syncs all new files from the configured Drive folder to the GCS bucket.
    Files already synced (tracked by Drive file ID) are skipped.

    Args:
        folder_id: Google Drive folder ID to sync from. Uses GDRIVE_FOLDER_ID env var if not provided.
    """
    error = config.validate()
    if error:
        return json.dumps({"error": error}, indent=2)

    target_folder = folder_id or config.gdrive_folder_id
    if not target_folder:
        return json.dumps(
            {"error": "No folder ID provided. Set GDRIVE_FOLDER_ID or pass folder_id parameter."},
            indent=2,
        )

    result = sync_drive_to_gcs(target_folder)
    return json.dumps(result, indent=2)
