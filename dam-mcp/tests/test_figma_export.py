"""Tests for export_figma_frames tool."""

import json
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from dam_mcp.core.tools_figma_export import (
    export_figma_frames,
    _extract_file_key,
    _sanitize_filename,
    _find_matching_frames,
)


def test_extract_file_key_design_url():
    url = "https://www.figma.com/design/meJ8eKClDGVXRUx8WWtOY0/My-File"
    assert _extract_file_key(url) == "meJ8eKClDGVXRUx8WWtOY0"


def test_extract_file_key_file_url():
    url = "https://www.figma.com/file/ABC123/My-File"
    assert _extract_file_key(url) == "ABC123"


def test_extract_file_key_invalid():
    assert _extract_file_key("https://example.com") is None


def test_sanitize_filename():
    assert _sanitize_filename("Hero Banner 1") == "Hero_Banner_1"
    assert _sanitize_filename("test/frame:2") == "test_frame_2"


def test_find_matching_frames_exact():
    node = {
        "name": "Page",
        "type": "CANVAS",
        "children": [
            {"id": "1:1", "name": "Hero_1", "type": "FRAME", "children": []},
            {"id": "1:2", "name": "Hero_2", "type": "FRAME", "children": []},
            {"id": "1:3", "name": "Footer", "type": "FRAME", "children": []},
        ],
    }
    results = []
    _find_matching_frames(node, "Hero_1", results)
    assert len(results) == 1
    assert results[0]["id"] == "1:1"


def test_find_matching_frames_glob():
    node = {
        "name": "Page",
        "type": "CANVAS",
        "children": [
            {"id": "1:1", "name": "Hero_1", "type": "FRAME", "children": []},
            {"id": "1:2", "name": "Hero_2", "type": "FRAME", "children": []},
            {"id": "1:3", "name": "Footer", "type": "FRAME", "children": []},
        ],
    }
    results = []
    _find_matching_frames(node, "Hero_*", results)
    assert len(results) == 2


@pytest.mark.asyncio
async def test_export_no_figma_token(mock_config):
    with patch.dict("os.environ", {}, clear=False), \
         patch("dam_mcp.core.tools_figma_export._get_figma_token", return_value=None):
        result = await export_figma_frames(
            figma_url="https://www.figma.com/design/ABC123/File",
            frame_names="Hero_1",
        )
        data = json.loads(result)
        assert "error" in data
        assert "FIGMA_PAT" in data["error"]


@pytest.mark.asyncio
async def test_export_invalid_url(mock_config):
    with patch("dam_mcp.core.tools_figma_export._get_figma_token", return_value="fake-token"):
        result = await export_figma_frames(
            figma_url="https://example.com/not-figma",
            frame_names="Hero_1",
        )
        data = json.loads(result)
        assert "error" in data
        assert "file key" in data["error"].lower()


@pytest.mark.asyncio
async def test_export_success(mock_config):
    file_data = {
        "document": {
            "name": "Doc",
            "type": "DOCUMENT",
            "children": [{
                "name": "Page",
                "type": "CANVAS",
                "children": [
                    {"id": "1:1", "name": "Hero_1", "type": "FRAME", "children": []},
                ],
            }],
        }
    }
    export_data = {"images": {"1:1": "https://figma-cdn.example.com/img.png"}}
    image_bytes = b"fake-png-data"

    mock_blob = MagicMock()
    mock_blob.reload = MagicMock()

    with patch("dam_mcp.core.tools_figma_export._get_figma_token", return_value="fake-token"), \
         patch("dam_mcp.core.tools_figma_export._figma_get", new_callable=AsyncMock) as mock_figma, \
         patch("dam_mcp.core.tools_figma_export.upload_blob", return_value=mock_blob) as mock_upload:

        mock_figma.side_effect = [file_data, export_data]

        # Mock the image download
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = image_bytes
            mock_resp.raise_for_status = MagicMock()
            mock_get.return_value = mock_resp

            result = await export_figma_frames(
                figma_url="https://www.figma.com/design/ABC123/File",
                frame_names="Hero_1",
                campaign="summer-2026",
                tags=["hero", "figma"],
            )
            data = json.loads(result)
            assert data["status"] == "completed"
            assert data["frames_exported"] == 1
            assert data["exported"][0]["frame_name"] == "Hero_1"
            mock_upload.assert_called_once()
