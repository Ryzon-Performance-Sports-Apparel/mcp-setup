"""Shared test fixtures for DAM MCP tests."""

import datetime
import os
import pytest
from unittest.mock import MagicMock, patch


def make_mock_blob(
    name="test-asset/abc123_hero.png",
    content_type="image/png",
    size=1024,
    metadata=None,
    updated=None,
):
    """Create a mock GCS blob with configurable metadata."""
    blob = MagicMock()
    blob.name = name
    blob.content_type = content_type
    blob.size = size
    blob.updated = updated or datetime.datetime(2026, 3, 31, 12, 0, 0, tzinfo=datetime.timezone.utc)
    blob.metadata = metadata or {
        "dam_original_filename": name.split("/")[-1].split("_", 1)[-1] if "_" in name.split("/")[-1] else name.split("/")[-1],
        "dam_tags": "hero,summer",
        "dam_campaign": "summer-2026",
        "dam_width": "1080",
        "dam_height": "1080",
        "dam_upload_source": "direct",
        "dam_created_at": "2026-03-31T12:00:00+00:00",
    }
    blob.reload = MagicMock()
    blob.exists = MagicMock(return_value=True)
    blob.patch = MagicMock()
    blob.upload_from_string = MagicMock()
    blob.generate_signed_url = MagicMock(
        return_value="https://storage.googleapis.com/signed-url-mock"
    )
    return blob


@pytest.fixture(autouse=True)
def mock_config():
    """Set env vars so DamConfig.validate() passes in all tests."""
    from dam_mcp.core.config import config

    old_project = config.gcp_project_id
    old_bucket = config.gcs_bucket_name
    config.gcp_project_id = "test-project"
    config.gcs_bucket_name = "test-bucket"
    config.signed_url_expiry_minutes = 60
    yield config
    config.gcp_project_id = old_project
    config.gcs_bucket_name = old_bucket


@pytest.fixture
def sample_blob():
    """A single mock blob for unit tests."""
    return make_mock_blob()
