# Atlas timing: conditional read/write break-even

Audit date: 2026-09-13. Status: arithmetic re-analysis of the existing six recorded rows; not a new experiment.

## What was actually measured

The [methodology](./methodology.md) identifies the metric as **UI-reported thinking time**. It is not full task wall time, active human labor, measured API compute, money or total business cost.

From [data/timing.csv](./data/timing.csv), Git blob `268b67655d5072571d364d133fc425ade593aebf`:

| Operation | Native seconds | Root seconds |
|---|---:|---:|
| U1 | 37 | 105 |
| U2 | 18 | 203 |
| R1 | 279 | 116 |
| U3 | 56 | 148 |
| U4 | 20 | 113 |
| R2 | 291 | 137 |
| Updates, total | 131 | 569 |
| Retrievals, total | 570 | 253 |
| All six operations | 701 | 822 |

The observed sequence favors Native by 121 seconds on this timing proxy. Root updates took about 4.34 times the Native update time; Native retrievals took about 2.25 times the Root retrieval time. Neither ratio describes total work efficiency.

## Explicitly hypothetical stationary-mean calculation

Let U be the number of comparable updates and Q the number of comparable retrievals. Assume, only for this sensitivity calculation, that the observed per-operation means remain constant and additive:

```text
Native(U,Q) = 32.75 U + 285.0 Q
Root(U,Q)   = 142.25 U + 126.5 Q
Root - Native = 109.5 U - 158.5 Q
```

For U > 0, the fitted timing proxy favors Root exactly when:

```text
Q/U > 109.5 / 158.5 = 219/317 = 0.690851735...
```

At four updates, the fitted break-even is Q > 2.7634. The first integer count is **three comparable retrievals**. The extrapolated totals at U=4, Q=3 are Native 986 seconds and Root 948.5 seconds, a 37.5-second Root advantage. **The third retrieval was not measured.**

## Reproduction

Run from this benchmark directory, using only Python's standard library:

```python
import csv
from fractions import Fraction
from pathlib import Path

rows = list(csv.DictReader(Path('data/timing.csv').open(encoding='utf-8', newline='')))
def total(kind, arm):
    return sum(int(r[f'{arm}_seconds']) for r in rows if r['type'] == kind)

u = sum(r['type'] == 'update' for r in rows)
q = sum(r['type'] == 'retrieval' for r in rows)
assert (u, q) == (4, 2)
assert tuple(total(k, a) for k in ('update', 'retrieval') for a in ('native', 'root')) == (131, 569, 570, 253)
extra_update = Fraction(total('update', 'root') - total('update', 'native'), u)
saved_retrieval = Fraction(total('retrieval', 'native') - total('retrieval', 'root'), q)
assert extra_update > 0 and saved_retrieval > 0
print('conditional Q/U threshold:', extra_update / saved_retrieval)
assert 4 * extra_update - 2 * saved_retrieval == 121
assert 4 * extra_update - 3 * saved_retrieval == Fraction(-75, 2)
```

## Interpretation boundary

The data contain four heterogeneous updates and two retrievals in one manual sequence. They do not establish independent per-operation distributions, a confidence interval for the threshold, or a stable production cost function. State size, query difficulty, update dependencies, caching and UI timing semantics may change the means. Six repeated measurements from one trajectory are not six independently sampled projects.

The hypothesis suggested by the pattern is that some preparation/canonicalization work can be amortized over later reads. Do not state that all Root costs have been causally transferred from reading to writing or that Q/U=0.691 is a general adoption rule.

A deployment decision must separately measure state setup and maintenance, human preparation/review/repair, full elapsed time, model/tool use and outcome quality. First-use and recurring costs should be reported separately. Missing cost terms cannot be silently set to zero. See the [unified argument](../../docs/STRUCTURE_ALLOCATION_ARGUMENT.md).
