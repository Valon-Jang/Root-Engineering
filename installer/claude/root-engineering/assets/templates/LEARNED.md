<!-- ROOT_REVISION: 1 -->
# Learned Knowledge

## Verified reusable lessons

- `Method`: Start at `ROOT.md`, identify the owning route, and read only the relevant node.
- `Method`: Before a durable write, retain the owning node's revision and content hash, re-read immediately before writing, and re-merge on any difference.
- `Method`: Create the replacement node, read it back, and only then trash the superseded node.
- `Method`: Reduce context through routing rather than aggressive storage compression.
- `Method`: Prune on contact. Repair duplication, stale pointers, and contradictions only in the section already being used.
- `Failure lesson`: Keeping two current-state owners permits silent divergence. Use links or compatibility pointers instead of duplicate authority.
- `Failure lesson`: A blocked, static-only, installation-only, or restart-pending check is not verified success.
- `Failure lesson`: Trashing a node before its replacement reads back can lose the node entirely. Order matters.

## Operational-memory pointer

Detailed repeated-operation records belong only in `nodes/OPERATIONAL_MEMORY.md`. Do not duplicate those records here.

## Candidates awaiting verification

- None yet.
