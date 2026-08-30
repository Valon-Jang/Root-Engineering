<!-- ROOT_REVISION: 1 -->
# Current Knowledge

## Confirmed facts

- `Fact`: {{PROJECT_NAME}} is the selected project for this checkout.
- `Fact`: Root Engineering was initialized on {{DATE}} with project-local Markdown and a Codex `AGENTS.md` connection block.

## Active decisions

- `Decision`: `.root/ROOT.md` and its routed nodes are the canonical durable project-knowledge tree.
- `Decision`: `.root/nodes/OPERATIONAL_MEMORY.md` owns repeated-operation failure patterns, preferred paths, and required evidence.
- `Decision`: Detailed knowledge remains on disk; context cost is controlled through route- and section-level retrieval.

## Current constraints

- Current explicit instructions outrank stored Root knowledge.
- Root updates preserve scope, authority, conditions, exceptions, provenance, and unresolved issues.
- Concurrent or stale edits are re-read and merged instead of overwritten blindly.
- `.root/` is checkout-local in Git worktrees.

## Unresolved

- `Unresolved`: Confirm and record the project's current state, active goals, and next meaningful action from authoritative sources.
- `Unresolved`: Run a fresh Codex acceptance check after initialization and replace this item with observed evidence.

## Provenance

- Root Engineering Codex initializer, {{DATE}}.
