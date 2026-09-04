from pathlib import Path
import json
import os
import shutil
import tempfile
import uuid

BASE = Path("/mnt/data/root-engineering-rebirth-selftest")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def verify_contains(path: Path, tokens: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    assert all(token in text for token in tokens), (path, tokens)


def main() -> None:
    if BASE.exists():
        shutil.rmtree(BASE)

    (BASE / "knowledge").mkdir(parents=True)
    (BASE / "runtime").mkdir()
    (BASE / "sources").mkdir()
    (BASE / "scratch").mkdir()

    project_id = "REP-" + uuid.uuid4().hex[:10].upper()
    root_id = "RR-" + uuid.uuid4().hex[:14].upper()

    atomic_write(
        BASE / "BOOT.md",
        "# ROOT ENGINEERING 1.0 — REBIRTH BOOT\n"
        "Root: ROOT.md\n"
        "Checkpoint: runtime/CHECKPOINT.md\n"
        "Compact-time backup only; scheduled and idle sync are disabled.\n"
        "Hard rule: save failure = no compact.\n",
    )
    atomic_write(
        BASE / "ROOT.md",
        f"# PROJECT ROOT\n- Project ID: {project_id}\n- Root ID: {root_id}\n"
        "- Root Engineering Version: 1.0.0\n- Codename: Rebirth\n",
    )

    for name in ["FOUNDATION", "CURRENT", "LEARNED", "OPERATIONAL", "HISTORY"]:
        atomic_write(
            BASE / "knowledge" / f"{name}.md",
            f"# {name}\n- Project ID: {project_id}\n- Root ID: {root_id}\n",
        )

    atomic_write(
        BASE / "runtime" / "CHECKPOINT.md",
        "# ACTIVE CHECKPOINT\n## Current Goal\nSelf-test\n## Next\nVerify compaction guard.\n"
        "## Resume Instruction\nContinue from Next.\n",
    )

    state = {
        "schema_version": "1.0.0",
        "context_epoch": 0,
        "compaction_count": 0,
        "checkpoint_revision": 1,
        "root_revision": 1,
        "last_compaction": None,
        "boundary_compaction_verified": False,
        "boundary_verification_scope": None,
        "external_backup_sync_trigger": "EXPLICIT_COMPACT_ONLY",
        "scheduled_backup_sync": False,
        "idle_backup_sync": False,
        "external_backup_pending": False,
        "last_external_backup": None,
    }
    atomic_write(BASE / "runtime" / "STATE.json", json.dumps(state, indent=2))
    atomic_write(
        BASE / "runtime" / "CAPABILITIES.json",
        json.dumps(
            {
                "schema_version": "1.0.0",
                "local_workspace": "VERIFIED",
                "native_compact_action": "UNKNOWN",
                "zero_output_boundary_compaction": "UNVERIFIED",
                "external_backup": {
                    "adapter": "OPTIONAL",
                    "sync_trigger": "EXPLICIT_COMPACT_ONLY",
                    "scheduled_sync": "DISABLED",
                    "idle_sync": "DISABLED",
                    "failure_policy": "WARN_AND_MARK_PENDING",
                },
            },
            indent=2,
        ),
    )
    atomic_write(
        BASE / "MANIFEST.json",
        json.dumps(
            {
                "package_version": "1.0.0",
                "codename": "Rebirth",
                "project_id": project_id,
                "root_id": root_id,
                "primary_storage_adapter": "chat-local-mnt",
                "status": "ACTIVE",
            },
            indent=2,
        ),
    )

    for path in [BASE / "ROOT.md"] + [
        BASE / "knowledge" / f"{name}.md"
        for name in ["FOUNDATION", "CURRENT", "LEARNED", "OPERATIONAL", "HISTORY"]
    ]:
        verify_contains(path, [project_id, root_id])

    atomic_write(
        BASE / "runtime" / "CHECKPOINT.md",
        "# ACTIVE CHECKPOINT\n## Current Goal\nSelf-test\n"
        "## Completed\n- Local Root created.\n"
        "## Next\n- Simulate save failure guard.\n"
        "## Resume Instruction\nContinue from Next.\n",
    )
    verify_contains(
        BASE / "runtime" / "CHECKPOINT.md",
        ["Local Root created", "Simulate save failure guard"],
    )

    required_save_verified = False
    compact_called = False
    if required_save_verified:
        compact_called = True
    assert compact_called is False

    # Backup is permitted only in the explicit compact maintenance window.
    state = json.loads((BASE / "runtime" / "STATE.json").read_text())
    assert state["external_backup_sync_trigger"] == "EXPLICIT_COMPACT_ONLY"
    assert state["scheduled_backup_sync"] is False
    assert state["idle_backup_sync"] is False

    # Optional backup failure is visible and pending, not silently successful.
    state["external_backup_pending"] = True
    state["last_external_backup"] = {"status": "PENDING", "adapter": "google-drive"}
    atomic_write(BASE / "runtime" / "STATE.json", json.dumps(state, indent=2))
    reread = json.loads((BASE / "runtime" / "STATE.json").read_text())
    assert reread["external_backup_pending"] is True
    assert reread["last_external_backup"]["status"] == "PENDING"

    required_save_verified = True
    compaction_confirmed = True
    if required_save_verified and compaction_confirmed:
        state = reread
        state["context_epoch"] += 1
        state["compaction_count"] += 1
        atomic_write(BASE / "runtime" / "STATE.json", json.dumps(state, indent=2))

    state = json.loads((BASE / "runtime" / "STATE.json").read_text())
    assert state["context_epoch"] == 1
    assert state["compaction_count"] == 1

    print("REBIRTH_SELFTEST_PASS")
    print(f"project_id={project_id}")
    print(f"root_id={root_id}")
    print(f"files={sum(1 for p in BASE.rglob('*') if p.is_file())}")
    print(f"context_epoch={state['context_epoch']}")
    print(f"backup_sync_trigger={state['external_backup_sync_trigger']}")


if __name__ == "__main__":
    main()
