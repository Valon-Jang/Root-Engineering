#!/usr/bin/env python3
"""Validate the staged Root Engineering 1.1 Sidecar Work Graph package."""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
from pathlib import Path

REQUIRED_ENGLISH = {
    "package_version: 1.1.0",
    "status: staged-next-version",
    "control_plane_path: .root",
    "existing_markdown_adoption: byte-exact-register-in-place",
    "Root → Core → exact Work Context",
    "Any protected Markdown mismatch = adoption failure.",
    "tools/root_sidecar_adopt.py",
}

REQUIRED_KOREAN = {
    "package_version: 1.1.0",
    "status: staged-next-version",
    "control_plane_path: .root",
    "existing_markdown_adoption: byte-exact-register-in-place",
    "Root → Core → 정확한 Work Context",
    "보호대상 Markdown 불일치 1건이라도 있으면 Adoption 실패다.",
    "tools/root_sidecar_adopt.py",
}

FORBIDDEN_SPECIALIZED_TOKENS = {
    "BMW",
    "4695",
    "46100",
    "46120",
    "SP310",
    "2P_WORK_CORE",
    "2P_PART_LEADER",
}


def require_tokens(text: str, required: set[str], label: str) -> None:
    missing = sorted(token for token in required if token not in text)
    if missing:
        raise AssertionError(f"{label} missing required tokens: {missing}")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    english_path = repo / "installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_v1.1.0.md"
    korean_path = repo / "installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_v1.1.0_KO.md"
    release_path = repo / "docs/releases/v1.1.0-sidecar-work-graph.md"
    staged_path = repo / "installer/LATEST_STAGED.json"
    next_version_path = repo / "NEXT_VERSION"
    tool_path = repo / "tools/root_sidecar_adopt.py"

    for path in (english_path, korean_path, release_path, staged_path, next_version_path, tool_path):
        if not path.is_file():
            raise AssertionError(f"required file missing: {path.relative_to(repo)}")

    english = english_path.read_text(encoding="utf-8")
    korean = korean_path.read_text(encoding="utf-8")
    release = release_path.read_text(encoding="utf-8")
    staged = json.loads(staged_path.read_text(encoding="utf-8"))
    next_version = next_version_path.read_text(encoding="utf-8").splitlines()

    require_tokens(english, REQUIRED_ENGLISH, "English installer")
    require_tokens(korean, REQUIRED_KOREAN, "Korean installer")

    combined_installers = english + "\n" + korean
    leaked = sorted(token for token in FORBIDDEN_SPECIALIZED_TOKENS if token in combined_installers)
    if leaked:
        raise AssertionError(f"project-specialized tokens leaked into generic installer: {leaked}")

    if staged.get("version") != "1.1.0":
        raise AssertionError("LATEST_STAGED.json version mismatch")
    if staged.get("status") != "staged-next-version":
        raise AssertionError("LATEST_STAGED.json status mismatch")
    if staged.get("existing_markdown_policy") != "byte-exact-register-in-place":
        raise AssertionError("LATEST_STAGED.json preservation policy mismatch")

    expected_next_version = [
        "1.1.0",
        "Rebirth",
        "Sidecar Work Graph",
        "status=staged-next-version",
    ]
    if next_version != expected_next_version:
        raise AssertionError(f"NEXT_VERSION mismatch: {next_version!r}")

    if "pre/post SHA-256" not in release:
        raise AssertionError("release notes do not state pre/post SHA-256 preservation")

    py_compile.compile(str(tool_path), doraise=True)
    completed = subprocess.run(
        [sys.executable, str(tool_path), "--self-test"],
        cwd=repo,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "sidecar self-test failed\nSTDOUT:\n"
            + completed.stdout
            + "\nSTDERR:\n"
            + completed.stderr
        )
    if "ROOT_SIDECAR_SELF_TEST_PASS" not in completed.stdout:
        raise AssertionError("sidecar self-test did not emit PASS marker")
    if "ROOT_SIDECAR_FAIL_CLOSED_TEST_PASS" not in completed.stdout:
        raise AssertionError("sidecar fail-closed test did not emit PASS marker")

    print("VALIDATE_ROOT_ENGINEERING_V1_1_0_PASS")
    print(completed.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
