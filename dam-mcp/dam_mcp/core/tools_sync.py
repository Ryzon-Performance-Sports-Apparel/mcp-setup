"""sync_status tool — report last Drive-to-GCS sync status."""

import json

from .gcs import read_sync_state
from .server import mcp_server


@mcp_server.tool()
async def sync_status() -> str:
    """Check the status of the last Google Drive to GCS sync.

    Reports when the last sync ran, how many files were synced,
    and any errors that occurred.
    """
    state = read_sync_state()

    if state is None:
        return json.dumps(
            {
                "status": "never_synced",
                "message": "No sync has been run yet. Use trigger_sync to start one.",
            },
            indent=2,
        )

    return json.dumps(
        {
            "status": state.get("last_sync_result", "unknown"),
            "last_sync_at": state.get("last_sync_at", ""),
            "files_synced": state.get("files_synced", 0),
            "total_drive_files": state.get("total_drive_files", 0),
            "errors": state.get("errors", []),
        },
        indent=2,
    )
