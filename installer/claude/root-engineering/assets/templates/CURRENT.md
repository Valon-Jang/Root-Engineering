<!-- ROOT_REVISION: 1 -->
# Current Knowledge

## Confirmed facts

- `Fact`: {{PROJECT_NAME}} is the project bound to Drive folder `{{PROJECT_FOLDER_ID}}`.
- `Fact`: Root Engineering was initialized on {{DATE}} with Drive-hosted Markdown nodes and a Claude project-instruction connection block.

## Active decisions

- `Decision`: `ROOT.md` and its routed nodes are the canonical durable project-knowledge tree.
- `Decision`: `nodes/OPERATIONAL_MEMORY.md` owns repeated-operation failure patterns, preferred paths, and required evidence.
- `Decision`: Nodes are resolved by folder ID plus fixed file name, because rewrite-based updates change file IDs.
- `Decision`: Detailed knowledge remains in storage; context cost is controlled through node-level retrieval.

## Current constraints

- `ACTIVE_CONSTRAINT`: The Claude Drive connector cannot patch file content, return a revision, or read part of a file. Updates rewrite a whole node and verify through the in-file revision and a content hash.
- Current explicit instructions outrank stored Root knowledge.
- Root updates preserve scope, authority, conditions, exceptions, provenance, and unresolved issues.
- Concurrent or stale edits are re-read and merged instead of overwritten blindly.
- A replacement node is read back before the superseded node is trashed.

## Unresolved

- `Unresolved`: Confirm and record the project's current state, active goals, and next meaningful action from authoritative sources.
- `Unresolved`: Run a fresh-chat acceptance check after initialization and replace this item with observed evidence.

## Provenance

- Root Engineering Claude initializer, {{DATE}}.
