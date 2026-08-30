# Shadow Carrier Operating Protocol

Version: 0.2
Status: Experimental / proficiency-training phase

## Purpose

Shadow Carrier is a speculative prefetch layer that accelerates an otherwise normal adaptive AI workflow without replacing the AI's reasoning loop.

The primary goal is to hide read/search/tool latency while preserving the same decision authority, evidence quality, and final reasoning path as the Normal workflow.

Core principle:

> Do not make Interceptors decide instead of the Carrier. Make them prepare likely next read-only actions before the Carrier asks for them.

The proficiency goal is equally important:

> Learn from every observable tool trajectory, including ordinary Normal workflows, so Shadow prediction improves faster than Shadow-only trial and error.

## Architecture

```text
Carrier / Normal reasoning
        |
        | current tool action
        | + likely next read-only actions
        v
Shadow Scheduler
   |   |   |   |   |
  I1  I2  I3  I4  I5
   \   \   |   /   /
      hidden cache
          |
     commit only if
     Carrier selects it
          |
          v
       Carrier
```

Interceptors remain deterministic workers whenever possible. They search, fetch, open, read, parse, validate basic scope, deduplicate, and cache. They do not make the final research judgment.

## Non-negotiable rules

1. **Normal reasoning remains authoritative.**
   - The Carrier decides what information is needed next.
   - A speculative result never forces the next step.

2. **Speculative work is read-only.**
   - Allowed: search, fetch, open, read, parse, hash, deduplicate, cache, metadata inspection.
   - Forbidden by default: send, post, delete, purchase, submit, mutate state, change permissions, write to production data, or any irreversible action.

3. **Prefetched results stay hidden until selected.**
   - Unused speculative results do not enter model context.
   - Only a result that matches an actual Carrier-selected next action is committed to the AI-visible path.

4. **A miss falls back to Normal.**
   - If the needed result was not prefetched, run the normal tool action.
   - A speculative miss may cost machine/network work, but must not lower answer quality.

5. **Evidence is not aggressively summarized.**
   - For selected natural-language evidence, preserve at least 70% of the selected body text.
   - Maximum text reduction is 30% and is a ceiling, not a quota.
   - Remove only safe filler/redundant framing; preserve numbers, IDs, dates, negation, conditions, exceptions, scope, authority, provenance, uncertainty, comparisons, causal links, and conflict/supersession relations.
   - If uncertain, pass the original text.

6. **Page/source selection is retrieval, not compression.**
   - It is valid to keep irrelevant prefetched pages outside model context.
   - Once a page/section is selected as evidence, do not turn it into a tiny summary merely to save tokens.

7. **Prefetch horizon is bounded.**
   - Default horizon = one likely next tool step.
   - Horizon 2 is allowed only for repeatedly validated, low-cost, read-only sequences.
   - Do not recursively speculate arbitrary future trees. This prevents combinatorial explosion.

8. **Candidate diversity beats duplicate guessing.**
   - Do not spend five Interceptors on five near-identical queries unless the task explicitly benefits from source redundancy.
   - Prefer distinct plausible next branches or distinct authoritative source families.

## Shadow State

Before predicting, build a compact machine-readable `Shadow State`. It should contain only features that can change the next tool decision.

Recommended fields:

```json
{
  "task_class": "official_docs_comparison",
  "current_action": "open_headless_docs",
  "recent_actions": ["search_product", "open_headless_docs"],
  "entities": ["Claude Code"],
  "unresolved": ["windows_sandbox", "permissions", "mcp"],
  "required_authority": "first_party",
  "freshness": "current",
  "known_sources": ["code.claude.com"],
  "mutation_allowed": false
}
```

Do not include full conversation text merely to predict the next action.

## Candidate generation hierarchy

Generate likely next actions using the cheapest reliable source first.

Priority order:

1. **Deterministic obligation / missing-field map**
   - Required field, gate, dependency, or unresolved item already explicit in task state.
   - Example: 6 comparison gates and only `sandbox` + `permission` remain missing.

2. **Exact validated trajectory match**
   - A previously observed state signature led to the same next action repeatedly.

3. **Short action-transition memory**
   - Reusable patterns such as `search -> open official docs -> open security/permissions docs`.
   - Prefer short local transitions over memorizing whole conversations.

4. **Task-class pattern**
   - Similar task classes may have stable source and action ordering.

5. **Current Carrier plan**
   - Reuse next actions the Carrier is already implicitly or explicitly considering.

6. **Small planner only when necessary**
   - Use only when the above sources cannot produce a useful candidate set.
   - Never make a planner reread the full raw corpus merely to predict tool calls.

## Prediction confidence

Exact calibrated probabilities are optional during early training. Use confidence bands if necessary:

- `VERY_HIGH`: nearly forced next step / direct dependency
- `HIGH`: strong repeated pattern
- `MEDIUM`: plausible branch
- `LOW`: weak guess

When enough traces exist, convert these bands into empirical hit probabilities per task class and state signature.

## Choosing how many Interceptors to dispatch

Do not automatically launch all five.

Use the **smallest candidate set with positive expected value and adequate expected coverage**.

Expected-value rule:

```text
prefetch candidate i when:

p_i * (normal_latency_i - cache_latency_i) > speculative_cost_i
```

Practical dispatch policy during training:

- 0 workers: speculation has no positive expected value.
- 1 worker: one next action is dominant.
- 2–3 workers: several realistic branches exist; default useful range.
- 4–5 workers: branch uncertainty is genuinely broad and speculative calls are cheap/read-only.

When probabilities are available, choose the smallest `k` such that:

```text
cumulative_probability(top-k) >= target_coverage
```

while every dispatched candidate still has positive expected value.

Initial `target_coverage` for training can be 0.80, but calibrate it from actual traces rather than treating it as permanent.

## Source-aware prefetching

When the next action is a search/read action, Shadow Carrier should also learn **where** useful evidence normally comes from.

Maintain compact source preferences per task class/entity, for example:

```text
official_docs_comparison:
  prefer first-party docs
  then official repository docs/issues
  then primary standards/regulatory sources
  avoid generic marketing/home/login pages when a technical document is required
```

Learn negative source patterns too. Repeatedly useless generic pages should be deprioritized without exposing them to the Carrier.

This source preference is retrieval routing, not evidence summarization.

## Operating loop

### Step 1 — Execute the Normal current action

The Carrier chooses the current tool call exactly as it would without Shadow Carrier.

### Step 2 — Build Shadow State

Capture the current action, unresolved information, task class, known sources, recent actions, and any hard source/authority/freshness constraints.

### Step 3 — Predict likely next read-only actions

Generate a small ranked candidate set using the hierarchy above.

Example:

```text
Likely next actions:
1. Claude Code Windows sandbox documentation
2. Claude Code permission documentation
3. Claude Code MCP configuration documentation
```

### Step 4 — Dispatch Interceptors selectively

Dispatch only positive-EV candidates. Prefer 1–3 unless broad uncertainty justifies more.

### Step 5 — Store results outside model context

Each cached result should contain at least:

```text
candidate_id
canonical_request_signature
action_type
target/entity
scope/parameters
source/url
retrieval timestamp
freshness window
status
content hash
raw/cleaned artifact reference
basic provenance
```

Do not push body text into the Carrier context yet.

### Step 6 — Compatibility gate before commit

A cache hit is usable only if the actual action matches the prefetched request semantically, not merely lexically.

Check at minimum:

```text
action intent
target/entity
scope
parameters
required authority/source type
freshness requirement
time-sensitive cutoff if applicable
```

If a material field differs, treat it as a miss and execute the Normal action.

### Step 7 — Commit or discard

When the Carrier chooses its next action:

- compatible cache hit → return cached result;
- no compatible hit → execute Normal action;
- unrelated speculative results → keep briefly for possible reuse or discard according to cache policy.

### Step 8 — Learn from the observed transition

Record:

```text
Shadow State -> predicted candidates -> actual next action -> hit rank -> latency/cost outcome
```

Do not store full conversation text merely for dispatch learning.

## Learn from Normal workflows too

Shadow proficiency must not depend only on occasions when Shadow Carrier was enabled.

Whenever a normal multi-tool workflow exposes a useful sequence such as:

```text
search -> open result -> inspect gap -> search narrower -> open official source
```

capture the compact transition trace after the fact.

This creates training data without speculative runtime cost.

A Normal trace can teach:

- next-action transitions,
- common missing-field sequences,
- useful source families,
- dead-end source patterns,
- typical tool latency,
- when branching tends to occur.

The actual Normal action remains the ground truth label for next-action prediction.

## Counterfactual replay training

Use saved traces to improve policy **without executing new web/tool calls**.

For each historical trajectory, replay candidate policies offline:

```text
What would hit@1 have been?
What would hit@3 have been?
Would dispatching 5 instead of 2 have saved more wall-clock after speculative cost?
Which confidence threshold minimized waste?
Which source preference would have avoided dead ends?
```

Replay several policies against the same trace set and choose the best expected policy for that task class.

This is the fastest path to proficiency because one real workflow can train many hypothetical dispatch policies.

## Training curriculum

### Phase A — Observe Normal

Before aggressive speculation, harvest compact action traces from real Normal workflows.

Goal:
- discover common transitions,
- measure tool latency,
- build initial source preferences,
- find predictable task classes.

Shadow may remain off or use only one low-risk prefetch.

### Phase B — Assisted Shadow

For suitable read-heavy tasks:

1. execute Normal current action;
2. predict 1–3 likely next actions;
3. prefetch silently;
4. record actual next action and hit rank;
5. preserve Normal reasoning authority.

Goal: establish safe hit-rate and waste-rate baselines.

### Phase C — Dynamic Shadow

After enough observations:

- dynamically choose 0–5 Interceptors;
- use learned transitions, task classes, source preferences, and unresolved-field maps;
- tune target coverage and EV thresholds from replay;
- reuse compatible cached artifacts;
- shorten or disable cache TTL for time-sensitive data.

### Phase D — Compiled Workflow

When the same successful action sequence repeats reliably, compile the stable portion into a deterministic meta-tool or reusable Skill.

Example:

```text
research_windows_agent_security(product)
```

The Carrier then sees the resolved output and exceptions rather than re-planning the stable routine every time.

This is the long-term token-saving path: repeated AI reasoning becomes machine execution.

## Proficiency ladder

Track proficiency by **measured behavior**, not by a subjective label.

### P0 — Untrained
- no reliable transition data
- Shadow mostly off

### P1 — Observing
- Normal traces collected
- common action/source patterns identified

### P2 — Assisted
- hit@3 begins to stabilize
- speculation limited to 1–3 read-only candidates

### P3 — Calibrated
- per-task-class hit rates and latency estimates available
- dynamic dispatch count is evidence-based
- cache compatibility failures are rare

### P4 — Predictive
- Shadow frequently hides material tool latency with Normal-quality parity
- source routing avoids known dead ends
- replay-selected policy outperforms fixed-k policies

### P5 — Compiled
- repeated stable trajectories converted into deterministic Skills/meta-tools
- Carrier mainly handles novelty, conflict, and exceptions

Do not promote proficiency merely because one benchmark was successful.

## Exploration vs exploitation

A purely greedy predictor can become trapped in old patterns.

During training, reserve a small amount of low-cost exploration when:

- the task class is changing,
- source layout recently changed,
- observed hit rate is degrading,
- multiple branches have similar confidence.

Exploration must remain read-only and cost bounded.

Do not explore just to consume idle Interceptors.

## Cache policy

Cache reuse is valuable only when semantics and freshness remain valid.

Use shorter TTL when:

- current news/status is involved,
- availability/prices/versions can change quickly,
- an issue/PR/build state is live.

Use longer TTL when:

- stable official documentation is being read,
- repository files are pinned to a commit/ref,
- immutable artifacts are addressed by hash.

A cache entry with uncertain freshness should not silently replace a Normal fresh lookup.

## Metrics

Record metrics separately. Do not collapse them into one score during training.

### Prediction

- `hit@1`: actual next action was the top prediction
- `hit@3`: actual next action was within top 3
- `hit@5`: actual next action was within all dispatched candidates
- `MRR`: reciprocal rank of the actual next action, averaged across traces
- `commit_rate`: prefetched results actually consumed / prefetched results produced
- `waste_rate`: unused speculative results / prefetched results produced
- `compatibility_reject_rate`: nominal hits rejected because scope/parameters/freshness did not match

### Latency

- Normal tool latency
- prefetch completion latency
- cache-return latency
- end-to-end task latency
- latency hidden by speculation
- time lost on misses/rate-limit interference

### Cost

- speculative requests
- speculative bytes
- API/network/compute cost
- rate-limit incidents attributable to speculation

### Context / tokens

- model-visible evidence in Normal
- model-visible evidence with Shadow Carrier
- speculative machine-only bytes
- unused speculative bytes kept outside model context

Machine-only speculative work is not model-visible token usage, but its compute/network/API cost must still be reported separately.

### Quality

Use the existing Carrier quality contract:

- Factual Accuracy
- Critical Coverage / Recall
- Evidence Precision / Relevance
- Scope Fidelity
- Provenance / Authority Fidelity
- Conflict Handling
- Reasoning / Decision Quality
- Information Efficiency
- Hard Failure

Quality must be at least Normal. A speed gain with a material quality regression is a failure.

## Training record schema

For each observed transition, keep a compact record such as:

```json
{
  "task_class": "product_official_docs_comparison",
  "state_signature": "missing:sandbox,permission",
  "current_action": "open_headless_docs",
  "predictions": [
    {"action": "sandbox_docs", "confidence": "HIGH"},
    {"action": "permission_docs", "confidence": "MEDIUM"},
    {"action": "mcp_docs", "confidence": "MEDIUM"}
  ],
  "dispatched": 3,
  "actual_next": "sandbox_docs",
  "hit_rank": 1,
  "normal_latency_ms": 6200,
  "prefetch_latency_ms": 2700,
  "cache_latency_ms": 280,
  "saved_ms": 5920,
  "unused_prefetches": 2,
  "compatibility_reject": false,
  "quality_regression": false
}
```

Keep traces compact and strip project-sensitive content when the learning pattern can be represented generically.

## Policy update rule

Do not rewrite policy after every single observation.

At meaningful checkpoints:

1. aggregate traces by task class/state signature,
2. compare current policy with counterfactual alternatives,
3. identify repeated wins/failures,
4. update only reusable routing rules,
5. retain rollback information for policy changes.

Examples of reusable updates:

- `official docs comparison + unresolved security gate -> security/permissions docs often next`
- `site-restricted GitHub lookup -> enforce repository path, not domain only`
- `generic product homepage repeatedly unused -> deprioritize for technical-gate tasks`

Do not encode one-off accidental action sequences as permanent policy.

## Initial promotion gates

Do not treat these as permanent constants; calibrate them from real traces.

A reasonable first gate for moving a workload from training to default Shadow use is:

- quality >= Normal,
- Hard Failure = 0,
- `hit@3 >= 70%`,
- positive net latency value after speculative cost,
- end-to-end latency improvement >= 20% **or** model-visible input reduction >= 30%,
- speculative monetary/rate-limit cost remains acceptable,
- compatibility reject rate remains low,
- no speculative mutating actions.

If these gates are not met, keep Shadow Carrier off for that workload.

## Best-fit workloads

Strong candidates:

- multi-step web research,
- repeated official-document audits,
- source comparison across several products,
- repository/document exploration,
- workflows with slow independent reads,
- tasks with recurring retrieval patterns,
- long investigations where the next one or two reads are often predictable.

Weak candidates:

- one-shot deterministic lookups,
- creative writing,
- highly novel tasks with unpredictable branching,
- cheap local computations,
- operations dominated by mutation/approval rather than reading,
- expensive/rate-limited APIs where speculative misses are costly.

## Failure modes to watch

1. **Over-prefetching** — five workers launched for every step regardless of value.
2. **Context leakage** — unused speculative results accidentally entering model context.
3. **Semantic mismatch** — a cached result is reused for a superficially similar but materially different request.
4. **Planner inflation** — a separate LLM spends more reasoning tokens predicting next actions than speculation saves.
5. **Agent imitation** — Interceptors start independently deciding conclusions and recreate the cost of full subagents.
6. **Compression drift** — selected evidence is summarized far below the 70% retention floor.
7. **Rate-limit amplification** — parallel speculative queries make the actual task slower or less reliable.
8. **Branch explosion** — speculative horizon expands recursively and creates a search tree instead of a next-step cache.
9. **Pattern lock-in** — historical traces suppress new valid branches after tools/sites/tasks change.
10. **False cache hit** — same keywords but different scope/freshness/authority are treated as equivalent.

## Current operating stance

Shadow Carrier is not a replacement for Normal reasoning and not a five-LLM subagent architecture.

It is a latency-hiding, context-safe speculative execution layer around Normal reasoning.

Current optimization priority:

1. observe and learn from Normal tool trajectories,
2. maximize next-action prediction quality,
3. minimize speculative waste and cache mismatches,
4. hide read/search latency without changing the reasoning path,
5. compile repeatedly successful trajectories only after evidence accumulates.

The target behavior is asymmetric:

> Hit -> faster.
> Miss -> fall back to Normal.
> Learn from both.
> Never trade answer quality for speculative speed.
