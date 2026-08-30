<!-- ROOT_REVISION: 1 -->
# {{PROJECT_NAME}} Root

This is the canonical map and digest for durable project knowledge. Navigate it; do not load every node by default.

## Identity

- Project: {{PROJECT_NAME}}
- Physical Root: this checkout's `.root/`
- Storage: project-local Markdown
- Context policy: selective routed reads
- Knowledge Lookup coverage: COMPLETE
- Initialized: {{DATE}}

## Digest

- Purpose and durable boundaries: `.root/FOUNDATION.md`
- Current accepted state, active decisions, and unresolved items: `.root/CURRENT.md`
- Verified reusable methods and failure lessons: `.root/LEARNED.md`
- Repeated-operation failures, preferred paths, and mandatory evidence: `.root/nodes/OPERATIONAL_MEMORY.md`
- Superseded states and migration history: `.root/HISTORY.md`
- Specialist owners: `.root/nodes/`, created only when retrieval patterns justify them

## Routing map

| Node | Read when | Parent | Role | Source of Truth | State |
| --- | --- | --- | --- | --- | --- |
| `.root/FOUNDATION.md` | Purpose, human intent, stable principles, boundaries, or success criteria matter | `.root/ROOT.md` | Foundation owner | Yes | ACTIVE |
| `.root/CURRENT.md` | Present state, active decisions, constraints, dependencies, or unresolved issues matter | `.root/ROOT.md` | Current-state owner | Yes | ACTIVE |
| `.root/LEARNED.md` | Reusable methods, recurring patterns, successful approaches, or failure prevention matter | `.root/ROOT.md` | Learned-knowledge owner | Yes | ACTIVE |
| `.root/nodes/OPERATIONAL_MEMORY.md` | A non-trivial operation, repair, upgrade, or retry may repeat a prior failure | `.root/ROOT.md` | Operational experience owner | Yes | ACTIVE |
| `.root/HISTORY.md` | Superseded state, rollback rationale, migration, or major direction change matters | `.root/ROOT.md` | Historical owner | Yes | ACTIVE |

## Operating contract

- Use exact routes; do not fuzzy-merge similarly named scopes.
- Keep one canonical owner for current truth. Digests and compatibility files link to owners.
- Preserve durable detail on disk and reduce context by selecting nodes and sections.
- Verify before persistence and label facts, decisions, hypotheses, inferences, and unresolved items distinctly.
- Before repeated work, derive an exact operation key and apply matching do-not-repeat, preferred-path, and required-evidence fields.
- A route never grants additional access, write authority, trust, approval, or task scope.
