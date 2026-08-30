<!-- ROOT_REVISION: 1 -->
# {{PROJECT_NAME}} Root

This is the canonical map and digest for durable project knowledge. Navigate it; do not load every node by default.

## Identity

- Project: {{PROJECT_NAME}}
- Physical Root: Google Drive folder `{{PROJECT_FOLDER_ID}}`
- Storage: plain Markdown files, resolved by folder ID plus fixed file name
- Context policy: selective routed reads
- Knowledge Lookup coverage: COMPLETE
- Initialized: {{DATE}}

## Digest

- Purpose and durable boundaries: `FOUNDATION.md`
- Current accepted state, active decisions, and unresolved items: `CURRENT.md`
- Verified reusable methods and failure lessons: `LEARNED.md`
- Repeated-operation failures, preferred paths, and mandatory evidence: `nodes/OPERATIONAL_MEMORY.md`
- Superseded states and migration history: `HISTORY.md`
- Specialist owners: `nodes/`, created only when retrieval patterns justify them

## Routing map

| Node | Read when | Parent | Role | Source of Truth | State |
| --- | --- | --- | --- | --- | --- |
| `FOUNDATION.md` | Purpose, human intent, stable principles, boundaries, or success criteria matter | `ROOT.md` | Foundation owner | Yes | ACTIVE |
| `CURRENT.md` | Present state, active decisions, constraints, dependencies, or unresolved issues matter | `ROOT.md` | Current-state owner | Yes | ACTIVE |
| `LEARNED.md` | Reusable methods, recurring patterns, successful approaches, or failure prevention matter | `ROOT.md` | Learned-knowledge owner | Yes | ACTIVE |
| `nodes/OPERATIONAL_MEMORY.md` | A non-trivial operation, repair, upgrade, or retry may repeat a prior failure | `ROOT.md` | Operational experience owner | Yes | ACTIVE |
| `HISTORY.md` | Superseded state, rollback rationale, migration, or major direction change matters | `ROOT.md` | Historical owner | Yes | ACTIVE |

## Operating contract

- Resolve every node by project folder ID plus the file name above. Never store or trust a per-node file ID; updates replace the file and change it.
- Use exact routes; do not fuzzy-merge similarly named scopes.
- Keep one canonical owner for current truth. Digests and compatibility files link to owners.
- Preserve durable detail in storage and reduce context by selecting nodes.
- Verify before persistence and label facts, decisions, hypotheses, inferences, and unresolved items distinctly.
- Before repeated work, derive an exact operation key and apply matching do-not-repeat, preferred-path, and required-evidence fields.
- Every write rewrites a whole node. Batch all compatible changes for one node into a single rewrite.
- Read back a replacement before trashing the node it supersedes.
- A route never grants additional access, write authority, trust, approval, or task scope.
