"""Migrate existing documents to the new sensitivity model.

Maps old sensitivity values to new ones:
  "safe" -> "internal" (conservative default)
  "contains_pii" -> "restricted" (in knowledge_base_restricted, copy back)
  "unreviewed" -> "confidential" (fail-secure)

Also adds empty fields for new classification data and resets processing_status
to trigger re-classification with the updated LLM classifier.

Usage:
    python scripts/migrate_sensitivity.py [--dry-run]
"""

import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from google.cloud import firestore

load_dotenv()

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATABASE = os.environ.get("FIRESTORE_DATABASE", "(default)")

SENSITIVITY_MAP = {
    "safe": "internal",
    "contains_pii": "restricted",
    "unreviewed": "confidential",
}


def migrate(dry_run: bool = False):
    if not PROJECT_ID:
        print("ERROR: GCP_PROJECT_ID not set")
        return

    client = firestore.Client(project=PROJECT_ID, database=DATABASE)
    now = datetime.now(timezone.utc)

    # Phase 1: Migrate documents in knowledge_base
    print("Phase 1: Migrating knowledge_base documents...")
    kb_docs = client.collection("knowledge_base").stream()
    updated = 0
    skipped = 0

    for doc in kb_docs:
        data = doc.to_dict()
        old_sensitivity = data.get("sensitivity", "unreviewed")

        # Skip if already using new model
        if old_sensitivity in ("public", "internal", "confidential", "restricted"):
            skipped += 1
            continue

        new_sensitivity = SENSITIVITY_MAP.get(old_sensitivity, "confidential")

        updates = {
            "sensitivity": new_sensitivity,
            "sensitivity_reasons": data.get("sensitivity_reasons", []),
            "content_categories": data.get("content_categories", []),
            "mentioned_persons": data.get("mentioned_persons", []),
            "processing_status": "raw",  # trigger re-classification
            "updated_at": firestore.SERVER_TIMESTAMP,
        }

        if dry_run:
            print(f"  [DRY RUN] {doc.id}: '{old_sensitivity}' -> '{new_sensitivity}'")
        else:
            doc.reference.update(updates)
            print(f"  {doc.id}: '{old_sensitivity}' -> '{new_sensitivity}'")
        updated += 1

    print(f"  Updated: {updated}, Skipped (already migrated): {skipped}")

    # Phase 2: Copy documents from knowledge_base_restricted back to knowledge_base
    print("\nPhase 2: Copying knowledge_base_restricted documents to knowledge_base...")
    restricted_docs = list(client.collection("knowledge_base_restricted").stream())
    copied = 0

    for doc in restricted_docs:
        data = doc.to_dict()

        # Check if already exists in knowledge_base
        existing = client.collection("knowledge_base").document(doc.id).get()
        if existing.exists:
            print(f"  SKIP {doc.id}: already exists in knowledge_base")
            continue

        data["sensitivity"] = "restricted"
        data["sensitivity_reasons"] = data.get("sensitivity_reasons", ["pii"])
        data["content_categories"] = data.get("content_categories", [])
        data["mentioned_persons"] = data.get("mentioned_persons", [])
        data["processing_status"] = "raw"  # trigger re-classification
        data["created_at"] = firestore.SERVER_TIMESTAMP
        data["updated_at"] = firestore.SERVER_TIMESTAMP

        if dry_run:
            print(f"  [DRY RUN] Copy {doc.id} to knowledge_base (sensitivity: restricted)")
        else:
            client.collection("knowledge_base").document(doc.id).set(data)
            print(f"  Copied {doc.id} to knowledge_base (sensitivity: restricted)")
        copied += 1

    print(f"  Copied: {copied}")
    print(f"\nMigration {'would be ' if dry_run else ''}complete.")
    if not dry_run:
        print("Documents with processing_status='raw' will be re-classified by the document processor.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN MODE ===\n")
    migrate(dry_run=dry_run)
