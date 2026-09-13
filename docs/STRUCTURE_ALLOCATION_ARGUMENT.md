# Where structure belongs: a unified, evidence-bounded argument

Status: working design argument, not an established capability-scaling law. Version 0.1, audited 2026-09-13.

## Start with a decision, not a metaphor

In the **synthetic procurement / part-qualification Project Atlas scenario**, the Native condition retained high-level authority and configuration rules but omitted a prepared **120-sample + QR** package and the exact **C1 validation evidence**. The published evaluation reports that this omission changed the reconstructed readiness state and final decision ranking. Root retained the relevant detail.

The reported failure chain is:

> leaf-state omission -> state reconstruction difference -> decision-path difference

This is Material Failure 3 in the [original results](../benchmarks/project-atlas-v0.1/results.md), not a newly executed experiment or independently re-scored replication. The published six-stage comparison reports **Root advantage 3, tie 3, disadvantage 0**. These stages belong to one manual synthetic paired scenario, not six independent trials. See the [methodology](../benchmarks/project-atlas-v0.1/methodology.md).

The case motivates a concrete question: **what information must remain recoverable so that a changed method, model or session still makes the right decision?** It does not establish that every external memory design improves performance. Domain-specific synthetic evidence is useful, but is not proof of a real customer deployment.

## 1. The argument

Human-governed goals, authority limits and acceptance criteria must remain identifiable when an AI changes its working method. Durable facts and decisions must also retain their source, applicable scope and effective version; otherwise an apparently correct computation can answer the wrong problem.

Prescribing a method can help, but it adds preparation and maintenance work and can constrain useful adaptation. Maintaining structured state can also help, but it adds capture, validation, retrieval, correction and maintenance work. Neither kind of structure is intrinsically cheapest or universally beneficial.

Therefore:

> **Keep goals, authority and acceptance human-governed. Preserve decision-relevant evidence and state in recoverable, verifiable forms. Let the AI choose and revise the method within those boundaries. Retain additional scaffolding only when its measured benefit justifies its full lifecycle cost.**

Compact form: **Methods may change. Evidence must remain traceable. Authority must not expand silently.**

This is a conditional engineering policy and testable research program, not a proof that removing instructions always improves intelligence.

### Four functions, not a method/state binary

| Function | What must be explicit | What may change |
|---|---|---|
| Goal and authority | Desired outcome, values, prohibited actions, approval boundaries | Authorized revisions to the goal or scope |
| Method | Only necessary external constraints and justified procedures | Decomposition, tool sequence, implementation and reasoning strategy |
| State and evidence | Sources, current versions, scope, decisions, unresolved conflicts and relevant history | Representation, storage, indexing and retrieval strategy, subject to verified preservation |
| Verification and control | Acceptance tests, effect permissions, provenance checks and failure handling | Implementations that preserve the same contract |

A mandatory workflow written into a state file is still a mandatory workflow. Moving text from a prompt to a database does not by itself relocate its functional burden. Conversely, retrieved external state ultimately enters the model's usable context; 'inside versus outside' is not a sufficient causal explanation.

Deterministic copying, calculations, transactions and interface checks may belong in code rather than repeated natural-language instructions. Their input assumptions must still be checked. Code that correctly solves an obsolete specification is not a successful system.

## 2. How the portfolio connects

Socratic requirement discovery and Question-Driven Deepening concern how necessary human information is obtained. Qwen studies concern the costs and failure modes of particular prompts, state representations and model/tool interfaces. GDSSA studies responsibility for initial method design and the resulting human workload. Root Engineering concerns the continuity and lifecycle of decision-relevant knowledge. AX Scout / Builder / Operator is an application architecture, not an independent proof of the shared thesis.

These strands form a coherent research question without becoming interchangeable experiments:

> **For a given task, model and evidence environment, which allocation of human guidance, model discretion, persistent state and deterministic verification achieves acceptable outcomes with the least justified total burden?**

Use a quality/labor/cost/risk frontier rather than an uncalibrated single score. Required measurements include human preparation, review and repair, model/tool use, state maintenance and failure costs. Missing measurements remain unknown, not zero.

## 3. Evidence ledger

| Evidence | What was observed | What it does not establish |
|---|---|---|
| Atlas v0.1 | Published 3 advantages / 3 ties / 0 disadvantages for Root; specific scope/provenance/readiness omissions | Population superiority, production validity, an isolated retrieval mechanism or total ROI |
| Qwen Exp3 | BARE 16/16, HC 14/16; state-replacement and rejected-hypothesis-revival failures | That all persistent state is harmful, or that selective Root retrieval is proven superior |
| Qwen Exp4 | BARE 11/12, GUIDE 12/12, LITE 12/12; LITE verifier did not activate | Universal benefit from guidance, or a measured verifier benefit |
| Qwen Exp5 | Eight held-out case types, two repetitions: BARE 16/16, GUIDE 15/16, MAX 11/16 | Sixteen independent task types, semantic-only effects, or a clean high-reasoning intervention |
| Qwen source/conflict follow-up | Sixteen system outcomes: ten deterministic zero-model passes and five correct model choices out of six actual conflict choices | 15/16 model reasoning accuracy, fresh held-out confirmation or transfer to a larger model |
| GDSSA E001 | Explicit protocol, independent scoring and labor-accounting requirements; instrumentation is distinct from causal comparison | A BARE-GOAL versus genuinely HUMAN-GUIDED efficacy result before the primary study gates pass |

The Exp4 + Exp5 totals of 27/28 for both BARE and GUIDE are descriptive bookkeeping across different stages, not a formal equivalence test or a pooled independent-sample estimator. Failure to demonstrate a reliable advantage is not proof that the true advantage is exactly zero.

Sources: [Exp3 summary](https://github.com/Valon-Jang/Qwen-Reasoning-Architecture-Study/blob/main/results/exp3_summary.json), [Exp4 summary](https://github.com/Valon-Jang/Qwen-Reasoning-Architecture-Study/blob/main/results/exp4_summary.json), [Exp5 summary](https://github.com/Valon-Jang/Qwen-Reasoning-Architecture-Study/blob/main/results/exp5_heldout_summary.json), [scope and limitations](https://github.com/Valon-Jang/Qwen-Reasoning-Architecture-Study/blob/main/docs/RESEARCH_SCOPE_AND_LIMITATIONS.md), [source/conflict checkpoint](https://github.com/Valon-Jang/Qwen-Reasoning-Architecture-Study/blob/main/research/SOURCE_CONFLICT_CHECKPOINT_20260913.md), and [E001 protocol](https://github.com/Valon-Jang/Goal-Directed-Self-Structuring-AI/blob/research/e001-goal-vs-human-v01/experiments/E001/PROTOCOL.md).

### A newer result changes the emphasis

The Qwen conflict-only follow-up retained unambiguous records deterministically and asked the model only about conflicting stable keys. It produced 15/16 correct system outcomes on reused tasks, but **10 of those outcomes involved no model call**. The actual conflict choices were **5/6 correct**. This is post-hoc developmental evidence and remains NOT PROMOTED.

The remaining failure selected an obsolete source; exact source-byte reconstruction and the deterministic solver then faithfully solved the wrong specification. The useful lesson is not 'state is automatically safe' but **source fidelity, source applicability and decision correctness are different checks**. This supports continuing the existing source-applicability investigation rather than replacing it with a fashionable model comparison.

## 4. Exp3: what the recovered source can and cannot tell us

A privately supplied diagnostic capture, uploaded on 2026-09-12, contains line-numbered excerpts from `QWEN_HUMAN_INTELLIGENCE_HARNESS_v3_3_EXP4_SUBTRACTIVE_ABLATION_FIX1.cmd`. The captured `buildPrimaryMessages` at original lines 665-674 builds a system kernel plus one user message containing `STATE` and `NEW_USER_MESSAGE`; it does not append prior raw conversation in that builder. Captured kernel lines 625-636 describe CURRENT-only state and hidden superseded history.

This is evidence for the design in the recovered **later FIX1 revision**. It is not the complete historical Exp3 executable, a verified full call-chain audit, or a hash match to the run that produced 14/16. The original result and reproducibility limitations are preserved. The public note intentionally excludes private paths, endpoints and unrelated capture contents.

Even with exact execution provenance, the following inference would still be invalid:

> compressed-state HC lost -> therefore selective external Root retrieval won

That comparison was not performed. State compression, replacement of history, update mechanics, prompt rules, control formatting and additional calls were bundled. A follow-up must separately compare raw history, lossy replacement and source-backed selective retrieval under matched conditions. Exp3 remains a negative result for the tested bundle and a motivation for this test, not retroactive positive validation of Root.

## 5. Atlas timing: a conditional break-even, not business ROI

The [six source rows](../benchmarks/project-atlas-v0.1/data/timing.csv) sum to:

| UI-reported thinking time | Native | Root |
|---|---:|---:|
| Four updates | 131 s | 569 s |
| Two retrievals | 570 s | 253 s |
| Observed total | 701 s | 822 s |

Under the explicitly hypothetical assumption that these per-operation means remain unchanged, an update adds 109.5 s for Root and a retrieval saves 158.5 s. With U updates and Q retrievals:

`Root - Native = 109.5 U - 158.5 Q`

The fitted timing proxy favors Root when `Q/U > 219/317`, approximately **0.691**. At four updates, the third comparable retrieval would cross that fitted threshold. That third retrieval was **not observed**.

See [the calculation and limitations](../benchmarks/project-atlas-v0.1/timing-break-even.md). The metric excludes full elapsed work, human preparation/review/repair, maintenance and money. Four heterogeneous updates and two retrievals do not establish a reusable cost function, uncertainty interval or production break-even.

## 6. Separate three hypotheses

**Conditional allocation hypothesis.** Some state/verification structures reduce relevant failures enough to justify their costs, while some procedural structures do not. Test this within defined task/model conditions.

**Method-by-state interaction hypothesis.** The benefit of maintained state may be larger when the method is self-designed than when an initial human guide is supplied. This is an optional stronger prediction, not a logical requirement of the core argument.

**Capability-scaling hypothesis.** Higher model capability reduces the optimal amount of method instruction and increases the optimal amount of state structure. This is not established. 'Optimal amount' needs a definition: token length, enforced steps, maintenance effort and state coverage are not equivalent. A more capable model could maintain better state with fewer tokens. Longer deployed task horizons could increase state requirements even if capability alone does not.

One model setting cannot identify a capability slope. Two model families do not cleanly identify one either: training, context handling, serving and instruction-following change together. A single-model 2x2 tests an interaction, not a capability derivative. Reusing a small near-ceiling case set across models is a diagnostic, not a decisive scaling study.

### A null interaction does not erase state value

Let A/B be no-maintained-Root outcomes without/with method guidance; C/D are their maintained-Root counterparts. On a predeclared higher-is-better outcome scale, define `I = (C-A) - (D-B)`.

The proposed prediction is I > 0. It describes greater marginal state benefit without guidance; equivalently, with guide=1 coding, the conventional state-by-guide interaction is negative. It is not automatically a claim of statistical complementarity.

For illustration only, A=.60, B=.65, C=.80, D=.85 gives I=0 while state improves both arms by .20. Thus 'no interaction means the whole thesis is only less prompting' is false. Positive, zero, reverse and uncertain interactions all remain reportable. A guide could also teach better state use, producing the opposite interaction.

## 7. Make outcome observation operational

The claim that outcome observability has no operational treatment is too broad. The existing [E001 protocol](https://github.com/Valon-Jang/Goal-Directed-Self-Structuring-AI/blob/research/e001-goal-vs-human-v01/experiments/E001/PROTOCOL.md) already specifies independent deterministic grading, hidden answer keys, evidence support, authority constraints, fact parity, version hashes, human labor categories and BLOCKED gates. Its [continuing charter](https://github.com/Valon-Jang/Goal-Directed-Self-Structuring-AI/blob/research/e001-goal-vs-human-v01/RESEARCH_CHARTER.md) prohibits manufacturing results or promoting missing evidence.

Bring those requirements into the public argument rather than creating a duplicate framework. For each consequential completion claim, identify the target outcome, authoritative scope/version, required evidence, evaluator, observation time and acceptance rule. Verify both the artifact/effect and the facts it rests on.

If evidence is absent, delayed or ambiguous, report UNVERIFIED or BLOCKED as appropriate. Do not treat 'no observed failure' or 'file created' as success. Safe reversible investigation may continue within existing authority; unsupported consequential actions may not. When no deterministic oracle is available, use a declared independent review/rubric and disclose uncertainty rather than inventing one.

## 8. Prior work and positioning

MemGPT (Packer et al., 2023/2024) already studies managed memory tiers beyond a model's context window. Anthropic's *Effective harnesses for long-running agents* (2025-11-26) explicitly connects more capable agents and longer tasks to cross-session continuity, external progress artifacts and tests; it also reports benefits from specific procedural guidance in its setting.

These sources do not establish the exact proposed capability derivatives. They do rule out a defensible blanket claim that nobody considers durable external state for increasingly autonomous agents, or that the industry only recommends fewer instructions. Exact novelty remains unestablished; no exhaustive priority review has been performed.

Primary references: [MemGPT](https://arxiv.org/abs/2310.08560) and [Anthropic long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

The useful differentiation to earn is **reproducible task-specific evidence, explicit failure boundaries, lifecycle economics and a workable delegation policy**, not an unsupported first-in-the-world claim.

## 9. Adopted changes and research governance

Adopt: a case-first common argument, separate claim/evidence levels, timing break-even with the correct metric, historical source audit with provenance limits, and a prospective method/state factorial design.

Modify: 'move all structure to state' becomes conditional functional allocation; 'failure proves navigation' becomes a mechanism hypothesis; 'two models prove a slope' becomes a controlled transfer/scaling program.

Reject: novelty by assertion; causal explanations of repository stars without evidence; forced physical repository merger; relabeling native project memory as no memory; changing an active experiment to fit the narrative.

Keep one canonical argument here and link distinct repositories for their independent protocols, implementation and evidence. Release labels such as Rebirth and Sidecar Work Graph remain implementation/history names, not extra theoretical prerequisites. Explanatory tree metaphors are optional teaching aids, not evidence. Goal Contract, source/authority distinctions, Save Gate and failure modes remain operationally meaningful.

No runtime, permissions, acceptance thresholds or frozen E001 treatment is changed by this note. No new paid inference, model efficacy trial or background automation was executed for this audit. The next experiment must follow the existing charter and readiness gates, with negative results preserved.

## Audit trail

Original Git blob identities inspected: Atlas results `d7153e066b620e573178c52d680ebc8468bf3d43`; timing CSV `268b67655d5072571d364d133fc425ade593aebf`; methodology `d68adbfb4216d3b9330116e71ea644af16ce3fd5`; Qwen Exp3 summary `76515ec34e92b7bdd5edcf340f43e8657115cde2`; Exp4 summary `93ce552472e4edee75a1d05d7cf2e731ed9bf1d4`; Exp5 summary `cfe12472842919bb5f63bfa20b4a9d1c6dfea2ca`; source/conflict checkpoint `df21c517b96290aa9863dfbf09dc64c98a4a44e0`; E001 protocol `81871e436388b830d4650913801ce5d4460e2ef9`.

These are content blob identities, not execution commit hashes. Original model runs were not repeated or independently re-graded during this audit; published counts were checked against their source summaries, and the timing arithmetic was recalculated.
