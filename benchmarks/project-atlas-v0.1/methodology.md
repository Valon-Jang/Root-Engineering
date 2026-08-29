# Methodology

## Benchmark Type

Manual paired benchmark using a synthetic long-running project: **Project Atlas**.

The benchmark intentionally accumulated:

- revisions
- material/process variants
- exact lots
- customer authority documents
- supplier quotes
- internal validation evidence
- temporary waivers
- expiry times
- partial supersession
- conditional activation
- stale-but-true historical facts
- stale but plausible baseline reintroduction
- low-salience decision-relevant leaf facts

The goal was to test **current-state reconstruction**, not raw recall.

## Model Configuration

| Role | Model / reasoning |
|---|---|
| Benchmark designer and prompt submitter | GPT-5.6 Sol (XHigh) |
| Native answer condition | GPT-5.6 Sol (High) |
| Root answer condition | GPT-5.6 Sol (High) |

The two compared answer conditions used the same model/reasoning setting.

## Compared Conditions

### Native
Native ChatGPT Project Memory.

### Root
Same project workflow with Root Engineering enabled.

Root Engineering maintained a writable canonical state layer with scoped reads and update/read-back behavior.

### Stateless Control
A Temporary Chat was used only to confirm that continuity depends on persistent project context.

## Prompt Matching

Native and Root were given matched benchmark inputs in the same synthetic project progression.

A later control clarification explicitly confirmed that both compared conditions had received the same preceding inputs for the selective-retrieval case.

## Scoring

A response was considered materially correct when it preserved the decision-relevant current state across these axes:

1. Configuration / scope
2. Authority / temporal activation
3. Lot eligibility / cancellation
4. Commercial field provenance and LT anchor
5. Evidence / traceability separation
6. Readiness / leaf retrieval
7. Final decision path or ranking

### Material failure

A failure was treated as material when it:

- invented a nonexistent state/configuration,
- revived a superseded value as current,
- lost a live field while preserving only the high-level rule,
- mis-scoped evidence or authority,
- or changed the final decision ranking because of an omission.

Pure wording/style differences were not counted as performance differences.

## Timing Measurement

Timing values are the **UI-reported thinking time** visible in ChatGPT.

They are not direct measurements of:

- token consumption
- server compute
- model FLOPs
- API latency
- full wall-clock latency

Timing is therefore treated as a secondary exploratory signal.

## Bias / Confound Disclosure

Potential confounds include:

- manual benchmark design
- small sample count
- XHigh benchmark designer/evaluator
- execution order
- cache effects
- service load
- hidden memory retrieval behavior
- UI timing semantics

Future benchmark versions should:

- pre-register expected state and scoring,
- alternate Native/Root execution order,
- repeat each stage,
- use an external or blinded evaluator where practical,
- export exact raw prompts and responses,
- measure wall-clock time separately,
- and test across multiple models/providers.
