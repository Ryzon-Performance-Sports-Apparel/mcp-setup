"""Utilities for the DAM MCP server."""

import base64
import logging
import mimetypes
import os
import pathlib
import platform
import uuid
from datetime import datetime, timezone


def _get_log_dir() -> pathlib.Path:
    if platform.system() == "Darwin":
        base = pathlib.Path.home() / "Library" / "Application Support"
    elif platform.system() == "Windows":
        base = pathlib.Path(os.environ.get("APPDATA", pathlib.Path.home()))
    else:
        base = pathlib.Path.home() / ".config"
    log_dir = base / "dam-mcp"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def _setup_logger() -> logging.Logger:
    _logger = logging.getLogger("dam_mcp")
    _logger.setLevel(logging.DEBUG)

    try:
        log_path = _get_log_dir() / "dam_mcp_debug.log"
        handler = logging.FileHandler(str(log_path), encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
    except Exception:
        pass

    return _logger


logger = _setup_logger()


def detect_content_type(filename: str) -> str:
    """Detect MIME type from filename."""
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or "application/octet-stream"


def decode_asset_data(data: str) -> tuple[bytes, str | None]:
    """Decode base64 or data URL to bytes.

    Returns (bytes, content_type_or_none).
    """
    if data.startswith("data:"):
        header, b64 = data.split(",", 1)
        content_type = header.split(";")[0].replace("data:", "")
        return base64.b64decode(b64), content_type
    return base64.b64decode(data), None


def generate_asset_id() -> str:
    """Generate a unique asset ID."""
    return uuid.uuid4().hex[:16]


def now_iso() -> str:
    """Current UTC time as ISO string."""
    return datetime.now(timezone.utc).isoformat()
