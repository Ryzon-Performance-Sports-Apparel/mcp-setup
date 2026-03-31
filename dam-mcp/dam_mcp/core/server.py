"""MCP server configuration for Digital Asset Management."""

import argparse
import sys

from mcp.server.fastmcp import FastMCP

from .utils import logger

mcp_server = FastMCP("dam")


def main():
    """Main entry point for the DAM MCP server."""
    logger.info("DAM MCP server starting")
    logger.debug(f"Python version: {sys.version}")
    logger.debug(f"Args: {sys.argv}")

    parser = argparse.ArgumentParser(
        description="DAM MCP Server - Digital Asset Management via Model Context Protocol"
    )
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        from dam_mcp import __version__

        print(f"DAM MCP v{__version__}")
        return 0

    logger.info("Starting MCP server with stdio transport")
    mcp_server.run(transport="stdio")
