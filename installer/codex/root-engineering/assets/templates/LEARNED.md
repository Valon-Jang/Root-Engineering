<!-- ROOT_REVISION: 1 -->
# Learned Knowledge

## Verified reusable lessons

- `Method`: Start at `.root/ROOT.md`, identify the owning route, and read only the relevant node or section.
- `Method`: Before a durable write, retain the owning node's revision or SHA-256, apply the smallest contextual patch, and re-read on conflict.
- `Method`: Reduce context through routing rather than aggressive storage compression.
- `Failure lesson`: Keeping two current-state owners permits silent divergence. Use links or compatibility pointers instead of duplicate authority.
- `Failure lesson`: A blocked, static-only, installation-only, or restart-pending check is not verified success.
- `Method`: Prune on contact. Repair duplication, stale pointers, and contradictions only in the section already being used.

## Operational-memory pointer

Detailed repeated-operation records belong only in `.root/nodes/OPERATIONAL_MEMORY.md`. Do not duplicate those records here.

## Candidates awaiting verification

- None yet.
