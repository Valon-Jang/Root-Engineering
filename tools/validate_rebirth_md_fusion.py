#!/usr/bin/env python3
"""Validate Root Engineering 1.0 Rebirth Markdown fusion invariants."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


VERSION = "1.0.0"

INSTALLER_METADATA_KEYS = {
    "package_version": "1.0.0",
    "schema_version": "1.0.0",
    "three_layer_memory_model": "transcript-active-context-local-root",
    "checkpoint_owner": "runtime/CHECKPOINT.md",
    "compaction_transaction": "persist-verify-compact-rehydrate",
    "backup_sync_policy": "event-driven-dirty-only",
    "backup_on_compaction": "configured-and-hash-changed",
    "optional_backup_failure_blocks_compaction": "false",
    "strict_backup_compaction_command": "true",
    "backup_direction": "local-to-external-one-way",
}

REQUIRED: dict[str, set[str]] = {
    "installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md": {
        "Local Storage Gate",
        "LOCAL CAPABILITY WORKSPACE",
        "External adapter reality gate",
        "Required local save or Storage Gate failure = no compact.",
        "policy declaration is not an executable adapter",
        "only one compaction trigger Skill",
        "Skills preserve reusable capability",
    },
    "installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md": {
        "Local Save가 검증된 뒤",
        "backup_sync_policy: event-driven-dirty-only",
        "external_backup_pending = true",
        "백업하고 압축해",
        "정상 흐름은 Local → External Backup",
        "필수 Local Save 실패 = No Compact",
    },
    "docs/ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION.md": {
        "Research may discover behavior. Rebirth owns the production contract.",
        "One trigger owner",
        "Pre-Compaction Save Gate",
        "Local Storage Gate",
        "A policy declaration is not an executable adapter.",
        "Do not install a second `persistent-project-thread` Skill",
    },
    "docs/ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION_KO.md": {
        "연구는 동작을 발견하고, Rebirth가 Production 계약을 소유한다.",
        "Trigger Owner는 하나",
        "Pre-Compaction Save Gate",
        "Local Storage Gate",
        "정책 문구가 있다는 것과 실행 가능한 Adapter가 있다는 것은 다르다.",
    },
    "docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md": {
        "event-driven",
        "hash",
        "Local → external",
        "strict backup-and-compact failure blocks compaction",
    },
    "docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY_KO.md": {
        "Event 기반",
        "Hash",
        "Local → External",
        "백업하고 압축해",
    },
    "docs/ROOT_ENGINEERING_1.0_REBIRTH.md": {
        "LOCAL CAPABILITY WORKSPACE",
        "Document authority",
        "Local Storage Gate",
        "A Google Drive policy is not proof that a Drive adapter ran.",
        "Persistent Project Thread",
    },
    "installer/rebirth/root-engineering/SKILL.md": {
        "single operational owner of `압축해`",
        "Run the Local Storage Gate",
        "External policy text is not proof that an adapter executed.",
        "Strict `백업하고 압축해`",
        "Local Capability Workspace",
    },
    "installer/rebirth/README.md": {
        "Canonical package composition",
        "single operational owner for `압축해`",
        "Google Drive synchronization is real only when",
        "validate_rebirth_md_fusion.py",
    },
}

FORBIDDEN_DUPLICATE_SKILL = "installer/rebirth/persistent-project-thread/SKILL.md"


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo",
        nargs="?",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="repository root",
    )
    repo = parser.parse_args().repo.resolve()
    errors: list[str] = []

    for relative, needles in REQUIRED.items():
        path = repo / relative
        if not path.is_file():
            errors.append(f"missing file: {relative}")
            continue
        text = read(path)
        for needle in sorted(needles):
            if needle not in text:
                errors.append(f"{relative}: missing {needle!r}")

    english_path = repo / "installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md"
    korean_path = repo / "installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md"
    if english_path.is_file() and korean_path.is_file():
        english = frontmatter(read(english_path))
        korean = frontmatter(read(korean_path))
        for key, expected in INSTALLER_METADATA_KEYS.items():
            for label, metadata in (("EN", english), ("KO", korean)):
                actual = metadata.get(key)
                if actual != expected:
                    errors.append(
                        f"{label} installer metadata {key!r}: expected {expected!r}, got {actual!r}"
                    )
        for key in INSTALLER_METADATA_KEYS:
            if english.get(key) != korean.get(key):
                errors.append(
                    f"installer semantic mirror mismatch for {key!r}: "
                    f"EN={english.get(key)!r}, KO={korean.get(key)!r}"
                )

    duplicate = repo / FORBIDDEN_DUPLICATE_SKILL
    if duplicate.exists():
        errors.append(
            "duplicate compaction trigger Skill exists: " + FORBIDDEN_DUPLICATE_SKILL
        )

    version_path = repo / "VERSION"
    if not version_path.is_file():
        errors.append("missing VERSION")
    else:
        lines = read(version_path).splitlines()
        if lines[:2] != [VERSION, "Rebirth"]:
            errors.append(f"VERSION changed unexpectedly: {lines[:2]!r}")

    if errors:
        print("REBIRTH MD FUSION VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("REBIRTH MD FUSION VALIDATION: PASS")
    print("- package/schema: 1.0.0")
    print("- authority map and single trigger owner: present")
    print("- EN/KO installer metadata: synchronized")
    print("- Root resolution + Local Storage Gate: present")
    print("- event/hash/adapter-gated external backup: present")
    print("- optional vs strict backup semantics: present")
    print("- Local Capability Workspace without second Root: present")
    print("- persistent-project-thread retained as research provenance: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
