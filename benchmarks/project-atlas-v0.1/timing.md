# Timing Results

## Measurement Type

All values below are **ChatGPT UI-reported thinking time**.

They are exploratory and should not be interpreted as direct model compute, token use, or full wall-clock latency.

## Raw Update / Registration Times

| Turn | Native | Root | Root overhead |
|---|---:|---:|---:|
| U1 | 37 s | 105 s | +68 s |
| U2 | 18 s | 203 s | +185 s |
| U3 | 56 s | 148 s | +92 s |
| U4 | 20 s | 113 s | +93 s |
| **Total** | **131 s** | **569 s** | **+438 s** |
| **Average** | **32.75 s** | **142.25 s** | — |

Root update overhead was variable, so it should **not** be modeled as a stable fixed cost yet.

## Raw Retrieval / Verification Times

| Turn | Native | Root | Root saving | Root reduction |
|---|---:|---:|---:|---:|
| R1 | 279 s | 116 s | 163 s | 58.4% |
| R2 | 291 s | 137 s | 154 s | 52.9% |
| **Total** | **570 s** | **253 s** | **317 s** | — |
| **Average** | **285 s** | **126.5 s** | **158.5 s** | **55.6%** |

Across these two samples, Native retrieval thinking time averaged about **2.25×** Root.

## Observed End-to-End Cycles

### Cycle A
Two updates followed by one retrieval.

- Native: 37 + 18 + 279 = **334 s (5:34)**
- Root: 105 + 203 + 116 = **424 s (7:04)**

Root was **90 s slower overall**.

### Cycle B
Two updates followed by one retrieval.

- Native: 56 + 20 + 291 = **367 s (6:07)**
- Root: 148 + 113 + 137 = **398 s (6:38)**

Root was **31 s slower overall**.

### Combined Observed Time

- Native: **701 s (11:41)**
- Root: **822 s (13:42)**

For the measured workload of **two updates → one complex retrieval**, Native was faster end-to-end.

## Break-Even Projection

This is a projection, not an observed result.

Cycle A:
- Root update overhead: 253 s
- per-retrieval saving observed: 163 s

Cycle B:
- Root update overhead: 185 s
- per-retrieval saving observed: 154 s

A second comparable retrieval without another update would cross the simple timing break-even in both cycles.

This supports a working hypothesis of:

> **write-heavy / read-fast cost shifting**

but does not yet prove a speed advantage in real workloads.

## Next Measurement Improvements

Future runs should:
- record actual wall-clock time in addition to UI thinking time
- alternate Native/Root execution order
- repeat each stage multiple times
- record output length
- record every update and retrieval turn
- keep model/reasoning settings fixed
- separate update-only, retrieval-only, and full-cycle metrics
