"""Tests for search_knowledge_base_semantic MCP tool."""

import json
import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from dam_mcp.core.tools_semantic_search import search_knowledge_base_semantic


@pytest.mark.asyncio
async def test_semantic_search_returns_results():
    mock_docs = [
        {
            "id": "doc1",
            "type": "meeting_note",
            "title": "Sprint Planning",
            "content": "We planned the sprint.",
            "tags": ["sprint"],
            "created_at": datetime(2026, 4, 7, tzinfo=timezone.utc),
        }
    ]
    mock_voyage = MagicMock()
    mock_result = MagicMock()
    mock_result.embeddings = [[0.1] * 1024]
    mock_voyage.embed.return_value = mock_result

    with patch("dam_mcp.core.tools_semantic_search._get_voyage_client", return_value=mock_voyage), \
         patch("dam_mcp.core.tools_semantic_search.vector_search", return_value=mock_docs):
        result = await search_knowledge_base_semantic(query="sprint planning")
        data = json.loads(result)
        assert data["count"] == 1
        assert data["documents"][0]["title"] == "Sprint Planning"
        assert "content_preview" in data["documents"][0]


@pytest.mark.asyncio
async def test_semantic_search_with_type_filter():
    mock_voyage = MagicMock()
    mock_result = MagicMock()
    mock_result.embeddings = [[0.1] * 1024]
    mock_voyage.embed.return_value = mock_result

    with patch("dam_mcp.core.tools_semantic_search._get_voyage_client", return_value=mock_voyage), \
         patch("dam_mcp.core.tools_semantic_search.vector_search", return_value=[]) as mock_vs:
        result = await search_knowledge_base_semantic(query="test", type="meeting_note")
        mock_vs.assert_called_once()
        call_kwargs = mock_vs.call_args[1]
        assert call_kwargs["doc_type"] == "meeting_note"


@pytest.mark.asyncio
async def test_semantic_search_no_api_key():
    with patch("dam_mcp.core.tools_semantic_search._get_voyage_client", return_value=None):
        result = await search_knowledge_base_semantic(query="test")
        data = json.loads(result)
        assert "error" in data
        assert "VOYAGE_API_KEY" in data["error"]


@pytest.mark.asyncio
async def test_semantic_search_config_error(mock_config):
    mock_config.gcp_project_id = ""
    mock_config.gcs_bucket_name = ""
    result = await search_knowledge_base_semantic(query="test")
    data = json.loads(result)
    assert "error" in data
