"""sync_status tool — Drive-to-GCS sync status (Phase 1 stub)."""

import json

from .server import mcp_server


@mcp_server.tool()
async def sync_status() -> str:
    """Check the status of Google Drive to GCS sync.

    Phase 1: Returns a stub indicating sync is not yet configured.
    Phase 2 will implement real-time sync monitoring via Cloud Functions.
    """
    return json.dumps(
        {
            "status": "not_configured",
            "message": (
                "Google Drive sync is not yet configured. "
                "This feature will be available in Phase 2. "
                "For now, use upload_asset to add assets directly."
            ),
        },
        indent=2,
    )
