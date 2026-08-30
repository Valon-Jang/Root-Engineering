from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
INSTALLER = ROOT / "installer/ROOT_ENGINEERING_CLAUDE_INSTALLER.md"
PKG = ROOT / "installer/claude/root-engineering"
SKILL = PKG / "SKILL.md"
PROTOCOL = PKG / "references/PROTOCOL.md"
CURRENT = PKG / "assets/templates/CURRENT.md"
VALIDATOR = ROOT / "tools/validate_claude_installer.py"
VALIDATOR_WF = ROOT / ".github/workflows/validate-claude-installer.yml"

EMBED_FILES = [
    "SKILL.md",
    "references/PROTOCOL.md",
    "assets/templates/ROOT.md",
    "assets/templates/FOUNDATION.md",
    "assets/templates/CURRENT.md",
    "assets/templates/LEARNED.md",
    "assets/templates/OPERATIONAL_MEMORY.md",
    "assets/templates/HISTORY.md",
    "assets/templates/INSTRUCTIONS_BLOCK.md",
]


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected 1 match, got {n}")
    return text.replace(old, new, 1)


def insert_once(text, anchor, payload, label):
    if payload in text:
        return text
    return replace_once(text, anchor, payload + "\n\n" + anchor, label)

# README: make the installation ownership/linkage explicit.
s = README.read_text(encoding="utf-8")
anchor = "The Claude package keeps the Codex project-local Markdown model but stores nodes as plain `.md` files in a Drive project folder."
linkage = (
    "The top-level Claude installer is the **self-contained installation source**. It embeds the exact protocol, project-instruction block, and node templates needed for installation. "
    "The files under `installer/claude/root-engineering/` are the maintained mirror/reference package, not an additional attachment requirement. "
    "Repository CI verifies that the embedded installer payload and those mirror files stay identical."
)
if linkage not in s:
    s = replace_once(s, anchor, linkage + "\n\n" + anchor, "README Claude linkage")
README.write_text(s, encoding="utf-8")

# CURRENT: do not claim that the project-instruction binding already happened during file initialization.
s = CURRENT.read_text(encoding="utf-8")ns_old = "- `Fact`: Root Engineering was initialized on {{DATE}} with Drive-hosted Markdown nodes and a Claude project-instruction connection block."
ns_new = "- `Fact`: Drive-hosted Root Engineering Markdown nodes were initialized on {{DATE}}."
if ns_old in s:
    s = replace_once(s, ns_old, ns_new, "CURRENT premature binding fact")
old_accept = "- `Unresolved`: Run a fresh-chat acceptance check after initialization and replace this item with observed evidence."
new_accept = "- `Unresolved`: Confirm the Project instruction connection block is present, then run the fresh-chat binding acceptance check and replace this item only with observed evidence."
if old_accept in s:
    s = replace_once(s, old_accept, new_accept, "CURRENT acceptance state")
CURRENT.write_text(s, encoding="utf-8")

# SKILL: explicitly connect runtime mirror to the self-contained installer.
s = SKILL.read_text(encoding="utf-8")
link_section = """## Package linkage

The top-level Claude installer is the self-contained installation source. It embeds the protocol, instruction block, and node templates required to initialize a project without relying on these repository files being separately loaded at install time.

This `SKILL.md`, `references/PROTOCOL.md`, and `assets/templates/*` directory is the maintained mirror/reference package. Repository validation must fail if an embedded installer payload differs from its mirror. Runtime behavior after installation comes from the Project instruction block plus the bound Root files; do not assume this repository checkout remains in context.
"""
s = insert_once(s, "## Resolve the active Root", link_section.rstrip(), "SKILL package linkage")
SKILL.write_text(s, encoding="utf-8")

# PROTOCOL: split installation acceptance from later runtime transaction invariants.
s = PROTOCOL.read_text(encoding="utf-8")
head = "## 13. Acceptance criteria"
pos = s.find(head)
if pos < 0:
    raise RuntimeError("PROTOCOL acceptance heading missing")
new_acceptance = """## 13. Acceptance criteria

### 13.1 Installation acceptance

A Claude installation is accepted only when both the installer preflight and a fresh-session binding check pass.

The preflight must prove the storage operations the installed Root will actually depend on, using temporary data and read-back rather than capability-name assumptions.

The fresh-session binding check must demonstrate:

- the project instructions contain exactly one complete Root Engineering marker pair
- a fresh chat in the same Project resolves the bound folder and reads `ROOT.md` without the installer attached
- the exact route to `CURRENT.md` resolves and only decision-relevant routed nodes are loaded
- the Operational Memory route declared by `ROOT.md` resolves to its canonical owner
- the observed fresh-session result is reported as evidence rather than assumed from static inspection
- the unresolved acceptance item in `CURRENT.md` is changed only after the observed fresh-session check passes
- multiple projects remain isolated and sensitive material is rejected

A static repository inspection, generated instruction block, or successful file creation alone is not installation acceptance.

### 13.2 Runtime transaction invariants

The following are runtime guarantees and must be verified whenever their paths are exercised; they are not additional hidden prerequisites for the fresh-session binding check:

- a durable update reaches one canonical owner and increments its revision
- a stale update is detected by the pre-write re-read and re-merged instead of overwriting silently
- an update interrupted before supersession cleanup leaves the previous canonical node intact and resolvable
- repeated work retrieves its exact operational record before implementation
- a matching verified fast path is selected without replaying its failed path
- the first new failure remains visible, while unchanged same-path retry is prevented
- blocked, static-only, installation-only, or restart-pending evidence is not promoted to verified success
- no token, quality, or latency improvement is claimed without a matched fresh-run benchmark
"""
s = s[:pos] + new_acceptance.rstrip() + "\n"
PROTOCOL.write_text(s, encoding="utf-8")

# INSTALLER: declare self-contained bootstrap and align fresh-chat acceptance wording.
s = INSTALLER.read_text(encoding="utf-8")
bootstrap = """## Package Bootstrap Contract

This top-level installer is the complete installation input. It contains an embedded canonical copy of the protocol, Project instruction block, and every node template required by the installation flow.

- Do not invent a missing template or reconstruct one from memory.
- Do not require the user to attach the lower package files separately.
- The lower `installer/claude/root-engineering/` files are maintenance mirrors and references. When repository access exists they may be cross-checked, but installation must not depend on them being separately loaded.
- The embedded payloads and mirror files are required to remain identical; repository validation enforces this connection.
"""
s = insert_once(s, "## 1. Connect Google Drive", bootstrap.rstrip(), "installer bootstrap contract")

old_fresh = """Acceptance passes when Claude:

- resolves the project folder from the instruction block
- reads `ROOT.md` from that folder
- follows the exact route to `CURRENT.md`
- does not load unrelated Root nodes
- reports the fresh-session result as evidence rather than assuming success

After the check passes, ask Claude to replace the corresponding unresolved item in `CURRENT.md` with the observed result."""
new_fresh = """Before declaring the installation accepted, require **both** the Section 5 preflight and this fresh-session binding check.

The fresh-session binding check passes when Claude:

- resolves the project folder from the instruction block
- reads `ROOT.md` from that folder without relying on this installer being attached
- follows the exact route to `CURRENT.md`
- resolves the Operational Memory route declared by `ROOT.md`
- does not load unrelated Root nodes
- reports the fresh-session result as evidence rather than assuming success

After the check passes, ask Claude to replace the corresponding unresolved acceptance item in `CURRENT.md` with the observed result. Do not mark that item complete from static inspection or from initialization alone."""
if old_fresh in s:
    s = replace_once(s, old_fresh, new_fresh, "installer fresh acceptance")
elif new_fresh not in s:
    raise RuntimeError("installer fresh acceptance block not found")

# Replace or append the embedded canonical payloads from the maintained mirror files.
start = "<!-- ROOT_ENGINEERING_EMBEDDED_PAYLOADS_START -->"
end = "<!-- ROOT_ENGINEERING_EMBEDDED_PAYLOADS_END -->"
blocks = [start, "## Embedded Canonical Payloads", "", "These payloads are the exact installation source. They are generated from and CI-checked against the maintained mirror package.", ""]
for rel in EMBED_FILES:
    body = (PKG / rel).read_text(encoding="utf-8").rstrip("\n")
    blocks += [
        f"<!-- ROOT_ENGINEERING_EMBED_START:{rel} -->",
        "````markdown",
        body,
        "````",
        f"<!-- ROOT_ENGINEERING_EMBED_END:{rel} -->",
        "",
    ]
blocks.append(end)
embedded = "\n".join(blocks).rstrip()
if start in s:
    a = s.index(start)
    b = s.index(end, a) + len(end)
    s = s[:a] + embedded + s[b:]
else:
    s = insert_once(s, "## Package Contents", embedded, "installer embedded payloads")
INSTALLER.write_text(s, encoding="utf-8")

validator = r'''from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
INSTALLER = ROOT / "installer/ROOT_ENGINEERING_CLAUDE_INSTALLER.md"
PKG = ROOT / "installer/claude/root-engineering"

EMBED_FILES = [
    "SKILL.md",
    "references/PROTOCOL.md",
    "assets/templates/ROOT.md",
    "assets/templates/FOUNDATION.md",
    "assets/templates/CURRENT.md",
    "assets/templates/LEARNED.md",
    "assets/templates/OPERATIONAL_MEMORY.md",
    "assets/templates/HISTORY.md",
    "assets/templates/INSTRUCTIONS_BLOCK.md",
]

errors = []

def need(cond, msg):
    if not cond:
        errors.append(msg)

readme = README.read_text(encoding="utf-8")
installer = INSTALLER.read_text(encoding="utf-8")
need("self-contained installation source" in readme, "README does not identify the Claude installer as self-contained")
need("## Package Bootstrap Contract" in installer, "Claude installer bootstrap contract missing")
need("Do not require the user to attach the lower package files separately." in installer, "installer lower-package independence missing")
need("both** the Section 5 preflight and this fresh-session binding check" in installer, "installer acceptance linkage missing")

for rel in EMBED_FILES:
    path = PKG / rel
    need(path.exists(), f"missing mirror file: {rel}")
    if not path.exists():
        continue
    sm = f"<!-- ROOT_ENGINEERING_EMBED_START:{rel} -->"
    em = f"<!-- ROOT_ENGINEERING_EMBED_END:{rel} -->"
    need(installer.count(sm) == 1 and installer.count(em) == 1, f"embedded markers invalid for {rel}")
    if installer.count(sm) == 1 and installer.count(em) == 1:
        chunk = installer.split(sm, 1)[1].split(em, 1)[0].strip()
        if not (chunk.startswith("````markdown") and chunk.endswith("````")):
            errors.append(f"embedded fence invalid for {rel}")
        else:
            body = chunk[len("````markdown"): -len("````")].strip("\n")
            mirror = path.read_text(encoding="utf-8").strip("\n")
            need(body == mirror, f"embedded payload drift: {rel}")

current = (PKG / "assets/templates/CURRENT.md").read_text(encoding="utf-8")
need("with Drive-hosted Markdown nodes and a Claude project-instruction connection block" not in current, "CURRENT prematurely claims instruction binding")
need("fresh-chat binding acceptance check" in current, "CURRENT acceptance unresolved item missing")

protocol = (PKG / "references/PROTOCOL.md").read_text(encoding="utf-8")
need("### 13.1 Installation acceptance" in protocol, "Protocol installation acceptance missing")
need("### 13.2 Runtime transaction invariants" in protocol, "Protocol runtime invariant split missing")
need("Operational Memory route declared by `ROOT.md`" in protocol, "Protocol acceptance does not check Operational Memory route")

skill = (PKG / "SKILL.md").read_text(encoding="utf-8")
need("## Package linkage" in skill, "SKILL package linkage missing")
need("do not assume this repository checkout remains in context" in skill, "SKILL runtime independence missing")

root_t = (PKG / "assets/templates/ROOT.md").read_text(encoding="utf-8")
for required in ["FOUNDATION.md", "CURRENT.md", "LEARNED.md", "nodes/OPERATIONAL_MEMORY.md", "HISTORY.md"]:
    need(required in root_t, f"ROOT template route missing: {required}")

instr = (PKG / "assets/templates/INSTRUCTIONS_BLOCK.md").read_text(encoding="utf-8")
need(instr.count("<!-- ROOT_ENGINEERING_START -->") == 1, "instruction start marker count invalid")
need(instr.count("<!-- ROOT_ENGINEERING_END -->") == 1, "instruction end marker count invalid")

for rel in ["ROOT.md", "FOUNDATION.md", "CURRENT.md", "LEARNED.md", "OPERATIONAL_MEMORY.md", "HISTORY.md"]:
    p = PKG / "assets/templates" / rel
    need(p.read_text(encoding="utf-8").startswith("<!-- ROOT_REVISION: 1 -->"), f"ROOT_REVISION missing: {rel}")

if errors:
    print("Claude installer validation FAILED")
    for e in errors:
        print("-", e)
    raise SystemExit(1)
print("Claude installer validation PASS")
'''
VALIDATOR.write_text(validator, encoding="utf-8")

workflow = '''name: Validate Claude installer

on:
  push:
    branches: [main]
    paths:
      - README.md
      - installer/ROOT_ENGINEERING_CLAUDE_INSTALLER.md
      - installer/claude/root-engineering/**
      - tools/validate_claude_installer.py
      - .github/workflows/validate-claude-installer.yml
  pull_request:
    paths:
      - README.md
      - installer/ROOT_ENGINEERING_CLAUDE_INSTALLER.md
      - installer/claude/root-engineering/**
      - tools/validate_claude_installer.py
      - .github/workflows/validate-claude-installer.yml

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Claude installer package linkage
        run: python tools/validate_claude_installer.py
'''
VALIDATOR_WF.write_text(workflow, encoding="utf-8")

print("Claude package connectivity repair generated")
