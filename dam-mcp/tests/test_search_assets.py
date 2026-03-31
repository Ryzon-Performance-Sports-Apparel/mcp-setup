"""Tests for search_assets tool."""

import json
import pytest
from unittest.mock import patch

from dam_mcp.core.tools_search import search_assets


@pytest.mark.asyncio
async def test_search_returns_results():
    mock_results = [
        {
            "asset_id": "abc_hero.png",
            "name": "hero.png",
            "content_type": "image/png",
            "tags": ["hero", "summer"],
            "campaign": "summer-2026",
        }
    ]

    with patch("dam_mcp.core.tools_search.search_blobs", return_value=mock_results):
        result = await search_assets(query="hero")
        data = json.loads(result)
        assert data["count"] == 1
        assert data["assets"][0]["name"] == "hero.png"


@pytest.mark.asyncio
async def test_search_empty_results():
    with patch("dam_mcp.core.tools_search.search_blobs", return_value=[]):
        result = await search_assets(query="nonexistent")
        data = json.loads(result)
        assert data["count"] == 0
        assert data["assets"] == []


@pytest.mark.asyncio
async def test_search_with_filters():
    with patch("dam_mcp.core.tools_search.search_blobs", return_value=[]) as mock_search:
        await search_assets(
            tags=["hero"],
            format="png",
            campaign="summer-2026",
            min_width=1080,
        )
        mock_search.assert_called_once_with(
            query="",
            tags=["hero"],
            format="png",
            campaign="summer-2026",
            min_width=1080,
            min_height=None,
            limit=50,
        )
