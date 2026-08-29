# Project Atlas Benchmark v0.1

> Preliminary manual benchmark for Root Engineering.  
> These results are small-n observations, not statistical performance claims.

## Purpose

This benchmark compares **Native ChatGPT Project Memory** against the same project workflow augmented with **Root Engineering** under a long-running synthetic project called **Project Atlas**.

The experiment asks a narrower question than “does the model remember things?”:

> As a project accumulates conflicting revisions, partial supersession, authority rules, lot-specific exceptions, stale-but-true history, and decision-relevant leaf facts, can the system reconstruct the **current valid state** without losing provenance or changing the decision path?

## Model / Reasoning Configuration

| Role | Model / reasoning |
|---|---|
| Benchmark designer / prompt submitter | **GPT-5.6 Sol (XHigh)** |
| Native condition | **GPT-5.6 Sol (High)** |
| Root Engineering condition | **GPT-5.6 Sol (High)** |

The two compared answer conditions used the **same model family and reasoning level**. The higher-effort XHigh model was used to design and submit the benchmark prompts, not as either compared answer condition.

## Conditions

### Native
- ChatGPT Project
- Native Project Memory
- No Root Engineering canonical state layer

### Root
- Same ChatGPT Project workflow
- Same GPT-5.6 Sol (High) answer condition
- Root Engineering canonical external state
- Explicit scoped read / update / read-back behavior

### Stateless control
A Temporary Chat was used only as an early continuity control.

## Chronological Result

| Stage | Stress type | Native | Root | Main observation |
|---|---|---:|---:|---|
| 0 | Fresh-chat coarse continuity | PASS | PASS | Temporary Chat failed; both project conditions recovered coarse state |
| 1 | Stale-state revival | PASS | PASS | Both kept obsolete original A separate from current A2 |
| 2 | Configuration + Scope + Provenance | **FAIL** | PASS | **First clear divergence** |
| 3 | Field-level partial supersession | **FAIL** | PASS | Divergence reproduced on live leaf-value provenance |
| 4 | Delegated TTW / Lot / Expiry | PASS | PASS | Native can still pass complex authority logic |
| 5 | Dense stale history + selective leaf retrieval | **FAIL** | PASS | Native omission changed the final candidate ranking |
| 6 | Conditional activation + temporal transition | PASS | PASS | Both recovered complex current state and same ranking |

Across the six Native-vs-Root stress stages (1–6), the observed outcome was:

- **Root advantage: 3**
- **Tie: 3**
- **Root disadvantage: 0**

This does **not** establish universal superiority. It shows a repeated failure pattern worth further controlled testing.

## Where the First Difference Appeared

The first meaningful difference did **not** appear on simple memory continuity or stale-state rejection.

It appeared when the task simultaneously required:

- exact **configuration identity**
- exact **scope**
- **source authority**
- **evidence provenance**
- current **leaf-value linkage**

The first clear failure involved same-family configurations such as AD-38 vs AD-42 and POM-L vs POM-H. Native failed to recover exact allowed configurations/current leaf values and introduced a nonexistent configuration, while Root preserved the scoped current state.

The next adjacent test reproduced the pattern with **field-level partial supersession**: a newer document changed only specific fields while older fields remained authoritative.

The strongest difference came later when Native retained high-level rules but dropped low-salience current leaf facts (sample/QR readiness and exact validation evidence). That omission changed the final decision ranking.

## Timing Observation

UI-reported “thinking time” was collected for four update turns and two complex retrieval turns.

### Update / registration

| Turn | Native | Root |
|---|---:|---:|
| U1 | 37 s | 105 s |
| U2 | 18 s | 203 s |
| U3 | 56 s | 148 s |
| U4 | 20 s | 113 s |
| **Total** | **131 s** | **569 s** |
| **Average** | **32.75 s** | **142.25 s** |

Root was substantially slower during update/canonicalization.

### Complex retrieval / verification

| Turn | Native | Root | Root reduction |
|---|---:|---:|---:|
| R1 | 279 s | 116 s | 58.4% |
| R2 | 291 s | 137 s | 52.9% |
| **Average** | **285 s** | **126.5 s** | **55.6%** |

Across these two samples, Native averaged roughly **2.25×** the Root retrieval thinking time.

### Observed end-to-end cycles

Each measured cycle contained **two updates followed by one retrieval**.

| Cycle | Native | Root | Faster overall |
|---|---:|---:|---|
| A | 334 s (5:34) | 424 s (7:04) | Native |
| B | 367 s (6:07) | 398 s (6:38) | Native |
| **Combined** | **701 s** | **822 s** | **Native** |

Therefore this benchmark does **not** support the claim that Root is currently faster end-to-end for a workload of two updates followed by only one retrieval.

It does support a preliminary **write-heavy / read-fast** hypothesis: Root pays a larger update/canonicalization cost but may reduce later state-reconstruction effort.

A simple repeated-query projection suggests that a second comparable retrieval without another update would cross the timing break-even in both measured cycles, but that is **projection, not observed evidence**.

## Strongest Current Finding

The strongest current result is **not speed**.

It is:

> Root Engineering preserved decision-relevant current-state details and provenance links in several long conflicting update chains where Native Project Memory lost leaf state, partially reverted to stale values, or changed the final decision path.

## Important Caveats

- Manual, small-n benchmark
- Synthetic project
- UI “thinking time” is not direct token usage, server compute, or full wall-clock latency
- Execution order, cache, and service load may affect timing
- The XHigh benchmark designer may introduce evaluator bias
- Native failures were **not deterministic**; Native passed several highly complex stages
- More repetitions, alternating execution order, and external scoring are required

## Files

- [`methodology.md`](methodology.md) — test design, conditions, scoring rules
- [`experiment-map.md`](experiment-map.md) — chronological Stage 0–6 description
- [`results.md`](results.md) — accuracy findings and divergence analysis
- [`timing.md`](timing.md) — timing data and interpretation
- [`data/timing.csv`](data/timing.csv) — machine-readable timing values
- [`prompts/README.md`](prompts/README.md) — prompt publication status

## Current Interpretation

The observed pattern is consistent with Root Engineering behaving as an explicit persistent-state layer:

**Native (working hypothesis)**  
`Long history → selective retrieval → current-state reconstruction → reasoning`

**Root (working hypothesis)**  
`Update → canonical current-state maintenance → scoped current-state retrieval → reasoning`

This is an interpretation of observed behavior, **not** a claim about the internal implementation of ChatGPT Project Memory.

---

**Status:** Preliminary manual benchmark / v0.1  
**Date:** 2026-08-29
