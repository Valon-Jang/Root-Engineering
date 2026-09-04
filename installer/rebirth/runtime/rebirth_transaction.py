#!/usr/bin/env python3
"""Root Engineering 1.0 — Rebirth transaction guard.

This helper does not compact ChatGPT. It atomically checkpoints project state,
seals the state that may be compacted, and advances the context epoch only
after the host's compaction is explicitly observed.
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
METHODS = ("native", "zero-output-boundary", "manual-confirmation", "diagnostic")
SIGNALS = ("HOST_EVENT", "CONTEXT_REPLACEMENT_OBSERVED", "MANUAL_CONFIRMATION")


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_digest(root: Path) -> tuple[str, dict[str, str]]:
    hashes: dict[str, str] = {}
    aggregate = hashlib.sha256()
    for relative in CANONICAL:
        path = root / relative
        if not path.is_file():
            raise RebirthError(f"missing canonical file: {relative}")
        item_hash = sha256(path)
        hashes[relative] = item_hash
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(item_hash.encode("ascii"))
        aggregate.update(b"\n")
    return aggregate.hexdigest(), hashes


def verify(root: Path) -> dict[str, Any]:
    root = root.resolve()
    missing = [item for item in REQUIRED if not (root / item).is_file()]
    if missing:
        raise RebirthError("missing required paths: " + ", ".join(missing))

    manifest = read_json(root / "MANIFEST.json")
    state = read_json(root / "runtime/STATE.json")
    capabilities = read_json(root / "runtime/CAPABILITIES.json")
    project_id = manifest.get("project_id")
    root_id = manifest.get("root_id")
    if not project_id or not root_id:
        raise RebirthError("manifest identity is incomplete")
    if manifest.get("package_version") != VERSION:
        raise RebirthError("manifest package version mismatch")
    if manifest.get("status") != "ACTIVE":
        raise RebirthError("manifest is not ACTIVE")
    state_version = state.get("package_version")
    if state_version is not None and state_version != VERSION:
        raise RebirthError("state package version mismatch")

    for label, record in (("state", state), ("capabilities", capabilities)):
        for key, expected in (("project_id", project_id), ("root_id", root_id)):
            actual = record.get(key)
            if actual is not None and actual != expected:
                raise RebirthError(f"{label} identity mismatch: {key}")

    for relative in ("ROOT.md",) + CANONICAL[1:]:
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
        "pending_compaction": state.get("pending_compaction"),
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
    required_values = (
        args.goal,
        args.active_work,
        args.completed,
        args.promoted,
        args.unresolved,
        args.next_action,
        args.resume,
    )
    if any(not value.strip() for value in required_values):
        raise RebirthError("checkpoint fields must not be blank")

    text = checkpoint_text(checked, checked["context_epoch"], args)
    path = root / "runtime/CHECKPOINT.md"
    atomic_text(path, text)
    expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if sha256(path) != expected:
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
    if state.get("status", "ACTIVE") != "ACTIVE":
        raise RebirthError("runtime state is not ACTIVE")
    checkpoint_path = root / "runtime/CHECKPOINT.md"
    transaction = {
        "transaction_id": "RB-" + uuid.uuid4().hex[:12].upper(),
        "status": "READY_TO_COMPACT",
        "reason": reason,
        "prepared_at": now(),
        "context_epoch_before": checked["context_epoch"],
        "canonical_digest": checked["canonical_digest"],
        "checkpoint_sha256": sha256(checkpoint_path),
    }
    state["status"] = "READY_TO_COMPACT"
    state["canonical_digest"] = checked["canonical_digest"]
    state["pending_compaction"] = transaction
    state["last_error"] = None
    state["updated_at"] = transaction["prepared_at"]
    atomic_json(state_path, state)
    reread = read_json(state_path).get("pending_compaction", {})
    if reread.get("transaction_id") != transaction["transaction_id"]:
        raise RebirthError("transaction read-back verification failed")
    return transaction


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
    checkpoint_hash = sha256(root / "runtime/CHECKPOINT.md")
    if checkpoint_hash != transaction.get("checkpoint_sha256"):
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

    capabilities_path = root / "runtime/CAPABILITIES.json"
    capabilities = read_json(capabilities_path)
    capabilities.setdefault("compaction", {})
    capabilities["compaction"].update(
        {"last_verified_method": method, "success_signal": signal, "last_verified_at": finished["completed_at"]}
    )
    capabilities["updated_at"] = finished["completed_at"]
    atomic_json(capabilities_path, capabilities)
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
    return {"ok": True, "output": str(destination), "sha256": sha256(destination)}


def self_test() -> dict[str, Any]:
    base = Path(tempfile.mkdtemp(prefix="rebirth-transaction-test-"))
    try:
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
        atomic_json(root / "runtime/STATE.json", {"package_version": VERSION, "status": "ACTIVE", "project_id": project_id, "root_id": root_id, "context_epoch": 0, "compaction_count": 0, "checkpoint_revision": 0, "pending_compaction": None})
        atomic_json(root / "runtime/CAPABILITIES.json", {"package_version": VERSION, "project_id": project_id, "root_id": root_id, "compaction": {"native": "UNKNOWN", "zero_output_boundary": "UNKNOWN"}})
        verify(root)
        prepare(root, "self-test")
        abort(root, "expected")
        prepare(root, "self-test-success")
        done = complete(root, True, "manual-confirmation", "MANUAL_CONFIRMATION")
        assert done["context_epoch_after"] == 1
        prepare(root, "tamper-test")
        atomic_text(root / "runtime/CHECKPOINT.md", (root / "runtime/CHECKPOINT.md").read_text() + "\nchanged\n")
        blocked = False
        try:
            complete(root, True, "diagnostic", "CONTEXT_REPLACEMENT_OBSERVED")
        except RebirthError:
            blocked = True
        assert blocked
        abort(root, "tamper correctly blocked")
        snapshot = export_snapshot(root, base / "snapshot.zip")
        assert Path(snapshot["output"]).is_file()
        return {"ok": True, "tests": 7, "version": VERSION}
    finally:
        shutil.rmtree(base)


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    commands = cli.add_subparsers(dest="command", required=True)
    commands.add_parser("verify")
    commands.add_parser("status")
    cp = commands.add_parser("checkpoint")
    for flag in ("goal", "active-work", "completed", "promoted", "unresolved", "next-action", "resume"):
        cp.add_argument("--" + flag, required=True)
    prep = commands.add_parser("prepare-compact")
    prep.add_argument("--reason", default="user-requested")
    done = commands.add_parser("complete-compact")
    done.add_argument("--observed", action="store_true")
    done.add_argument("--method", choices=METHODS, required=True)
    done.add_argument("--signal", choices=SIGNALS, required=True)
    stop = commands.add_parser("abort-compact")
    stop.add_argument("--reason", required=True)
    out = commands.add_parser("export")
    out.add_argument("--output", type=Path)
    commands.add_parser("self-test")
    return cli


def main() -> int:
    args = parser().parse_args()
    root = args.root.resolve()
    try:
        if args.command == "verify":
            result = verify(root)
        elif args.command == "status":
            result = {"verify": verify(root), "state": read_json(root / "runtime/STATE.json")}
        elif args.command == "checkpoint":
            result = write_checkpoint(root, args)
        elif args.command == "prepare-compact":
            result = prepare(root, args.reason)
        elif args.command == "complete-compact":
            result = complete(root, args.observed, args.method, args.signal)
        elif args.command == "abort-compact":
            result = abort(root, args.reason)
        elif args.command == "export":
            result = export_snapshot(root, args.output)
        elif args.command == "self-test":
            result = self_test()
        else:
            raise RebirthError("unsupported command")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except RebirthError as exc:
        print(f"REBIRTH_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
