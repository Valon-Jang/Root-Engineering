# Results

## Accuracy Summary

For Native-vs-Root stress Stages 1–6:

- Root advantage: **3**
- Tie: **3**
- Root disadvantage: **0**

The three material Native failures were:

1. **Configuration / scope / provenance separation**
2. **Field-level partial supersession**
3. **Selective retrieval of decision-relevant leaf state**

## Material Failure 1 — Hallucinated / Mis-reconstructed State

Native failed to recover exact allowed configurations/current values and introduced a nonexistent configuration.

Root preserved:
- exact configuration identity
- customer authority
- historical evidence scope
- commercial source linkage

This was the **first clear same-input differential**.

## Material Failure 2 — Rule Retained, Leaf Values Lost

Native remembered the high-level principle that newer documents do not always replace older documents globally.

However, it lost the live field-level linkage:
- new source changed price only
- older source remained live for LT
- separate quote governed a different material configuration

This is important because the failure was not “forgot the rule.”

It was:

> remembered the rule, but failed to reconstruct the current state values that the rule should produce.

## Material Failure 3 — Omission Changed the Decision

Native retained much of the high-level authority/scope structure but dropped:
- prepared 120-sample + QR state
- exact C1 validation evidence

That omission caused a different final ranking.

This is the strongest benchmark result because it demonstrates:

`leaf-state omission → state reconstruction difference → decision-path difference`

## Cases Where Native Passed

Native also passed:
- simple stale-state rejection
- delegated TTW / lot / expiry logic
- conditional document activation / exact temporal transition

These controls matter because they show the benchmark is not merely selecting cases where Native fails.

## Current Interpretation

The current evidence is consistent with a narrower hypothesis:

> Explicit canonical current state may improve the stability of provenance-linked, low-salience, decision-relevant leaf facts under long conflicting update chains.

This benchmark does not reveal or prove how Native Project Memory works internally.

## Strongest Claim Supported Today

A conservative public statement is:

> In this preliminary paired synthetic benchmark, Native Project Memory and Root Engineering performed similarly on simple continuity and several complex authority tasks. Differences first appeared when exact configuration scope, provenance, partial supersession, and decision-relevant leaf retrieval had to be maintained across a long conflicting update history. In three stages, Native produced material state-reconstruction errors while the Root condition preserved the expected current state. More controlled repetitions are required.

## Claims Not Supported Yet

Do not claim:

- Root is always more accurate
- Native Project Memory cannot handle complex projects
- Root reduces total latency
- Root is “55% faster”
- the observed mechanism is proven
