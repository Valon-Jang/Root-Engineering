<!-- ROOT_REVISION: 1 -->
# Operational Memory

This node is the canonical owner of repeated-operation failures, do-not-repeat constraints, preferred methods, and required evidence.

## Fast-path index

| Operation key | Status | Preferred path summary |
| --- | --- | --- |
| _No records yet_ | — | Add a record only after an incident or reusable verified path passes the save gate. |

## Incident classification

| Incident class | Evidence test | Required branch |
| --- | --- | --- |
| `AGENT_MISTAKE` | The capability existed, but the agent used a wrong command, path, syntax, assumption, or sequence. | Correct the input or preflight guard, then verify the original intended outcome. |
| `CAPABILITY_MISSING` | A required program, feature, Skill, plugin, connector, or runtime capability is confirmed absent. | Prepare it under current authority, verify availability, then verify the original task. |
| `OPERATION_FAILURE` | Correct inputs and prerequisites were present, but the method or product failed its contract. | Establish recurrence, diagnose cause, improve the primary method when feasible, and run regression evidence. |
| `EXTERNAL_BLOCK` | Permission, approval, restart, unavailable service, lock, rate limit, or policy prevented execution. | Preserve the block and required next condition; do not retry unchanged or relabel it as product failure. |
| `EXPECTED_NEGATIVE` | A no-match, skipped branch, or negative assertion is the documented expected result. | Interpret it with an explicit success-returning check. |
| `UNCLASSIFIED` | Available evidence cannot distinguish the categories. | Gather one bounded decision-relevant diagnostic or request missing ground truth. |

## Record contract

Each durable record includes:

1. Operation key and aliases in `subsystem/action/failure-mode` form.
2. Scope and preconditions.
3. Incident class and classification evidence.
4. Recurrence state: `FIRST_OBSERVED`, `RECURRED`, `DETERMINISTIC`, `NOT_REPRODUCED`, or `NOT_CHECKED`.
5. Capability assessment.
6. Safe failure fingerprint, root cause, and `Do not repeat` constraints.
7. Improvement and workaround assessments.
8. Preferred path, adoption basis, required evidence, outcome status, date, and provenance.

Use lifecycle states `ACTIVE_CONSTRAINT`, `OBSERVED_FAILURE`, `RESTART_PENDING`, `VERIFIED_FAST_PATH`, and `SUPERSEDED`.

Do not store raw sensitive command text or output. A safe fingerprint contains only the operation key, tool class, normalized command shape, error or exit classification, scope, preconditions, and timestamp.

## Records

No durable operation records yet.
