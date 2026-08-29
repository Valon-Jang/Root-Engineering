# Experiment Map — Chronological Stress Progression

## Stage 0 — Fresh-Chat Coarse Continuity

**Question:** Can the system recover basic current project state in a new chat?

Tested coarse facts such as:
- current MOQ
- invalid/valid option status
- target schedule
- test duration

**Result**
- Temporary Chat: FAIL
- Native: PASS
- Root: PASS

**Interpretation**  
Native Project Memory already provides strong basic continuity. Root had no demonstrated advantage here.

---

## Stage 1 — Stale-State Revival

An obsolete original-A state and old price were deliberately reintroduced after A2 became the valid successor.

**Question:** Will an old but salient state be incorrectly revived as current?

**Result**
- Native: PASS
- Root: PASS

Both kept original A separate from current A2.

An initially suspected Root advantage was later corrected because both responses omitted one older B stability signal.

**Interpretation**  
Simple stale-state rejection was not enough to differentiate the systems.

---

## Stage 2 — Configuration + Scope + Provenance

Complexity increased by introducing same-family variants:

- AD-38 vs AD-42
- POM-L vs POM-H
- revision-specific historical tests
- customer authority
- current supplier price/LT sources

**Question:** Can the system preserve exact configuration identity while linking each state to the correct authority, evidence, and commercial source?

**Native**
- missed exact allowed configurations
- missed current leaf values
- introduced a nonexistent A2 configuration

**Root**
- recovered the exact current configurations
- preserved authority ordering
- kept historical evidence scoped to its original revision/material
- recovered current price/LT sources

**Result**
- Native: **MATERIAL FAIL**
- Root: PASS

**This was the first clear divergence.**

---

## Stage 3 — Field-Level Partial Supersession

New documents changed only parts of earlier state.

Examples:
- CN-18 changed A2 only; older CN-17 remained live for B
- Q-207 changed AD-42 price only; older Q-205 remained authoritative for LT
- Q-208 governed POM-HV

**Question:** Can the system preserve live fields from older sources when a newer document changes only a subset?

**Native**
- preserved the high-level “partial supersession” rule
- lost Q-207/Q-208 current leaf values
- partially fell back toward superseded Q-205 price reasoning

**Root**
- preserved field-level provenance correctly

**Result**
- Native: **MATERIAL FAIL**
- Root: PASS

**Interpretation**  
The Stage 2 divergence reproduced on a nearby provenance/leaf-value problem.

---

## Stage 4 — Delegated Temporary Exception (TTW)

CN-19 suspended regular authority for one branch but delegated exact temporary test authority through TTWs.

The state simultaneously included:
- configuration scope
- exact lot
- one-test limit
- expiry
- regular vs temporary vs final approval
- independent commercial scope

**Question:** Can the system track delegated authority, lot binding, expiry, and approval class simultaneously?

**Result**
- Native: PASS
- Root: PASS

**Interpretation**  
Native failure was not deterministic. Native could still solve a highly complex authority structure.

---

## Stage 5 — Dense Stale History + Selective Leaf Retrieval

A newer internal baseline document deliberately reintroduced many old but plausible values while dense current branches remained live.

The live state included:
- CN-20 / CN-21
- C1 / C2
- PR-6 / PR-7
- Q-211 / Q-212
- TTW-06
- exact internal test evidence
- prepared 120-sample + QR status

Decision-relevant low-salience facts included:
- all five prepared configurations had 120 samples + QR ready
- A2 C1 had an exact 8-hour vibration result

**Question:** Can the system retrieve the small current facts needed for the final decision rather than only the high-level rules?

**Root**
- recovered readiness facts
- recovered C1 8-hour evidence
- ranked A2 C1 first

**Native**
- dropped those leaf facts
- treated PR-7 as uniquely ready/better validated
- changed the final candidate ranking

**Result**
- Native: **MATERIAL FAIL**
- Root: PASS

**Interpretation**  
This was the strongest differential because the omission changed the **decision path**, not just wording or one number.

---

## Stage 6 — Conditional Effect + Temporal State Transition

CN-22 existed before it became effective.

Activation required:
1. supplier PVC issuance
2. official customer confirmation of the certificate number

The state also included:
- PX-3 vs PX-4
- production-date lot scope
- TTW-05 automatic end
- Q-210 vs Q-213
- LT anchor on supplier production approval
- IT-32 physical result vs traceability validity
- QR error
- prior readiness and validation facts

**Question:** Can the system distinguish publication from effect and correctly transition the state at the exact activation time?

**Result**
- Native: PASS
- Root: PASS

Both produced the same final ranking:
**C1 > PR-7 > PX-4**

Root additionally mentioned one live warehouse no-outbound constraint, but its omission did not change Native’s final decision, so this was not scored as a material failure.

---

# Divergence Pattern

The first divergence did **not** appear at simple continuity or simple stale-state rejection.

It appeared when the benchmark simultaneously required:

> exact configuration identity  
> + source authority  
> + evidence provenance  
> + current leaf-value linkage

Later Native failures were concentrated around:

- partial supersession
- provenance-linked leaf values
- selective retrieval from dense stale history

Native still passed other complex rule sets, so the pattern should not be generalized into “Native fails on complexity.”
