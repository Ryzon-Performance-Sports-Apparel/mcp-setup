"""Tests for get_asset tool."""

import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_get import get_asset
from tests.conftest import make_mock_blob


@pytest.mark.asyncio
async def test_get_asset_found():
    blob = make_mock_blob(name="campaigns/summer/abc_hero.png")

    with patch("dam_mcp.core.tools_get.get_blob", return_value=blob):
        result = await get_asset("campaigns/summer/abc_hero.png")
        data = json.loads(result)
        assert data["asset_id"] == "campaigns/summer/abc_hero.png"
        assert data["content_type"] == "image/png"
        assert "hero" in data["tags"]


@pytest.mark.asyncio
async def test_get_asset_not_found():
    with patch("dam_mcp.core.tools_get.get_blob", return_value=None):
        result = await get_asset("nonexistent.png")
        data = json.loads(result)
        assert "error" in data
        assert "not found" in data["error"].lower()


@pytest.mark.asyncio
async def test_get_asset_config_error(mock_config):
    mock_config.gcp_project_id = ""
    mock_config.gcs_bucket_name = ""
    result = await get_asset("test.png")
    data = json.loads(result)
    assert "error" in data
    assert "GCP_PROJECT_ID" in data["error"]
