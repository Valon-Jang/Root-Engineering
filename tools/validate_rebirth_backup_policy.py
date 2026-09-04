#!/usr/bin/env python3
"""Validate Root Engineering 1.0.0 Rebirth explicit compact-time recovery sync."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED_INSTALLER = {
    "package_version: 1.0.0",
    "schema_version: 1.0.0",
    "external_backup_sync_trigger: explicit-compact-only",
    "scheduled_backup_sync: false",
    "idle_backup_sync: false",
    "### Default backup cadence: explicit COMPACT only",
    "EXPLICIT_COMPACT_ONLY",
    "external_backup_pending=true",
    "SAVE FAILURE = NO COMPACT",
}

REQUIRED_POLICY = {
    "Version impact: none",
    "EXPLICIT_COMPACT_ONLY",
    "Scheduled, idle, timer-based, and background synchronization are disabled",
    "root-engineering-latest.zip",
    "BACKUP_MANIFEST.json",
    "Complete Chat Runtime",
    "Local → external",
}

FORBIDDEN = {
    "backup_sync_policy: event-driven-dirty-only",
    "critical authority, routing, or structure change | update `latest` immediately",
    "`마무리하자` / explicit closeout | update `latest`",
}


def require(path: Path, needles: set[str]) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    errors = [f"{path}: missing {needle!r}" for needle in sorted(needles) if needle not in text]
    errors += [f"{path}: forbidden legacy policy {needle!r}" for needle in sorted(FORBIDDEN) if needle in text]
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo",
        nargs="?",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="repository root",
    )
    args = parser.parse_args()
    repo = args.repo.resolve()

    errors: list[str] = []
    errors += require(repo / "installer" / "ROOT_ENGINEERING_REBIRTH_INSTALLER.md", REQUIRED_INSTALLER)
    errors += require(repo / "docs" / "ROOT_ENGINEERING_1.0_BACKUP_POLICY.md", REQUIRED_POLICY)

    version = repo / "VERSION"
    if not version.is_file():
        errors.append(f"missing file: {version}")
    else:
        value = version.read_text(encoding="utf-8").splitlines()
        if value[:2] != ["1.0.0", "Rebirth"]:
            errors.append(f"VERSION changed unexpectedly: {value[:2]!r}")

    if errors:
        print("REBIRTH BACKUP POLICY VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("REBIRTH BACKUP POLICY VALIDATION: PASS")
    print("- package version: 1.0.0")
    print("- sync trigger: EXPLICIT_COMPACT_ONLY")
    print("- scheduled/idle/background sync: disabled")
    print("- Local -> external recovery authority: present")
    print("- Complete Chat Runtime framing: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
