#!/usr/bin/env python3
"""Validate the Root Engineering 1.0.0 Rebirth backup-policy update."""

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
    "backup_on_compaction: configured-and-hash-changed",
    "optional_backup_failure_blocks_compaction: false",
    "strict_backup_compaction_command: true",
    "### 9.1 Explicit compact-time cadence — no scheduled or idle loop",
    "root-engineering-latest.zip",
    "external_backup_pending = true",
    "`백업하고 압축해`",
    "Local → external backup",
}

REQUIRED_POLICY = {
    "Version impact: none",
    "EXPLICIT_COMPACT_ONLY",
    "root-engineering-latest.zip",
    "BACKUP_MANIFEST.json",
    "Local → external",
    "strict backup-and-compact failure blocks compaction",
}


def require(path: Path, needles: set[str]) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    return [f"{path}: missing {needle!r}" for needle in sorted(needles) if needle not in text]


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
    errors += require(
        repo / "installer" / "ROOT_ENGINEERING_REBIRTH_INSTALLER.md",
        REQUIRED_INSTALLER,
    )
    errors += require(
        repo / "docs" / "ROOT_ENGINEERING_1.0_BACKUP_POLICY.md",
        REQUIRED_POLICY,
    )

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
    print("- schema version: 1.0.0")
    print("- explicit-compact-only hash-gated backup policy: present")
    print("- optional vs strict backup failure semantics: present")
    print("- Local -> external one-way authority: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
