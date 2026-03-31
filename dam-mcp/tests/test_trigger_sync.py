"""Tests for trigger_sync MCP tool."""

import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_trigger_sync import trigger_sync


@pytest.mark.asyncio
async def test_trigger_sync_success():
    sync_result = {
        "status": "completed",
        "drive_files_found": 10,
        "new_files_synced": 3,
        "skipped_existing": 7,
        "errors": [],
        "duration_seconds": 5.2,
    }

    with patch("dam_mcp.core.tools_trigger_sync.sync_drive_to_gcs", return_value=sync_result):
        result = await trigger_sync(folder_id="test_folder_123")
        data = json.loads(result)
        assert data["status"] == "completed"
        assert data["new_files_synced"] == 3


@pytest.mark.asyncio
async def test_trigger_sync_uses_config_folder_id(mock_config):
    mock_config.gdrive_folder_id = "config_folder_456"
    sync_result = {
        "status": "completed",
        "drive_files_found": 0,
        "new_files_synced": 0,
        "skipped_existing": 0,
        "errors": [],
        "duration_seconds": 0.1,
    }

    with patch("dam_mcp.core.tools_trigger_sync.sync_drive_to_gcs", return_value=sync_result) as mock_sync:
        await trigger_sync()
        mock_sync.assert_called_once_with("config_folder_456")


@pytest.mark.asyncio
async def test_trigger_sync_no_folder_id(mock_config):
    mock_config.gdrive_folder_id = ""
    result = await trigger_sync()
    data = json.loads(result)
    assert "error" in data
    assert "GDRIVE_FOLDER_ID" in data["error"]
