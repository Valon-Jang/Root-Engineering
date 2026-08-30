# Root Engineering — Codex Installer

This package installs Root Engineering as a reusable Codex Skill and then connects it to one repository or workspace through project-local `.root/` files and a small `AGENTS.md` block.

It does not require Google Drive, does not replace existing project instructions, and does not create a global cross-project knowledge database.

## 1. Install the Skill

In Codex, send this prompt:

```text
$skill-installer install the skill from https://github.com/Valon-Jang/Root-Engineering/tree/main/installer/codex/root-engineering
```

The built-in installer downloads the folder that contains `SKILL.md` and places it in the active Codex profile's Skill directory. The Skill becomes available on the next turn; if it does not appear, start a fresh Codex session.

For repository-scoped use without a user-level installation, copy the `installer/codex/root-engineering` folder to:

```text
<repository>/.agents/skills/root-engineering
```

## 2. Initialize One Project

Open the intended repository or workspace in Codex, then send:

```text
Use $root-engineering to initialize Root Engineering in this project and run the bundled validation. Preserve all existing AGENTS.md content.
```

The Skill creates this project-local structure only when it is absent:

```text
<project>/
├── AGENTS.md
└── .root/
    ├── ROOT.md
    ├── FOUNDATION.md
    ├── CURRENT.md
    ├── LEARNED.md
    ├── HISTORY.md
    └── nodes/
        └── OPERATIONAL_MEMORY.md
```

The initializer stages the complete Root before publishing it, refuses partial or invalid existing Roots, rejects symlinked targets, and appends one marked Root Engineering block to `AGENTS.md` without replacing existing bytes.

## 3. Verify in a Fresh Codex Session

Start a new Codex session from the initialized project and send:

```text
Use $root-engineering to identify this project's Root, read only the route needed for the current state, and report any unresolved fresh-session acceptance item without changing it.
```

Acceptance passes when Codex:

- discovers the `root-engineering` Skill
- loads the applicable project `AGENTS.md`
- resolves the current checkout's `.root/ROOT.md`
- follows the exact route to `.root/CURRENT.md`
- does not load unrelated Root nodes
- reports the fresh-session result as evidence rather than assuming success

After the check passes, ask Codex to replace the corresponding unresolved item in `.root/CURRENT.md` with the observed result.

## 4. Direct Tool Commands

The Skill includes a PowerShell tool with no third-party modules. Codex normally runs it for you.

```text
pwsh -File <skill-directory>/scripts/root_engineering.ps1 init -ProjectRoot <project-root>
pwsh -File <skill-directory>/scripts/root_engineering.ps1 validate -ProjectRoot <project-root>
pwsh -File <skill-directory>/scripts/root_engineering.ps1 validate-package
pwsh -File <skill-directory>/scripts/root_engineering.ps1 self-test
```

On Windows PowerShell, use the reviewed canonical script with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File` if the machine blocks direct script-file execution. The bypass applies only to that process; do not change the persistent machine policy. If PowerShell is unavailable, Codex can create the same files from the bundled templates with guarded file patches. It must not overwrite an existing Root or existing `AGENTS.md` content.

## 5. Safety and Scope

- Install the Skill only from the canonical repository path shown above.
- Review `SKILL.md` and `references/PROTOCOL.md` before adapting the package.
- Root routes do not grant filesystem access, approval, trust, or authority.
- Never place credentials, secrets, tokens, private keys, `.env` content, or raw authentication material in a Root.
- Treat `.root/` as checkout-local in Git worktrees.
- Do not claim installation success from static inspection alone; run project validation and a fresh Codex session check.

## Package Contents

```text
installer/codex/root-engineering/
├── SKILL.md
├── agents/openai.yaml
├── references/PROTOCOL.md
├── scripts/root_engineering.ps1
└── assets/templates/
```

Source: https://github.com/Valon-Jang/Root-Engineering  
License: [Creative Commons Attribution 4.0 International](../LICENSE)
