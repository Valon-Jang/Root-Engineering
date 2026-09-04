from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "installer" / "rebirth" / "runtime" / "rebirth_transaction.py"
SKILL = ROOT / "installer" / "rebirth" / "root-engineering" / "SKILL.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


if not RUNTIME.is_file():
    fail(f"missing runtime: {RUNTIME}")
if not SKILL.is_file():
    fail(f"missing Skill: {SKILL}")

source = RUNTIME.read_text(encoding="utf-8")
skill = SKILL.read_text(encoding="utf-8")
ast.parse(source, filename=str(RUNTIME))

required_runtime = [
    'VERSION = "1.0.0"',
    "METHODS = (",
    "SIGNALS = (",
    "pending_compaction",
    "canonical_digest",
    "checkpoint_sha256",
    "manifest package version mismatch",
    "runtime state is not ACTIVE",
    "--observed is required",
    "unsupported compaction method",
    "unsupported compaction signal",
    "canonical state changed after prepare",
    "checkpoint changed after prepare",
    "def export_snapshot",
]
required_skill = [
    "Persist → Checkpoint → Verify → Compact → Rehydrate",
    "현재 작업을 저장 중입니다…",
    "저장 완료. 대화를 압축 중입니다…",
    "압축 완료. 이어서 진행할게.",
    "Save failure = no compact",
    "Never invent or call a private/internal RPC",
]
for token in required_runtime:
    if token not in source:
        fail(f"runtime token missing: {token}")
for token in required_skill:
    if token not in skill:
        fail(f"Skill token missing: {token}")

forbidden = [
    "thread/compact/start RPC >",
    "Google Drive is required",
    "Project Instructions must",
]
for token in forbidden:
    if token in source or token in skill:
        fail(f"forbidden token present: {token}")

completed = subprocess.run(
    [sys.executable, str(RUNTIME), "self-test"],
    check=False,
    capture_output=True,
    text=True,
)
if completed.returncode != 0:
    print(completed.stdout)
    print(completed.stderr, file=sys.stderr)
    fail("runtime self-test failed")

try:
    result = json.loads(completed.stdout)
except json.JSONDecodeError as exc:
    fail(f"self-test output is not JSON: {exc}")
if result != {"ok": True, "tests": 7, "version": "1.0.0"}:
    fail(f"unexpected self-test result: {result}")

print("REBIRTH_RUNTIME_VALIDATION_PASS")
print(f"runtime_bytes={RUNTIME.stat().st_size}")
print(f"self_tests={result['tests']}")
