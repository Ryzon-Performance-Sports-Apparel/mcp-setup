"""
DAM MCP - Digital Asset Management MCP Server

Search, upload, tag, and serve creative assets from GCS for ad platforms.
"""

from dam_mcp.core.server import main

__version__ = "0.1.0"


def entrypoint():
    """Main entry point for the package when invoked with uvx."""
    return main()
