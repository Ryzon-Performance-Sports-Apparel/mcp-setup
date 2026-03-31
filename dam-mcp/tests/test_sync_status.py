"""Tests for sync_status MCP tool."""

import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_sync import sync_status


@pytest.mark.asyncio
async def test_sync_status_with_state():
    state = {
        "last_sync_at": "2026-03-31T14:00:00+00:00",
        "last_sync_result": "completed",
        "files_synced": 5,
        "total_drive_files": 42,
        "errors": [],
    }

    with patch("dam_mcp.core.tools_sync.read_sync_state", return_value=state):
        result = await sync_status()
        data = json.loads(result)
        assert data["last_sync_at"] == "2026-03-31T14:00:00+00:00"
        assert data["files_synced"] == 5
        assert data["status"] == "completed"


@pytest.mark.asyncio
async def test_sync_status_no_state():
    with patch("dam_mcp.core.tools_sync.read_sync_state", return_value=None):
        result = await sync_status()
        data = json.loads(result)
        assert data["status"] == "never_synced"
        assert "trigger_sync" in data["message"]
