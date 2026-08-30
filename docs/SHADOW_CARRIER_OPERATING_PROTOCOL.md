# Shadow Carrier Operating Protocol

Status: Experimental / training phase

## Purpose

Shadow Carrier is a speculative prefetch layer that accelerates an otherwise normal adaptive AI workflow without replacing the AI's reasoning loop.

The primary goal is to hide read/search/tool latency while preserving the same decision authority, evidence quality, and final reasoning path as the Normal workflow.

Core principle:

> Do not make Interceptors decide instead of the Carrier. Make them prepare likely next read-only actions before the Carrier asks for them.

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

Interceptors remain deterministic workers whenever possible. They search, fetch, parse, validate basic scope, deduplicate, and cache. They do not make the final research judgment.

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

## Operating loop

### Step 1 — Execute the Normal current action

The Carrier chooses the current tool call exactly as it would without Shadow Carrier.

Example:

```text
Current action:
Open Claude Code headless documentation.
```

### Step 2 — Predict likely next read-only actions

Generate a small candidate set from the current task state.

Example:

```text
Likely next actions:
1. Claude Code Windows sandbox documentation
2. Claude Code permission documentation
3. Claude Code MCP configuration documentation
```

The candidate generator should be cheap. Prefer:

1. deterministic task state / missing-field map,
2. previously validated workflow pattern,
3. current Carrier plan already being produced for the task,
4. a small planner only when the first three are insufficient.

Do not add a separate LLM call merely to guess obvious next actions.

### Step 3 — Dispatch Interceptors selectively

Do not automatically launch all five.

Use more Interceptors when:

- tool latency is high,
- next-step uncertainty is high,
- candidate operations are cheap/read-only,
- several branches are plausibly independent.

Use fewer or none when:

- one next action is overwhelmingly likely,
- the tool call is already cheap,
- rate limits or monetary cost are significant,
- the task is a simple one-shot lookup.

Expected-value rule:

```text
prefetch candidate i when:

p_i * (normal_latency_i - cache_latency_i) > speculative_cost_i
```

`p_i` is the estimated probability that candidate `i` becomes an actual next action.

### Step 4 — Store results outside model context

Each result is cached with at least:

```text
candidate_id
request_signature
source/url
retrieval timestamp
status
content hash
raw/cleaned artifact reference
basic provenance
```

Do not push the body text into the Carrier context yet.

### Step 5 — Commit or discard

When the Carrier chooses its next action:

- exact/compatible cache hit → return cached result;
- no compatible hit → execute Normal action;
- unrelated speculative results → keep briefly for possible reuse or discard according to cache policy.

A cache hit must preserve the same source scope and request semantics as the action the Carrier actually selected.

### Step 6 — Learn only from observed outcomes

After the step, log whether each speculative candidate was useful.

Do not infer that a workflow pattern is good because it sounds plausible. Promote patterns only from repeated successful observations.

## Training mode

Shadow Carrier should first be learned through repeated real tasks before becoming highly autonomous.

### Phase A — Assisted Shadow

For suitable read-heavy tasks:

1. run the Normal action;
2. predict only 1–3 likely next actions;
3. prefetch them silently;
4. record whether the actual next action was in the set;
5. never change the Carrier's reasoning because of the prediction.

Goal: learn prediction quality with minimal speculative waste.

### Phase B — Dynamic Shadow

After enough observations:

- dynamically choose 0–5 Interceptors;
- use learned task patterns and current missing-field state;
- reuse cached artifacts when request signatures remain compatible;
- tune dispatch thresholds using measured hit rate and latency savings.

### Phase C — Compiled Workflow

When the same successful research/tool sequence repeats reliably, compile the stable portion into a deterministic meta-tool or reusable Skill.

Example:

```text
research_windows_agent_security(product)
```

The Carrier then sees the resolved output and exceptions rather than re-planning the stable routine every time.

This is the long-term token-saving path: repeated AI reasoning becomes machine execution.

## Metrics

Record metrics separately. Do not collapse them into one score during training.

### Prediction

- `hit@1`: actual next action was the top prediction
- `hit@3`: actual next action was within top 3
- `hit@5`: actual next action was within all dispatched candidates
- `commit_rate`: prefetched results actually consumed / prefetched results produced
- `waste_rate`: unused speculative results / prefetched results produced

### Latency

- Normal tool latency
- prefetch completion latency
- cache-return latency
- end-to-end task latency
- latency hidden by speculation

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

## Initial promotion gates

Do not treat these as permanent constants; calibrate them from real traces.

A reasonable first gate for moving from training to default Shadow use is:

- quality >= Normal,
- Hard Failure = 0,
- `hit@3 >= 70%` on the target workload,
- end-to-end latency improvement >= 20% **or** model-visible input reduction >= 30%,
- speculative monetary/rate-limit cost remains acceptable,
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

## Learning record format

For each useful training episode, keep a compact machine-readable record such as:

```json
{
  "task_class": "product_official_docs_comparison",
  "state_signature": "missing:sandbox,permission",
  "predictions": ["sandbox_docs", "permission_docs", "mcp_docs"],
  "dispatched": 3,
  "actual_next": "sandbox_docs",
  "hit_rank": 1,
  "normal_latency_ms": 6200,
  "cache_latency_ms": 280,
  "saved_ms": 5920,
  "unused_prefetches": 2,
  "quality_regression": false
}
```

Keep this learning record compact. Do not store full conversations merely to train dispatch policy.

## Current operating stance

Shadow Carrier is not a replacement for Normal reasoning and not a five-LLM subagent architecture.

It is a latency-hiding, context-safe speculative execution layer around Normal reasoning.

The target behavior is asymmetric:

> Hit → faster.
> Miss → fall back to Normal.
> Never trade answer quality for speculative speed.
