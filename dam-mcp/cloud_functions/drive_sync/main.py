"""Cloud Function entry point for scheduled Drive-to-GCS sync."""

import json
import os
import time

import functions_framework
from google.cloud import storage
from googleapiclient.discovery import build

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
FOLDER_MIME = "application/vnd.google-apps.folder"
DAM_META_PREFIX = "dam_"
SYNC_STATE_BLOB = ".dam_sync_state.json"


def _get_config():
    return {
        "project_id": os.environ["GCP_PROJECT_ID"],
        "bucket_name": os.environ["GCS_BUCKET_NAME"],
        "folder_id": os.environ["GDRIVE_FOLDER_ID"],
    }


def _get_drive_service():
    import google.auth
    credentials, _ = google.auth.default(scopes=DRIVE_SCOPES)
    return build("drive", "v3", credentials=credentials)


def _get_gcs_bucket(cfg):
    client = storage.Client(project=cfg["project_id"])
    return client.bucket(cfg["bucket_name"])


def _list_drive_files(service, folder_id, path_prefix=""):
    results = []
    page_token = None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType, parents)",
            pageSize=1000,
            pageToken=page_token,
        ).execute()
        for item in resp.get("files", []):
            item_path = f"{path_prefix}{item['name']}" if path_prefix else item["name"]
            if item["mimeType"] == FOLDER_MIME:
                results.extend(_list_drive_files(service, item["id"], f"{item_path}/"))
            else:
                results.append({
                    "id": item["id"],
                    "name": item["name"],
                    "path": item_path,
                    "mimeType": item["mimeType"],
                })
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return results


def _find_blob_by_drive_id(bucket, drive_file_id):
    for blob in bucket.list_blobs():
        blob.reload()
        meta = blob.metadata or {}
        if meta.get(f"{DAM_META_PREFIX}drive_file_id") == drive_file_id:
            return blob
    return None


def _now_iso():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


@functions_framework.http
def sync_handler(request):
    """HTTP Cloud Function entry point."""
    start = time.time()

    cfg = _get_config()
    service = _get_drive_service()
    bucket = _get_gcs_bucket(cfg)
    errors = []

    try:
        drive_files = _list_drive_files(service, cfg["folder_id"])
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)}), 500

    new_synced = 0
    skipped = 0

    for f in drive_files:
        existing = _find_blob_by_drive_id(bucket, f["id"])
        if existing is not None:
            skipped += 1
            continue
        try:
            data = service.files().get_media(fileId=f["id"]).execute()
            blob = bucket.blob(f["path"])
            blob.upload_from_string(data, content_type=f["mimeType"])
            blob.metadata = {
                f"{DAM_META_PREFIX}drive_file_id": f["id"],
                f"{DAM_META_PREFIX}original_filename": f["name"],
                f"{DAM_META_PREFIX}upload_source": "drive_sync",
                f"{DAM_META_PREFIX}campaign": f["path"].split("/")[0] if "/" in f["path"] else "",
                f"{DAM_META_PREFIX}created_at": _now_iso(),
                f"{DAM_META_PREFIX}tags": "",
            }
            blob.patch()
            new_synced += 1
        except Exception as e:
            errors.append(f"{f['path']}: {e}")

    duration = round(time.time() - start, 1)
    state = {
        "last_sync_at": _now_iso(),
        "last_sync_result": "completed",
        "files_synced": new_synced,
        "total_drive_files": len(drive_files),
        "errors": errors,
        "duration_seconds": duration,
    }

    state_blob = bucket.blob(SYNC_STATE_BLOB)
    state_blob.upload_from_string(json.dumps(state, indent=2), content_type="application/json")

    return json.dumps({
        "status": "completed",
        "drive_files_found": len(drive_files),
        "new_files_synced": new_synced,
        "skipped_existing": skipped,
        "errors": errors,
        "duration_seconds": duration,
    }), 200
