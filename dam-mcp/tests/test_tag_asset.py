"""Tests for tag_asset tool."""

import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_tag import tag_asset
from tests.conftest import make_mock_blob


@pytest.mark.asyncio
async def test_tag_asset_updates_tags():
    blob = make_mock_blob()

    with patch("dam_mcp.core.tools_tag.get_blob", return_value=blob), \
         patch("dam_mcp.core.tools_tag.set_blob_metadata") as mock_set:
        result = await tag_asset("test-asset/abc123_hero.png", tags=["hero", "approved"])
        data = json.loads(result)
        assert data["success"] is True

        mock_set.assert_called_once()
        meta_update = mock_set.call_args[0][1]
        assert meta_update["dam_tags"] == "hero,approved"


@pytest.mark.asyncio
async def test_tag_asset_updates_campaign():
    blob = make_mock_blob()

    with patch("dam_mcp.core.tools_tag.get_blob", return_value=blob), \
         patch("dam_mcp.core.tools_tag.set_blob_metadata"):
        result = await tag_asset("test-asset/abc123_hero.png", campaign="winter-2026")
        data = json.loads(result)
        assert data["success"] is True


@pytest.mark.asyncio
async def test_tag_asset_not_found():
    with patch("dam_mcp.core.tools_tag.get_blob", return_value=None):
        result = await tag_asset("nonexistent.png", tags=["test"])
        data = json.loads(result)
        assert "error" in data


@pytest.mark.asyncio
async def test_tag_asset_no_updates():
    blob = make_mock_blob()

    with patch("dam_mcp.core.tools_tag.get_blob", return_value=blob):
        result = await tag_asset("test-asset/abc123_hero.png")
        data = json.loads(result)
        assert "error" in data
        assert "no updates" in data["error"].lower()
