# Repository Placement Status

**Status:** Incubation copy pending standalone repository migration  
**Decision date:** 2026-09-13

## Placement decision

Goal-Directed Self-Structuring AI (GDSSA) should be maintained as a **standalone public research repository**, not as a permanent subtopic of Root Engineering.

Planned canonical repository:

`Valon-Jang/Goal-Directed-Self-Structuring-AI`

## Why

- GDSSA is broader than Root Engineering. Root Engineering is one persistence/knowledge substrate that can support GDSSA, not the parent concept.
- GDSSA has its own research hypotheses, failure modes, benchmark design, terminology, and future implementation path.
- Existing repository structure already separates independent research programs such as Persistent Project Thread, Qwen Reasoning Architecture Study, and Swarm Micro-Reasoning Study from the Root Engineering implementation repository.
- Keeping GDSSA permanently under `Root-Engineering/research/` would imply the wrong conceptual hierarchy.

## Migration rule

Until the standalone repository exists and its contents are verified, the current README remains the preserved source copy.

After migration:

1. copy the full research document and future benchmark structure to the standalone repository;
2. verify the destination contents;
3. replace this directory with a short pointer to the standalone canonical repository rather than silently deleting the research lineage;
4. keep Root Engineering referenced from GDSSA as a supporting architecture, and link GDSSA from Root Engineering only as related research.

No academic priority or universal novelty claim is implied by this repository split.
