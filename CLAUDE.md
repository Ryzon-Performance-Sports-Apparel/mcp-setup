# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Monorepo containing two MCP (Model Context Protocol) servers for managing ad platforms via LLMs, plus a unified install script for non-technical users to set up Claude Desktop.

- **`meta-ads-mcp/`** — Meta (Facebook/Instagram) Ads MCP server (Python, FastMCP). Published to PyPI as `meta-ads-mcp`. See `meta-ads-mcp/CLAUDE.md` for detailed architecture.
- **`google-ads-mcp/`** — Google Ads MCP server (Python, Google Ads API). External upstream: `github.com/googleads/google-ads-mcp`.
- **`install.sh`** + **`SETUP_GUIDE.md`** — One-click installer that configures both servers for Claude Desktop on macOS.

## Commands

### meta-ads-mcp

```bash
cd meta-ads-mcp
pip install -e .                    # Install in dev mode
python -m meta_ads_mcp              # Run server (stdio)
python -m meta_ads_mcp --transport streamable-http --port 8080  # HTTP transport
pytest tests/ -v                    # Run unit tests (e2e excluded by default)
pytest tests/test_something.py -v   # Run single test file
pytest tests/ -v -m e2e             # Run e2e tests (requires running server)
python -m build                     # Build wheel
```

### google-ads-mcp

```bash
cd google-ads-mcp
pip install -e ".[dev]"             # Install with dev deps (black, nox)
nox                                 # Run test suite via nox
```

## Architecture

### meta-ads-mcp

Entry point: `meta_ads_mcp/__init__.py:entrypoint()` → `core/server.py:main()` → FastMCP server with registered tools.

Key modules in `meta_ads_mcp/core/`:
- `server.py` — CLI args, FastMCP init, transport selection
- `api.py` — HTTP wrapper for Meta Graph API v24.0 (rate limiting, error handling)
- `ads.py` — Largest module (~2,600 lines): ad/creative CRUD, image upload, all creative formats
- `campaigns.py`, `adsets.py` — Campaign and ad set CRUD
- `targeting.py` — Interest/behavior/location/demographic targeting search
- `insights.py` — Performance metrics
- `ryzon_config.py` + `ryzon_defaults.py` — Client-specific defaults activated by `RYZON_MODE=1` env var

Tools are registered via `@mcp_server.tool()` decorators in each module.

### google-ads-mcp

Entry point: `ads_mcp/server.py:run_server()`. Uses `coordinator.py` for GAQL query orchestration. Tools live in `ads_mcp/tools/`.

## Environment Variables

- `META_ACCESS_TOKEN` — Meta API token (required for meta-ads-mcp)
- `RYZON_MODE=1` — Activates Ryzon-specific defaults (account IDs, DSA fields, tracking, UTM params)
- `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_PROJECT_ID` — Required for google-ads-mcp
- `MCP_TEST_SERVER_URL` — e2e test target (default: `http://localhost:8080`)

## Release (meta-ads-mcp)

Version must be bumped in three files simultaneously:
1. `meta-ads-mcp/pyproject.toml`
2. `meta-ads-mcp/meta_ads_mcp/__init__.py`
3. `meta-ads-mcp/server.json`

PyPI publishing is automated via GitHub release + trusted publishing (OIDC).

## Testing (meta-ads-mcp)

- Uses `pytest-asyncio` with `asyncio_mode = "auto"`
- Unit tests mock Meta API calls; e2e tests use `@pytest.mark.e2e`
- Default pytest config excludes e2e: `addopts = "-v --strict-markers -m 'not e2e'"`
