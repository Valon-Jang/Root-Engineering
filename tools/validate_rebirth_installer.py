from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer" / "ROOT_ENGINEERING_REBIRTH_INSTALLER.md"

text = INSTALLER.read_text(encoding="utf-8")

required = [
    "package_version: 1.0.0",
    "codename: Rebirth",
    "primary_storage_adapter: chat-local-mnt",
    "project_required: false",
    "google_drive_required: false",
    "runtime/CHECKPOINT.md",
    "context_epoch",
    "SAVE FAILURE = NO COMPACT",
    "supported native compact action",
    "zero-output boundary fallback",
    "Never claim chat-local `/mnt/data` is permanent",
    "EXPLICIT_COMPACT_ONLY",
    "Complete Chat Runtime",
    "idle_backup_sync: false",
    "scheduled_backup_sync: false",
    "external_backup_sync_trigger: explicit-compact-only",
]

forbidden = [
    "thread/compact/start RPC >",
    "Google Drive is required",
    "Project Instructions must",
]

missing = [item for item in required if item not in text]
found_forbidden = [item for item in forbidden if item in text]

if missing or found_forbidden:
    print("FAIL")
    if missing:
        print("missing:", missing)
    if found_forbidden:
        print("forbidden:", found_forbidden)
    sys.exit(1)

assert len(re.findall(r"^## ", text, re.MULTILINE)) >= 10
print("PASS")
print(f"bytes={len(text.encode('utf-8'))}")
