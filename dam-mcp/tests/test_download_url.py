"""Tests for get_asset_download_url tool."""

import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_download_url import get_asset_download_url
from tests.conftest import make_mock_blob


@pytest.mark.asyncio
async def test_download_url_success():
    blob = make_mock_blob()

    with patch("dam_mcp.core.tools_download_url.get_blob", return_value=blob), \
         patch("dam_mcp.core.tools_download_url.generate_signed_url", return_value="https://storage.googleapis.com/signed"):
        result = await get_asset_download_url("test-asset/abc123_hero.png")
        data = json.loads(result)
        assert data["url"] == "https://storage.googleapis.com/signed"
        assert data["asset_id"] == "test-asset/abc123_hero.png"
        assert data["content_type"] == "image/png"
        assert data["size_bytes"] == 1024
        assert "expires_at" in data


@pytest.mark.asyncio
async def test_download_url_not_found():
    with patch("dam_mcp.core.tools_download_url.get_blob", return_value=None):
        result = await get_asset_download_url("nonexistent.png")
        data = json.loads(result)
        assert "error" in data
