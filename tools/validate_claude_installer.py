from pathlib import Path

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
