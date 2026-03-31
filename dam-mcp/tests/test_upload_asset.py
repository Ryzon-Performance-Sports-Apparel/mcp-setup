"""Tests for upload_asset tool."""

import base64
import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_upload import upload_asset
from tests.conftest import make_mock_blob


@pytest.mark.asyncio
async def test_upload_from_base64():
    blob = make_mock_blob(name="abc123_hero.png")

    with patch("dam_mcp.core.tools_upload.upload_blob", return_value=blob), \
         patch("dam_mcp.core.tools_upload.generate_asset_id", return_value="abc123"):
        data_b64 = base64.b64encode(b"fake-png-data").decode()
        result = await upload_asset(
            filename="hero.png",
            data=data_b64,
            campaign="summer-2026",
            tags=["hero", "banner"],
        )
        data = json.loads(result)
        assert data["success"] is True
        assert "asset" in data


@pytest.mark.asyncio
async def test_upload_from_data_url():
    blob = make_mock_blob(name="abc123_hero.png")

    with patch("dam_mcp.core.tools_upload.upload_blob", return_value=blob), \
         patch("dam_mcp.core.tools_upload.generate_asset_id", return_value="abc123"):
        data_url = "data:image/png;base64," + base64.b64encode(b"fake-png").decode()
        result = await upload_asset(filename="hero.png", data=data_url)
        data = json.loads(result)
        assert data["success"] is True


@pytest.mark.asyncio
async def test_upload_no_data_or_url():
    result = await upload_asset(filename="hero.png")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_upload_with_folder():
    blob = make_mock_blob(name="campaigns/summer/abc123_hero.png")

    with patch("dam_mcp.core.tools_upload.upload_blob", return_value=blob) as mock_upload, \
         patch("dam_mcp.core.tools_upload.generate_asset_id", return_value="abc123"):
        data_b64 = base64.b64encode(b"fake").decode()
        await upload_asset(filename="hero.png", data=data_b64, folder="campaigns/summer")
        mock_upload.assert_called_once()
        blob_name = mock_upload.call_args[0][0]
        assert blob_name == "campaigns/summer/abc123_hero.png"
