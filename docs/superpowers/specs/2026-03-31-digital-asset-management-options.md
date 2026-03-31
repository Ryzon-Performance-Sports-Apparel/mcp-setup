# Digital Asset Management (DAM) — Options for Creative Asset Automation

**Date:** 2026-03-31
**Status:** Discussion draft — awaiting team input before implementation decision

---

## Problem Statement

Today, creative assets (images, videos) live in Google Drive, managed manually by designers. When creating Meta ads via our MCP server, there is no programmatic way to:

- **Browse or search** available creatives from our library
- **Map a specific creative** to an ad being created
- **Automate** the flow from "asset exists" to "asset is live in an ad"

The current meta-ads-mcp server accepts raw base64 data, data URLs, or public URLs — meaning someone must manually locate the file, grab its URL, and paste it in. This is the primary automation bottleneck.

**Design goals:**
- Designers keep uploading to Google Drive (zero workflow disruption)
- Programmatic access for MCP and future AI applications
- Integration-friendly architecture that scales to a professional DAM over time

---

## Option A: GCS Asset Hub with Drive Sync (Integrated)

**Architecture:** Add asset management capabilities directly into the existing `meta-ads-mcp` server.

```
Google Drive (designers upload here)
      |
      v
Cloud Function (watches Drive, syncs new files)
      |
      v
GCP Cloud Storage bucket (canonical asset store)
  + Object metadata (dimensions, format, tags, campaign)
      |
      v
meta-ads-mcp (new tools: search_assets, get_asset, use_asset_in_ad)
```

**New MCP tools added to meta-ads-mcp:**
- `search_assets` — find creatives by name, tags, dimensions, campaign
- `get_asset_details` — retrieve metadata and preview URL for a specific asset
- `create_ad_from_asset` — one-step: fetch asset from GCS + create Meta ad creative

**Infrastructure required:**
- GCP Cloud Storage bucket
- Cloud Function for Drive-to-GCS sync (triggered by Drive API push notifications or polling)
- Object metadata on GCS objects (or a lightweight Firestore collection for richer querying)

**Pros:**
- Single server to manage — simpler operations
- Direct integration between asset lookup and ad creation
- GCS provides a clean, automatable API (unlike Drive)
- Metadata on objects enables structured search

**Cons:**
- Couples asset management to Meta ads — other consumers (Google Ads MCP, future AI apps) would need to either duplicate the logic or depend on meta-ads-mcp
- As asset management grows in complexity, meta-ads-mcp becomes bloated
- Two storage systems to keep in sync (Drive + GCS)

**Best for:** Teams that primarily need asset automation for Meta ads and want the simplest path to get there.

---

## Option B: Standalone DAM MCP Server + GCS Backend (Recommended)

**Architecture:** A new, independent MCP server (`dam-mcp`) that owns all asset management. Other servers (meta-ads-mcp, google-ads-mcp, future apps) consume it.

```
Google Drive (designers upload here)
      |
      v
Cloud Function (watches Drive, syncs new files)
      |
      v
GCP Cloud Storage bucket (canonical asset store)
  + Firestore (asset metadata, tags, campaign mappings)
      |
      v
dam-mcp server (standalone MCP server)
  Tools: search_assets, get_asset, tag_asset, list_assets_by_campaign,
         get_asset_download_url, upload_asset
      |
      +---> meta-ads-mcp (fetches assets via URL, creates ads)
      +---> google-ads-mcp (same pattern)
      +---> future AI apps (connect directly to dam-mcp)
```

**dam-mcp tools:**
| Tool | Description |
|------|-------------|
| `search_assets` | Find assets by name, tags, dimensions, format, campaign, date range |
| `get_asset` | Get full metadata + signed download URL for a specific asset |
| `list_assets` | List assets in a folder/campaign with pagination |
| `tag_asset` | Add/update metadata tags on an asset |
| `get_asset_download_url` | Generate a time-limited signed URL for downloading |
| `upload_asset` | Direct upload path (bypassing Drive, for programmatic use) |
| `sync_status` | Check Drive-to-GCS sync health and recent activity |

**How it works with meta-ads-mcp:**
1. LLM calls `dam-mcp.search_assets(tags=["summer-campaign", "1080x1080"])`
2. LLM picks the right asset, calls `dam-mcp.get_asset_download_url(asset_id)`
3. LLM calls `meta-ads-mcp.upload_ad_image(image_url=signed_url)` then `create_ad_creative(...)`

Or, for tighter integration, meta-ads-mcp could accept an `asset_id` parameter and resolve it internally via the DAM API.

**Infrastructure required:**
- GCP Cloud Storage bucket
- Firestore collection for asset metadata (richer querying than GCS object metadata alone)
- Cloud Function for Drive-to-GCS sync
- New Python MCP server (same FastMCP pattern as meta-ads-mcp)

**Pros:**
- Clean separation of concerns — DAM is independently useful
- Any AI application can connect to the DAM without depending on an ads server
- Scales naturally into a professional DAM (add approval workflows, versioning, usage tracking later)
- Consistent with the monorepo pattern (sits alongside meta-ads-mcp and google-ads-mcp)
- GCS signed URLs work with any consumer that accepts URLs

**Cons:**
- More upfront work than Option A
- Two MCP servers to coordinate during ad creation (though the LLM handles this naturally)
- Firestore adds a small operational cost

**Best for:** Teams that want a future-proof foundation, plan to have multiple AI consumers, or anticipate growing into a professional DAM.

---

## Option C: Direct Google Drive Integration

**Architecture:** Add Google Drive API tools directly to meta-ads-mcp. No GCS layer.

```
Google Drive (designers upload here)
      |
      v
meta-ads-mcp (new tools: list_drive_files, search_drive, download_and_upload)
```

**New MCP tools:**
- `list_drive_folder` — browse a Drive folder's contents
- `search_drive_assets` — search Drive by filename/type
- `create_ad_from_drive_file` — download from Drive + upload to Meta in one step

**Infrastructure required:**
- Google Drive API credentials (OAuth or service account)
- No new storage systems

**Pros:**
- Fastest to implement — no new infrastructure
- Single source of truth (Drive)
- Designers' workflow is completely unchanged

**Cons:**
- Drive API is not designed for programmatic asset management (rate limits, awkward search, no structured metadata)
- Tightly couples DAM to meta-ads-mcp
- No metadata/tagging layer — search is limited to filename and folder structure
- Other consumers would need their own Drive integration
- Dead end for DAM ambitions — Drive doesn't scale as a professional asset management backend

**Best for:** Quick win if the only goal is "make current workflow slightly less manual" with no plans for growth.

---

## Comparison Matrix

| Criteria | A: GCS Integrated | B: DAM MCP (Rec.) | C: Drive Direct |
|----------|-------------------|---------------------|-----------------|
| Implementation effort | Medium | Medium-High | Low |
| Designer workflow change | None | None | None |
| Programmatic access quality | High (GCS API) | High (GCS API) | Low (Drive API) |
| Multi-consumer ready | No | Yes | No |
| Metadata / tagging | Basic (object meta) | Rich (Firestore) | None (filenames only) |
| Future DAM scalability | Limited | High | None |
| Operational complexity | Medium | Medium-High | Low |
| Infrastructure cost | ~$5-20/mo (GCS) | ~$10-30/mo (GCS + Firestore) | $0 |

---

## Recommendation

**Option B (Standalone DAM MCP Server)** is recommended because:

1. It aligns with the stated goal of a professional, integration-friendly DAM
2. It follows the existing monorepo pattern (a third MCP server alongside the two existing ones)
3. The incremental cost over Option A is small, but the architectural benefit is significant
4. It naturally supports the "multiple AI consumers" future without rework

**Suggested phasing:**
- **Phase 1:** GCS bucket + Drive sync Cloud Function + basic dam-mcp with `search_assets`, `get_asset`, `list_assets`
- **Phase 2:** Firestore metadata layer + tagging tools + integration with meta-ads-mcp (accept `asset_id`)
- **Phase 3:** Approval workflows, versioning, usage analytics, Google Ads integration

---

## Open Questions for Team Discussion

1. **GCP project:** Should this use an existing GCP project or a new one? Who manages billing?
2. **Drive folder scope:** Which Drive folder(s) should be synced? All of them or specific ones?
3. **Metadata schema:** What metadata matters most for finding the right creative? (e.g., campaign name, ad format, dimensions, product line, language)
4. **Access control:** Should the DAM have any notion of permissions, or is it open to all authenticated consumers?
5. **Sync frequency:** Real-time (Drive push notifications) or periodic (e.g., every 5 minutes)?
6. **Video handling:** Videos are large — should they be synced to GCS or just indexed with a Drive reference?

---

*This document is a discussion draft. No implementation will begin until the team aligns on an approach.*
