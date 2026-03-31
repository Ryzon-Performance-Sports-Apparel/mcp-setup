"""Tests for list_assets tool."""

import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_list import list_assets
from tests.conftest import make_mock_blob


@pytest.mark.asyncio
async def test_list_assets_returns_results():
    blob = make_mock_blob()

    with patch("dam_mcp.core.tools_list.list_blobs", return_value=([blob], None)):
        result = await list_assets()
        data = json.loads(result)
        assert "assets" in data
        assert data["count"] == 1
        assert data["assets"][0]["content_type"] == "image/png"


@pytest.mark.asyncio
async def test_list_assets_empty():
    with patch("dam_mcp.core.tools_list.list_blobs", return_value=([], None)):
        result = await list_assets()
        data = json.loads(result)
        assert data["count"] == 0
        assert data["assets"] == []


@pytest.mark.asyncio
async def test_list_assets_with_pagination_token():
    blob = make_mock_blob()

    with patch("dam_mcp.core.tools_list.list_blobs", return_value=([blob], "next-page-token")):
        result = await list_assets()
        data = json.loads(result)
        assert data["next_page_token"] == "next-page-token"


@pytest.mark.asyncio
async def test_list_assets_filters_by_campaign():
    blob = make_mock_blob()

    with patch("dam_mcp.core.tools_list.list_blobs", return_value=([blob], None)):
        result = await list_assets(campaign="summer-2026")
        data = json.loads(result)
        assert data["count"] == 1

        result = await list_assets(campaign="winter-2026")
        data = json.loads(result)
        assert data["count"] == 0
