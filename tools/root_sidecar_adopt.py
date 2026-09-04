#!/usr/bin/env python3
"""Create a byte-preserving Root Engineering 1.1 `.root/` sidecar.

Dry-run is the default. Use `--apply` to activate. Existing Markdown is never
edited, moved, renamed, deleted, re-encoded, or line-ending-normalized.
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
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "1.1.0"
ROOT = ".root"
EXCLUDED = {ROOT, ".git", ".hg", ".svn", "node_modules", "__pycache__"}


class AdoptionError(RuntimeError):
    pass


@dataclass(frozen=True)
class Snapshot:
    relative_path: str
    size_bytes: int
    sha256: str
    role: str


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def excluded(path: Path, workspace: Path) -> bool:
    try:
        parts = path.relative_to(workspace).parts[:-1]
    except ValueError:
        return True
    return any(part in EXCLUDED or part.startswith(f"{ROOT}.") for part in parts)


def role(relative_path: str) -> str:
    name = Path(relative_path).name.upper()
    if "WORK_CORE" in name or "ROUTER" in name:
        return "ROUTING_CORE"
    if "PROFILE" in name or "OPERATING" in name:
        return "OPERATING_PROFILE"
    if name.startswith("WORK_"):
        return "WORK_CONTEXT"
    if any(x in name for x in ("STANDARD", "PROTOCOL", "GUIDE")):
        return "EXECUTION_STANDARD"
    if any(x in name for x in ("HANDOFF", "CHAT_SUMMARY", "STAGE_PLAN")):
        return "HANDOFF"
    if "REFERENCE" in name or "SOURCE" in name:
        return "REFERENCE"
    return "UNCLASSIFIED"


def inventory(workspace: Path) -> list[Snapshot]:
    result: list[Snapshot] = []
    for path in sorted(workspace.rglob("*"), key=lambda p: p.as_posix().lower()):
        if path.suffix.lower() != ".md" or not path.is_file() or path.is_symlink():
            continue
        if excluded(path, workspace):
            continue
        rel = path.relative_to(workspace).as_posix()
        result.append(Snapshot(rel, path.stat().st_size, digest(path), role(rel)))
    return result


def compare(before: list[Snapshot], after: list[Snapshot]) -> list[str]:
    old, new = ({x.relative_path: x for x in group} for group in (before, after))
    errors: list[str] = []
    for path in sorted(old.keys() | new.keys()):
        if path not in old:
            errors.append(f"unexpected protected Markdown appeared: {path}")
        elif path not in new:
            errors.append(f"protected Markdown missing or moved: {path}")
        else:
            if old[path].size_bytes != new[path].size_bytes:
                errors.append(f"size changed: {path}")
            if old[path].sha256 != new[path].sha256:
                errors.append(f"hash changed: {path}")
    return errors


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    try:
        with temp.open("wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def md_list(items: list[str]) -> str:
    return "\n".join(f"- `{x}`" for x in items) if items else "- NONE"


def make_files(items: list[Snapshot], project_id: str, root_id: str, timestamp: str) -> dict[str, bytes]:
    by_role: dict[str, list[str]] = {}
    for item in items:
        by_role.setdefault(item.role, []).append(item.relative_path)
    cores = by_role.get("ROUTING_CORE", [])
    default_core = cores[0] if len(cores) == 1 else ".root/ROOT.md"
    nodes = []
    for item in items:
        node = asdict(item)
        node.update(
            node_id="RN-" + hashlib.sha256(f"{root_id}\n{item.relative_path}".encode()).hexdigest()[:16].upper(),
            authority="CANONICAL_CONTENT_OWNER",
            status="ACTIVE",
            parent_route=default_core if item.role == "WORK_CONTEXT" else ".root/ROOT.md",
            direct_children=[],
        )
        nodes.append(node)
    registry = {
        "schema_version": SCHEMA,
        "project_id": project_id,
        "root_id": root_id,
        "workspace": ".",
        "preservation_mode": "BYTE_EXACT_REGISTER_IN_PLACE",
        "generated_at": timestamp,
        "nodes": nodes,
    }
    counts = Counter(x.role for x in items)
    text = {
        "BOOT.md": f"""# ROOT ENGINEERING BOOT\n\n- Schema: {SCHEMA}\n- Project ID: {project_id}\n- Root ID: {root_id}\n- Root: `.root/ROOT.md`\n- Current: `.root/knowledge/CURRENT.md`\n- Registry: `.root/runtime/CONTENT_REGISTRY.json`\n- Checkpoint: `.root/runtime/CHECKPOINT.md`\n\nRead ROOT, CURRENT, the exact routing core, and only the work owners needed.\n""",
        "ROOT.md": f"""# ROOT ENGINEERING ROOT\n\n## Identity\n- Schema: {SCHEMA}\n- Project ID: {project_id}\n- Root ID: {root_id}\n- Topology: SIDECAR_WORKSPACE\n- Generated: {timestamp}\n\n## Direct Routes\n- Foundation: `knowledge/FOUNDATION.md`\n- Current: `knowledge/CURRENT.md`\n- Learned: `knowledge/LEARNED.md`\n- Operational: `knowledge/OPERATIONAL.md`\n- History: `knowledge/HISTORY.md`\n- Registry: `runtime/CONTENT_REGISTRY.json`\n- Checkpoint: `runtime/CHECKPOINT.md`\n\n## Digest\n- Protected Markdown: {len(items)}\n- Roles: {json.dumps(dict(sorted(counts.items())), ensure_ascii=False)}\n\nDetailed truth remains in registered content owners.\n""",
        "knowledge/FOUNDATION.md": """# FOUNDATION\n\n- Preserve existing project knowledge during structural adoption.\n- Current explicit user instruction has highest project-level authority.\n- Profiles define judgment method; work nodes own project facts.\n""",
        "knowledge/CURRENT.md": f"""# CURRENT ROUTING DIGEST\n\n## Active Work Node\n- NONE\n\n## Routing Order\n`ROOT → CURRENT → ROUTING_CORE → exact WORK_CONTEXT → only required method/evidence nodes`\n\n## Routing Core\n{md_list(cores)}\n\n## Work Contexts\n{md_list(by_role.get('WORK_CONTEXT', []))}\n\n## Operating Profiles\n{md_list(by_role.get('OPERATING_PROFILE', []))}\n\n## Execution Standards\n{md_list(by_role.get('EXECUTION_STANDARD', []))}\n\n## Handoffs\n{md_list(by_role.get('HANDOFF', []))}\n\n## References\n{md_list(by_role.get('REFERENCE', []))}\n\n## Unclassified\n{md_list(by_role.get('UNCLASSIFIED', []))}\n""",
        "knowledge/LEARNED.md": "# LEARNED\n\nNo Root-level learning promoted yet.\n",
        "knowledge/OPERATIONAL.md": """# OPERATIONAL\n\n- Never alter protected Markdown during adoption.\n- Fast path: inventory → pre-hash → candidate → read-back → post-hash → activate.\n- Never replay an unchanged failed path under the same conditions.\n""",
        "knowledge/HISTORY.md": f"# HISTORY\n\n- {timestamp}: Sidecar created; existing Markdown verified by pre/post SHA-256.\n",
        "runtime/CHECKPOINT.md": """# ACTIVE CHECKPOINT\n\n## Current Goal\n- NONE\n## Active Work Node\n- NONE\n## Completed\n- Sidecar adoption verified.\n## Current State\n- Existing Markdown remains canonical at registered paths.\n## Next\n- Resolve the current workstream through the routing core.\n## Pending / Risks\n- Ambiguous role metadata may require later verification.\n## Resume Instruction\nRead ROOT, CURRENT, then only exact owners needed.\n""",
    }
    objects = {
        "MANIFEST.json": {
            "schema_version": SCHEMA, "status": "ACTIVE", "topology": "SIDECAR_WORKSPACE",
            "project_id": project_id, "root_id": root_id, "workspace_boundary": "..",
            "generated_at": timestamp, "protected_markdown_count": len(items),
            "preservation_check": "PASS", "registry": "runtime/CONTENT_REGISTRY.json",
        },
        "runtime/STATE.json": {
            "schema_version": SCHEMA, "root_revision": 1, "checkpoint_revision": 1,
            "context_epoch": 0, "active_work_node": None, "last_verified_at": timestamp,
        },
        "runtime/CAPABILITIES.json": {
            "schema_version": SCHEMA,
            "sidecar_adoption": {"status": "VERIFIED", "scope": "control-plane-only",
                                    "existing_markdown_mutation": "FORBIDDEN_DURING_ADOPTION"},
        },
        "runtime/CONTENT_REGISTRY.json": registry,
    }
    result = {path: body.encode() for path, body in text.items()}
    result.update({path: (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode() for path, obj in objects.items()})
    return result


def verify_control(root: Path, expected: dict[str, bytes], workspace: Path) -> None:
    for rel, data in expected.items():
        path = root / rel
        if not path.is_file() or path.read_bytes() != data:
            raise AdoptionError(f"control-plane read-back mismatch: {rel}")
    registry = json.loads((root / "runtime/CONTENT_REGISTRY.json").read_text())
    for node in registry["nodes"]:
        source = workspace / node["relative_path"]
        if not source.is_file() or source.stat().st_size != node["size_bytes"] or digest(source) != node["sha256"]:
            raise AdoptionError(f"registered source mismatch: {node['relative_path']}")


def adopt(workspace: Path, apply: bool) -> dict:
    workspace = workspace.expanduser().resolve()
    if not workspace.is_dir() or not os.access(workspace, os.W_OK):
        raise AdoptionError(f"workspace unavailable or not writable: {workspace}")
    active = workspace / ROOT
    if active.exists():
        raise AdoptionError("existing .root/ found; VERIFY or UPGRADE instead")
    before = inventory(workspace)
    summary = {
        "mode": "SIDECAR_WORKSPACE", "protected_markdown_files": len(before),
        "registered_roles": dict(sorted(Counter(x.role for x in before).items())),
        "preservation_policy": "PATH_SIZE_SHA256_UNCHANGED",
    }
    if not apply:
        return summary
    timestamp = now()
    project_id = "REP-" + uuid.uuid4().hex[:12].upper()
    root_id = "RR-" + uuid.uuid4().hex[:16].upper()
    expected = make_files(before, project_id, root_id, timestamp)
    candidate = workspace / f"{ROOT}.candidate-{uuid.uuid4().hex}"
    activated = False
    try:
        candidate.mkdir()
        for rel, data in expected.items():
            atomic_write(candidate / rel, data)
        verify_control(candidate, expected, workspace)
        errors = compare(before, inventory(workspace))
        if errors:
            raise AdoptionError("; ".join(errors))
        os.replace(candidate, active)
        activated = True
        verify_control(active, expected, workspace)
        errors = compare(before, inventory(workspace))
        if errors:
            raise AdoptionError("post-activation mismatch: " + "; ".join(errors))
    except Exception:
        if candidate.exists():
            shutil.rmtree(candidate, ignore_errors=True)
        if activated and active.exists():
            # This transaction created the sidecar. Remove only that new
            # control plane so a failed final verification cannot appear ACTIVE.
            shutil.rmtree(active, ignore_errors=True)
        raise
    summary.update(
        root=str(active), project_id=project_id, root_id=root_id,
        preservation_check=f"{len(before)}/{len(before)} path-size-hash unchanged",
        acceptance_routing="PASS",
        unclassified_files=sum(x.role == "UNCLASSIFIED" for x in before),
    )
    return summary


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="root-sidecar-selftest-") as temp:
        workspace = Path(temp)
        samples = {
            "PROJECT_PROFILE.md": b"# Profile\r\n\r\nExact CRLF.\r\n",
            "PROJECT_WORK_CORE.md": b"# Router\n",
            "PROJECT_STANDARD.md": b"\xef\xbb\xbf# Standard\n",
            "WORK_ALPHA.md": b"# Alpha\n",
            "WORK_BETA.MD": b"# Beta\n",
            "ALPHA_HANDOFF.md": b"# Handoff\n",
            "notes/reference.md": b"# Reference\n",
        }
        for rel, data in samples.items():
            path = workspace / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        result = adopt(workspace, True)
        if any((workspace / rel).read_bytes() != data for rel, data in samples.items()):
            raise AssertionError("source bytes changed")
        registry = json.loads((workspace / ROOT / "runtime/CONTENT_REGISTRY.json").read_text())
        roles = {x["relative_path"]: x["role"] for x in registry["nodes"]}
        expected = {
            "PROJECT_PROFILE.md": "OPERATING_PROFILE", "PROJECT_WORK_CORE.md": "ROUTING_CORE",
            "PROJECT_STANDARD.md": "EXECUTION_STANDARD", "WORK_ALPHA.md": "WORK_CONTEXT",
            "WORK_BETA.MD": "WORK_CONTEXT", "ALPHA_HANDOFF.md": "HANDOFF",
            "notes/reference.md": "REFERENCE",
        }
        if roles != expected or result["acceptance_routing"] != "PASS":
            raise AssertionError(f"routing mismatch: {roles}")
        print("ROOT_SIDECAR_SELF_TEST_PASS")
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", nargs="?", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv or sys.argv[1:])
    try:
        if args.self_test:
            self_test()
        elif args.workspace is None:
            raise AdoptionError("workspace is required unless --self-test is used")
        else:
            print(json.dumps(adopt(args.workspace, args.apply), ensure_ascii=False, indent=2))
        return 0
    except (AdoptionError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
