"""Tests for the GCS client wrapper."""

import json
import pytest
from unittest.mock import MagicMock, patch

from dam_mcp.core.gcs import blob_to_metadata_dict


def test_blob_to_metadata_dict(sample_blob):
    """Converts a GCS blob to a standard metadata dict."""
    result = blob_to_metadata_dict(sample_blob)
    assert result["asset_id"] == sample_blob.name
    assert result["content_type"] == "image/png"
    assert result["size_bytes"] == 1024
    assert "hero" in result["tags"]
    assert "summer" in result["tags"]
    assert result["campaign"] == "summer-2026"
    assert result["width"] == 1080
    assert result["height"] == 1080


def test_blob_to_metadata_dict_empty_metadata():
    """Handles blob with no custom metadata."""
    blob = MagicMock()
    blob.name = "test.png"
    blob.content_type = "image/png"
    blob.size = 512
    blob.updated = None
    blob.metadata = {}

    result = blob_to_metadata_dict(blob)
    assert result["asset_id"] == "test.png"
    assert result["tags"] == []
    assert result["campaign"] == ""
    assert result["width"] is None
