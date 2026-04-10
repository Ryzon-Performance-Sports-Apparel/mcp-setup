"""Seed default access policies into Firestore.

Usage:
    python scripts/seed_policies.py

Requires GCP_PROJECT_ID and FIRESTORE_DATABASE env vars.
"""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from google.cloud import firestore

load_dotenv()

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATABASE = os.environ.get("FIRESTORE_DATABASE", "(default)")

POLICIES = {
    "admin": {
        "name": "Admin — Full Access",
        "priority": 400,
        "match_roles": ["admin"],
        "allow_sensitivity": ["public", "internal", "confidential", "restricted"],
        "allow_content_categories": ["*"],
        "deny_content_categories": [],
        "participant_override": True,
        "feedback_subject_exclusion": False,
    },
    "hr": {
        "name": "HR — Full Access Including Compensation",
        "priority": 350,
        "match_roles": ["hr"],
        "allow_sensitivity": ["public", "internal", "confidential", "restricted"],
        "allow_content_categories": ["*"],
        "deny_content_categories": [],
        "participant_override": True,
        "feedback_subject_exclusion": False,
    },
    "leadership": {
        "name": "Leadership Access",
        "priority": 300,
        "match_roles": ["leadership"],
        "allow_sensitivity": ["public", "internal", "confidential"],
        "allow_content_categories": ["*"],
        "deny_content_categories": ["compensation"],
        "participant_override": True,
        "feedback_subject_exclusion": False,
    },
    "team_lead": {
        "name": "Team Lead Access",
        "priority": 200,
        "match_roles": ["team_lead"],
        "allow_sensitivity": ["public", "internal", "confidential"],
        "allow_content_categories": [
            "project_update", "technical", "product_roadmap",
            "performance_review", "strategy",
        ],
        "deny_content_categories": ["compensation", "legal"],
        "participant_override": True,
        "feedback_subject_exclusion": True,
    },
    "employee": {
        "name": "Default Employee Access",
        "priority": 100,
        "match_roles": ["employee"],
        "allow_sensitivity": ["public", "internal"],
        "allow_content_categories": ["project_update", "technical", "product_roadmap"],
        "deny_content_categories": [
            "hr_process", "compensation", "legal", "interpersonal_feedback",
        ],
        "participant_override": True,
        "feedback_subject_exclusion": True,
    },
    "external": {
        "name": "External/Contractor Access",
        "priority": 50,
        "match_roles": ["external"],
        "allow_sensitivity": ["public"],
        "allow_content_categories": ["project_update", "technical"],
        "deny_content_categories": [
            "strategy", "hr_process", "client_data", "financial",
            "legal", "interpersonal_feedback", "compensation",
        ],
        "participant_override": True,
        "feedback_subject_exclusion": True,
    },
}


def seed():
    if not PROJECT_ID:
        print("ERROR: GCP_PROJECT_ID not set")
        return

    client = firestore.Client(project=PROJECT_ID, database=DATABASE)
    now = datetime.now(timezone.utc)

    print(f"Seeding {len(POLICIES)} policies to _access_policies...")
    for policy_id, policy_data in POLICIES.items():
        doc_ref = client.collection("_access_policies").document(policy_id)
        doc_ref.set({
            **policy_data,
            "created_at": now,
            "updated_at": now,
        })
        print(f"  {policy_id}: {policy_data['name']}")

    # Seed initial admin user
    USERS = {
        "simon_heinken": {
            "email": "simon@ryzon.net",
            "roles": ["admin", "leadership"],
            "department": "engineering",
            "employment_type": "permanent",
            "teams": ["engineering", "product"],
        },
    }

    print(f"\nSeeding {len(USERS)} users to _access_roles...")
    for user_id, user_data in USERS.items():
        doc_ref = client.collection("_access_roles").document(user_id)
        doc_ref.set({
            **user_data,
            "created_at": now,
            "updated_at": now,
        })
        print(f"  {user_id}: {user_data['email']} ({', '.join(user_data['roles'])})")

    print("\nDone. Policies and users seeded successfully.")


if __name__ == "__main__":
    seed()
