#!/usr/bin/env python3
"""Root Engineering 1.0 Rebirth transaction guard.

This helper does not compact ChatGPT or upload to an external service by itself.
It protects Local ROOT/CHECKPOINT state, seals a compaction transaction, records
explicit compact-time backup outcomes, and advances context epoch only after
host compaction is explicitly observed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "1.0.0"
DEFAULT_ROOT = Path("/mnt/data/root-engineering")
METHODS = ("native", "zero-output-boundary", "manual-confirmation", "diagnostic")
SIGNALS = ("HOST_EVENT", "CONTEXT_REPLACEMENT_OBSERVED", "MANUAL_CONFIRMATION")
BACKUP_STATUSES = ("VERIFIED", "PENDING", "SKIPPED")
BACKUP_TRIGGER = "EXPLICIT_COMPACT_ONLY"

REQUIRED = (
    "BOOT.md",
    "ROOT.md",
    "MANIFEST.json",
    "knowledge/FOUNDATION.md",
    "knowledge/CURRENT.md",
    "knowledge/LEARNED.md",
    "knowledge/OPERATIONAL.md",
    "knowledge/HISTORY.md",
    "runtime/CHECKPOINT.md",
    "runtime/STATE.json",
    "runtime/CAPABILITIES.json",
)
CANONICAL = (
    "ROOT.md",
    "knowledge/FOUNDATION.md",
    "knowledge/CURRENT.md",
    "knowledge/LEARNED.md",
    "knowledge/OPERATIONAL.md",
    "knowledge/HISTORY.md",
)


class RebirthError(RuntimeError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RebirthError(f"missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RebirthError(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RebirthError(f"JSON root must be an object: {path}")
    return value


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temp = Path(raw)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_digest(root: Path) -> tuple[str, dict[str, str]]:
    aggregate = hashlib.sha256()
    items: dict[str, str] = {}
    for relative in CANONICAL:
        path = root / relative
        if not path.is_file():
            raise RebirthError(f"missing canonical file: {relative}")
        item_hash = file_sha256(path)
        items[relative] = item_hash
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(item_hash.encode("ascii"))
        aggregate.update(b"\n")
    return aggregate.hexdigest(), items


def verify(root: Path) -> dict[str, Any]:
    root = root.resolve()
    missing = [relative for relative in REQUIRED if not (root / relative).is_file()]
    if missing:
        raise RebirthError("missing required paths: " + ", ".join(missing))

    manifest = read_json(root / "MANIFEST.json")
    state = read_json(root / "runtime/STATE.json")
    capabilities = read_json(root / "runtime/CAPABILITIES.json")
    project_id, root_id = manifest.get("project_id"), manifest.get("root_id")
    if not project_id or not root_id:
        raise RebirthError("manifest identity is incomplete")
    if manifest.get("package_version") != VERSION:
        raise RebirthError("manifest package version mismatch")
    if manifest.get("status") != "ACTIVE":
        raise RebirthError("manifest is not ACTIVE")
    if state.get("package_version", VERSION) != VERSION:
        raise RebirthError("runtime package version mismatch")
    if state.get("status", "ACTIVE") not in ("ACTIVE", "READY_TO_COMPACT"):
        raise RebirthError("runtime state is not ACTIVE")
    if state.get("external_backup_sync_trigger", BACKUP_TRIGGER) != BACKUP_TRIGGER:
        raise RebirthError("backup trigger must remain EXPLICIT_COMPACT_ONLY")
    if state.get("scheduled_backup_sync", False):
        raise RebirthError("scheduled backup sync must remain disabled")
    if state.get("idle_backup_sync", False):
        raise RebirthError("idle backup sync must remain disabled")

    for label, value in (("state", state), ("capabilities", capabilities)):
        for key, expected in (("project_id", project_id), ("root_id", root_id)):
            actual = value.get(key)
            if actual is not None and actual != expected:
                raise RebirthError(f"{label} identity mismatch: {key}")

    for relative in CANONICAL:
        text = (root / relative).read_text(encoding="utf-8")
        if str(project_id) not in text or str(root_id) not in text:
            raise RebirthError(f"canonical identity missing: {relative}")

    checkpoint = (root / "runtime/CHECKPOINT.md").read_text(encoding="utf-8")
    if "## Resume Instruction" not in checkpoint:
        raise RebirthError("checkpoint heading missing: ## Resume Instruction")
    if "## Exact Next Action" not in checkpoint and "## Next" not in checkpoint:
        raise RebirthError("checkpoint next-action heading is missing")

    digest, hashes = canonical_digest(root)
    return {
        "ok": True,
        "version": VERSION,
        "root": str(root),
        "project_id": project_id,
        "root_id": root_id,
        "context_epoch": int(state.get("context_epoch", 0)),
        "compaction_count": int(state.get("compaction_count", 0)),
        "canonical_digest": digest,
        "canonical_hashes": hashes,
        "checkpoint_sha256": file_sha256(root / "runtime/CHECKPOINT.md"),
        "pending_compaction": state.get("pending_compaction"),
        "external_backup_pending": bool(state.get("external_backup_pending", False)),
    }


def checkpoint_text(identity: dict[str, Any], epoch: int, args: argparse.Namespace) -> str:
    return f"""# ACTIVE CHECKPOINT

- Root Engineering Version: {VERSION}
- Project ID: {identity['project_id']}
- Root ID: {identity['root_id']}
- Checkpoint Time: {now()}
- Context Epoch Before Compact: {epoch}
- Status: READY_FOR_PREPARE

## Current Goal
{args.goal.strip()}

## Active Work
{args.active_work.strip()}

## Completed Since Last Checkpoint
{args.completed.strip()}

## Durable State Promoted
{args.promoted.strip()}

## Important Unresolved
{args.unresolved.strip()}

## Exact Next Action
{args.next_action.strip()}

## Resume Instruction
{args.resume.strip()}
"""


def write_checkpoint(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    checked = verify(root)
    state_path = root / "runtime/STATE.json"
    state = read_json(state_path)
    if state.get("pending_compaction"):
        raise RebirthError("cannot replace checkpoint while compaction is pending")
    values = (args.goal, args.active_work, args.completed, args.promoted, args.unresolved, args.next_action, args.resume)
    if any(not value.strip() for value in values):
        raise RebirthError("checkpoint fields must not be blank")
    text = checkpoint_text(checked, checked["context_epoch"], args)
    path = root / "runtime/CHECKPOINT.md"
    atomic_text(path, text)
    expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if file_sha256(path) != expected:
        raise RebirthError("checkpoint read-back hash mismatch")
    state["checkpoint_revision"] = int(state.get("checkpoint_revision", 0)) + 1
    state["last_checkpoint_at"] = now()
    state["last_error"] = None
    state["updated_at"] = now()
    atomic_json(state_path, state)
    return {"ok": True, "checkpoint_sha256": expected, "checkpoint_revision": state["checkpoint_revision"]}


def prepare(root: Path, reason: str) -> dict[str, Any]:
    checked = verify(root)
    state_path = root / "runtime/STATE.json"
    state = read_json(state_path)
    if state.get("pending_compaction"):
        raise RebirthError("a compaction transaction is already pending")
    transaction = {
        "transaction_id": "RB-" + uuid.uuid4().hex[:12].upper(),
        "status": "READY_TO_COMPACT",
        "reason": reason,
        "prepared_at": now(),
        "context_epoch_before": checked["context_epoch"],
        "canonical_digest": checked["canonical_digest"],
        "checkpoint_sha256": checked["checkpoint_sha256"],
        "backup_trigger": BACKUP_TRIGGER,
    }
    state["status"] = "READY_TO_COMPACT"
    state["canonical_digest"] = checked["canonical_digest"]
    state["pending_compaction"] = transaction
    state["last_error"] = None
    state["updated_at"] = transaction["prepared_at"]
    atomic_json(state_path, state)
    if read_json(state_path).get("pending_compaction", {}).get("transaction_id") != transaction["transaction_id"]:
        raise RebirthError("transaction read-back verification failed")
    return transaction


def record_backup(
    root: Path,
    status: str,
    adapter: str,
    artifact_sha256: str | None,
    remote_reference: str | None,
    error: str | None,
) -> dict[str, Any]:
    if status not in BACKUP_STATUSES:
        raise RebirthError(f"unsupported backup status: {status}")
    state_path = root / "runtime/STATE.json"
    state = read_json(state_path)
    if state.get("external_backup_sync_trigger", BACKUP_TRIGGER) != BACKUP_TRIGGER:
        raise RebirthError("backup trigger must remain EXPLICIT_COMPACT_ONLY")
    if state.get("scheduled_backup_sync", False):
        raise RebirthError("scheduled backup sync must remain disabled")
    if state.get("idle_backup_sync", False):
        raise RebirthError("idle backup sync must remain disabled")
    record = {
        "status": status,
        "adapter": adapter,
        "artifact_sha256": artifact_sha256,
        "remote_reference": remote_reference,
        "error": error,
        "recorded_at": now(),
        "sync_trigger": BACKUP_TRIGGER,
    }
    state["last_external_backup"] = record
    state["external_backup_pending"] = status == "PENDING"
    if status == "VERIFIED" and artifact_sha256:
        state["last_backup_root_hash"] = artifact_sha256
        state["last_backup_at"] = record["recorded_at"]
    state["updated_at"] = record["recorded_at"]
    atomic_json(state_path, state)
    return record


def complete(root: Path, observed: bool, method: str, signal: str) -> dict[str, Any]:
    if not observed:
        raise RebirthError("--observed is required; context epoch was not advanced")
    if method not in METHODS:
        raise RebirthError(f"unsupported compaction method: {method}")
    if signal not in SIGNALS:
        raise RebirthError(f"unsupported compaction signal: {signal}")
    checked = verify(root)
    state_path = root / "runtime/STATE.json"
    state = read_json(state_path)
    transaction = state.get("pending_compaction")
    if not isinstance(transaction, dict) or transaction.get("status") != "READY_TO_COMPACT":
        raise RebirthError("no sealed compaction transaction is ready")
    if checked["canonical_digest"] != transaction.get("canonical_digest"):
        raise RebirthError("canonical state changed after prepare; abort and prepare again")
    if checked["checkpoint_sha256"] != transaction.get("checkpoint_sha256"):
        raise RebirthError("checkpoint changed after prepare; abort and prepare again")
    finished = {
        **transaction,
        "status": "COMPLETED",
        "completed_at": now(),
        "context_epoch_after": int(state.get("context_epoch", 0)) + 1,
        "method": method,
        "success_signal": signal,
    }
    state["status"] = "ACTIVE"
    state["context_epoch"] = finished["context_epoch_after"]
    state["compaction_count"] = int(state.get("compaction_count", 0)) + 1
    state["last_compaction"] = finished
    state["pending_compaction"] = None
    state["last_error"] = None
    state["updated_at"] = finished["completed_at"]
    atomic_json(state_path, state)
    return finished


def abort(root: Path, reason: str) -> dict[str, Any]:
    state_path = root / "runtime/STATE.json"
    state = read_json(state_path)
    transaction = state.get("pending_compaction")
    if not isinstance(transaction, dict):
        raise RebirthError("no pending compaction transaction")
    record = {
        "transaction_id": transaction.get("transaction_id"),
        "status": "ABORTED",
        "reason": reason,
        "aborted_at": now(),
    }
    state["status"] = "ACTIVE"
    state["pending_compaction"] = None
    state["last_error"] = record
    state["updated_at"] = record["aborted_at"]
    atomic_json(state_path, state)
    return record


def export_snapshot(root: Path, output: Path | None) -> dict[str, str]:
    verify(root)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = (output or root.parent / f"root-engineering-rebirth-{stamp}.zip").resolve()
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if path.is_file() and "scratch" not in relative.parts and "__pycache__" not in relative.parts:
                archive.write(path, str(Path("root-engineering") / relative))
    return {"ok": True, "output": str(destination), "sha256": file_sha256(destination)}


def make_test_root(base: Path) -> Path:
    root = base / "root"
    (root / "knowledge").mkdir(parents=True)
    (root / "runtime").mkdir()
    project_id, root_id = "REP-TEST", "RR-TEST"
    atomic_text(root / "BOOT.md", "# BOOT\n")
    atomic_text(root / "ROOT.md", f"# ROOT\n- Project ID: {project_id}\n- Root ID: {root_id}\n")
    for name in ("FOUNDATION", "CURRENT", "LEARNED", "OPERATIONAL", "HISTORY"):
        atomic_text(root / "knowledge" / f"{name}.md", f"# {name}\n- Project ID: {project_id}\n- Root ID: {root_id}\n")
    atomic_text(root / "runtime/CHECKPOINT.md", f"# ACTIVE CHECKPOINT\n- Project ID: {project_id}\n- Root ID: {root_id}\n## Exact Next Action\nTest.\n## Resume Instruction\nResume.\n")
    atomic_json(root / "MANIFEST.json", {"package_version": VERSION, "status": "ACTIVE", "project_id": project_id, "root_id": root_id})
    atomic_json(root / "runtime/STATE.json", {
        "package_version": VERSION,
        "status": "ACTIVE",
        "project_id": project_id,
        "root_id": root_id,
        "context_epoch": 0,
        "compaction_count": 0,
        "checkpoint_revision": 0,
        "pending_compaction": None,
        "external_backup_sync_trigger": BACKUP_TRIGGER,
        "scheduled_backup_sync": False,
        "idle_backup_sync": False,
        "external_backup_pending": False,
        "last_external_backup": None,
    })
    atomic_json(root / "runtime/CAPABILITIES.json", {"package_version": VERSION, "project_id": project_id, "root_id": root_id, "compaction": {"native": "UNKNOWN", "zero_output_boundary": "UNKNOWN"}})
    return root


def self_test() -> dict[str, Any]:
    base = Path(tempfile.mkdtemp(prefix="rebirth-transaction-test-"))
    tests = 0
    try:
        root = make_test_root(base)
        verify(root); tests += 1
        first = prepare(root, "abort-test"); assert first["backup_trigger"] == BACKUP_TRIGGER; tests += 1
        abort(root, "expected"); tests += 1
        prepare(root, "success-test")
        done = complete(root, True, "manual-confirmation", "MANUAL_CONFIRMATION")
        assert done["context_epoch_after"] == 1; tests += 1
        prepare(root, "tamper-test")
        atomic_text(root / "runtime/CHECKPOINT.md", (root / "runtime/CHECKPOINT.md").read_text() + "changed\n")
        blocked = False
        try:
            complete(root, True, "diagnostic", "CONTEXT_REPLACEMENT_OBSERVED")
        except RebirthError as exc:
            blocked = "checkpoint changed after prepare" in str(exc)
        assert blocked; tests += 1
        abort(root, "tamper blocked")
        snapshot = export_snapshot(root, base / "snapshot.zip")
        assert Path(snapshot["output"]).is_file(); tests += 1
        pending = record_backup(root, "PENDING", "google-drive", None, None, "expected")
        assert pending["status"] == "PENDING" and verify(root)["external_backup_pending"]; tests += 1
        verified = record_backup(root, "VERIFIED", "google-drive", snapshot["sha256"], "file-id", None)
        assert verified["status"] == "VERIFIED" and not verify(root)["external_backup_pending"]; tests += 1
        state_path = root / "runtime/STATE.json"
        state = read_json(state_path); state["scheduled_backup_sync"] = True; atomic_json(state_path, state)
        try:
            verify(root)
            raise AssertionError("scheduled guard failed")
        except RebirthError as exc:
            assert "scheduled backup sync must remain disabled" in str(exc)
        tests += 1
        state["scheduled_backup_sync"] = False; state["idle_backup_sync"] = True; atomic_json(state_path, state)
        try:
            verify(root)
            raise AssertionError("idle guard failed")
        except RebirthError as exc:
            assert "idle backup sync must remain disabled" in str(exc)
        tests += 1
        assert tests == 10
        return {"ok": True, "tests": tests, "version": VERSION}
    finally:
        shutil.rmtree(base, ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify")
    sub.add_parser("self-test")
    cp = sub.add_parser("checkpoint")
    for option in ("goal", "active-work", "completed", "promoted", "unresolved", "next-action", "resume"):
        cp.add_argument("--" + option, required=True)
    prepare_parser = sub.add_parser("prepare-compact")
    prepare_parser.add_argument("--reason", required=True)
    complete_parser = sub.add_parser("complete-compact")
    complete_parser.add_argument("--observed", action="store_true")
    complete_parser.add_argument("--method", required=True)
    complete_parser.add_argument("--signal", required=True)
    abort_parser = sub.add_parser("abort-compact")
    abort_parser.add_argument("--reason", required=True)
    export_parser = sub.add_parser("export")
    export_parser.add_argument("--output", type=Path)
    backup = sub.add_parser("record-backup")
    backup.add_argument("--status", required=True)
    backup.add_argument("--adapter", required=True)
    backup.add_argument("--artifact-sha256")
    backup.add_argument("--remote-reference")
    backup.add_argument("--error")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "self-test":
            result = self_test()
        elif args.command == "verify":
            result = verify(args.root)
        elif args.command == "checkpoint":
            result = write_checkpoint(args.root, args)
        elif args.command == "prepare-compact":
            result = prepare(args.root, args.reason)
        elif args.command == "complete-compact":
            result = complete(args.root, args.observed, args.method, args.signal)
        elif args.command == "abort-compact":
            result = abort(args.root, args.reason)
        elif args.command == "export":
            result = export_snapshot(args.root, args.output)
        elif args.command == "record-backup":
            result = record_backup(args.root, args.status, args.adapter, args.artifact_sha256, args.remote_reference, args.error)
        else:
            raise RebirthError("unsupported command")
        print(json.dumps(result, ensure_ascii=False, indent=None if args.command == "self-test" else 2))
        return 0
    except (RebirthError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
