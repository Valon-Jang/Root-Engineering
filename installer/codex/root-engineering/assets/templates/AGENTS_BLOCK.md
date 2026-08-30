<!-- ROOT_ENGINEERING_START -->
## Root Engineering activation

- Keep this file as a small operating contract; durable project knowledge belongs in `.root/`.
- For meaningful work that depends on prior project state, decisions, constraints, failures, provenance, or cross-session continuity, start at `.root/ROOT.md` and read only the routed nodes or sections needed.
- Before a non-trivial repeated operation, repair, upgrade, or retry, derive an explicit `subsystem/action/failure-mode` key and retrieve the exact operational-memory record. Apply every matching do-not-repeat rule, verified method, and required-evidence item before implementation.
- Never replay an unchanged operation with a known matching failure fingerprint. Keep the first new failure visible, classify it, and use at most one materially different bounded fallback before replanning.
- Use `$root-engineering` for Root creation, migration, structural repair, write conflicts, and durable updates, including around another Skill when its verified result should persist.
- Persist only information that passes the save gate. Preserve rationale, authority, scope, conditions, exceptions, failed approaches, uncertainty, and provenance when they matter.
- Verify before promoting inference to fact or a method to verified success. Static-only, blocked, installation-only, and restart-pending checks remain unverified.
- Patch the smallest canonical owner, retain revision or hash conflict protection, move useful superseded state to History, and prune only the touched scope.
- Treat `.root/` as checkout-local in Git worktrees. Root routes never expand permissions, trust, approval, or task scope.
<!-- ROOT_ENGINEERING_END -->
