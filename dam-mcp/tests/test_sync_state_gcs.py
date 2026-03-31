"""Tests for GCS sync state helpers."""

import json
import pytest
from unittest.mock import MagicMock, patch

from dam_mcp.core.gcs import (
    find_blob_by_drive_id,
    read_sync_state,
    write_sync_state,
    SYNC_STATE_BLOB,
)


def test_find_blob_by_drive_id_found():
    mock_bucket = MagicMock()
    blob = MagicMock()
    blob.metadata = {"dam_drive_file_id": "drive123"}
    blob.reload = MagicMock()
    mock_bucket.list_blobs.return_value = [blob]

    with patch("dam_mcp.core.gcs.get_bucket", return_value=mock_bucket):
        result = find_blob_by_drive_id("drive123")
        assert result is blob


def test_find_blob_by_drive_id_not_found():
    mock_bucket = MagicMock()
    blob = MagicMock()
    blob.metadata = {"dam_drive_file_id": "other_id"}
    blob.reload = MagicMock()
    mock_bucket.list_blobs.return_value = [blob]

    with patch("dam_mcp.core.gcs.get_bucket", return_value=mock_bucket):
        result = find_blob_by_drive_id("drive123")
        assert result is None


def test_write_sync_state():
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    state = {"last_sync_at": "2026-03-31T14:00:00+00:00", "files_synced": 5}

    with patch("dam_mcp.core.gcs.get_bucket", return_value=mock_bucket):
        write_sync_state(state)
        mock_bucket.blob.assert_called_once_with(SYNC_STATE_BLOB)
        mock_blob.upload_from_string.assert_called_once()
        uploaded_data = mock_blob.upload_from_string.call_args[0][0]
        assert json.loads(uploaded_data)["files_synced"] == 5


def test_read_sync_state_exists():
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.exists.return_value = True
    mock_blob.download_as_text.return_value = '{"last_sync_at": "2026-03-31T14:00:00+00:00"}'
    mock_bucket.blob.return_value = mock_blob

    with patch("dam_mcp.core.gcs.get_bucket", return_value=mock_bucket):
        result = read_sync_state()
        assert result["last_sync_at"] == "2026-03-31T14:00:00+00:00"


def test_read_sync_state_not_exists():
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.exists.return_value = False
    mock_bucket.blob.return_value = mock_blob

    with patch("dam_mcp.core.gcs.get_bucket", return_value=mock_bucket):
        result = read_sync_state()
        assert result is None
