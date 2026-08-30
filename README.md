<p align="center">
  <img src="./assets/root-engineering-social-preview.png" alt="Root Engineering tree and circuit-root emblem" width="100%">
</p>

# Root Engineering for AI

> **Model is replaceable. Root persists.**

Root Engineering is a context-engineering methodology for preserving validated project knowledge, decisions, constraints, learning, and source relationships across AI sessions and models.

It addresses three recurring failures in long-running AI work:

- the same project context must be reconstructed repeatedly
- previous decisions are forgotten or contradicted
- outdated information is mixed with the current state

The goal is simple:

> **Make the next AI start from a better place than the previous one.**

[Install Root Engineering](#install-and-verify) · [See how it works](#how-it-works) · [Review the benchmark](#preliminary-benchmark) · [Experimental research](#experimental-research-shadow-carrier) · [Read the detailed reference](./docs/ROOT_ENGINEERING_REFERENCE.md)

---

## When Root Engineering Helps

Root Engineering is designed for work where:

- projects continue across many AI conversations
- important decisions must survive model or tool changes
- several sources contain overlapping or conflicting information
- people repeatedly explain what has already been decided
- outdated facts can cause incorrect actions
- source provenance and decision history matter

It is usually unnecessary for one-off prompts, disposable tasks, or information that can be reconstructed cheaply.

---

## Install and Verify

The current reference implementation uses **ChatGPT Project + Google Drive live app access**.

1. Open the [canonical English installer](./installer/ROOT_ENGINEERING_INSTALLER.md).
2. Attach it to the first chat of a new ChatGPT Project.
3. Say: **“Read the package and install it.”**
4. Follow the prompts for Google Drive preflight, Root creation, Project Binding, and fresh-chat verification.

Korean users may use the separate [Korean installer](./installer/ROOT_ENGINEERING_INSTALLER_KO.md).

The installer does more than describe a folder structure. It checks storage access, creates the Canonical Root, generates project-specific instructions, connects the Root to the project, and runs a fresh-chat acceptance test.

Installer v0.1.11 is a single-file package for installation, verification, repair, and upgrade. Shared operating behavior lives in the Global Protocol, while ChatGPT Project Instructions contain only the project-specific connection block. A complete-coverage Knowledge Lookup inside ROOT resolves named areas before any full-Branch existence scan. When supported, independent startup reads run concurrently and an existing target read is reused for an optimistic, revision-guarded document batch; a conflict triggers the re-read instead of every successful write. Routine writes use the atomic response and returned revision, while critical changes receive one affected-scope verification read. Scope-preserving merge rules keep authority, configuration, revision, material, Lot, Sub-Lot, Serial, timing, exceptions, and unresolved issues distinct. Upgrade queues remain explicit by installed level and report only the paths actually changed.

### What the installer establishes

```text
Canonical Root
├── Knowledge Lookup [routing index]
├── Foundation
├── Current Knowledge
├── Learned Knowledge
└── History
```

The fresh-chat test verifies that a new conversation can identify the Project Binding, retrieve the Root, use the complete-coverage Lookup, navigate to Current Knowledge, and continue from the persisted project state.

This creates the path from methodology to operation:

```text
Install
  ↓
Create Canonical Root
  ↓
Bind Project
  ↓
Verify in a Fresh Chat
  ↓
Use and Update the Root
```

→ [Open the English installer](./installer/ROOT_ENGINEERING_INSTALLER.md)

---

## How It Works

```text
Canonical Root
      ↓
Selective Context
      ↓
Reasoning / Action
      ↓
Verification
      ↓
Minimum Root Patch
      ↓
Future Session
```

A Root keeps one authoritative representation of the project's currently accepted state.

The AI starts from a Root Map and reads only the branches relevant to the current task. After the work is completed and verified, it selectively preserves results that materially improve future reasoning.

> **Navigate the Root. Do not dump the Root.**

### Without Root vs. with Root

| Without Root | With Root |
|---|---|
| Decisions remain scattered across chats and documents | Accepted decisions have a canonical location |
| Each session reconstructs project context | Each session starts from validated current state |
| Old and new information may be mixed | Superseded information is separated from current knowledge |
| More context is loaded indiscriminately | Only task-relevant branches are retrieved |
| Useful lessons disappear after execution | Verified reusable lessons can persist |
| Changing models feels like restarting the project | Project knowledge remains external to the model |

---

## Root and Loop

> **Loop Engineering improves the current run.**<br>
> **Root Engineering improves the next run.**

Loops improve execution through iteration: attempt, evaluate, correct, and retry.

Roots determine what validated knowledge and decisions should survive after those loops finish. The two approaches are complementary.

---

## Preliminary Benchmark

[Project Atlas Benchmark v0.1](./benchmarks/project-atlas-v0.1/) connects the methodology to an inspectable experiment.

It is a manual paired comparison between:

- **Native condition:** GPT-5.6 Sol (High)
- **Root Engineering condition:** GPT-5.6 Sol (High)

The benchmark designer and prompt submitter was **GPT-5.6 Sol (XHigh)**. Native and Root are the actual compared conditions and use matched model and reasoning settings.

Both conditions performed similarly on simple continuity tasks. The first divergence appeared at **Stage 2**, when exact configuration scope and source provenance became important. Stage 5 recorded a selective-retrieval failure that changed the Native decision path, while Root preserved the expected state. **Stage 4 and Stage 6 remained ties.**

Two measured complex retrievals showed lower UI-reported thinking time in the Root condition, but Root required substantially more update and canonicalization time. The observed workload did **not** demonstrate an end-to-end Root speed advantage.

These are **preliminary manual small-n observations, not statistical proof**.

### Inspect the experiment

- [Benchmark overview](./benchmarks/project-atlas-v0.1/README.md)
- [Methodology and controls](./benchmarks/project-atlas-v0.1/methodology.md)
- [Stage 0–6 experiment map](./benchmarks/project-atlas-v0.1/experiment-map.md)
- [Observed results](./benchmarks/project-atlas-v0.1/results.md)
- [Timing interpretation](./benchmarks/project-atlas-v0.1/timing.md)
- [Raw timing data](./benchmarks/project-atlas-v0.1/data/timing.csv)
- [Submitted prompts](./benchmarks/project-atlas-v0.1/prompts/README.md)

The full path is therefore:

```text
Methodology
  ↓
Installer
  ↓
Fresh-Chat Verification
  ↓
Paired Benchmark
  ↓
Results and Failure Analysis
  ↓
Methodology Revision
```

---

## Experimental Research: Shadow Carrier

A separate experimental track is testing whether deterministic Interceptors can accelerate a strong adaptive AI workflow **without replacing its reasoning or lowering quality**.

The current Shadow Carrier hypothesis is simple:

```text
Normal reasoning performs the current step
        ↓
Interceptors pre-execute likely next read-only actions
        ↓
Unused results stay outside model context
        ↓
Compatible hit → use cache
Miss → fall back to Normal
```

This research is intentionally labeled experimental. Early benchmarks found both positive and negative cases: parallel heterogeneous parsing can reduce machine latency, while naive broad web retrieval can be faster yet lose on evidence quality. The current direction preserves Normal adaptive search and uses Interceptors as a speculative latency-hiding layer rather than as five independent LLM subagents.

- [Live Shadow Carrier research log](./research/SHADOW_CARRIER_RESEARCH_LOG.md)
- [Shadow Carrier operating protocol](./docs/SHADOW_CARRIER_OPERATING_PROTOCOL.md)

Experimental claims are promoted into the stable methodology only after reproducible evidence accumulates.

---

## Minimal Root

A Root can begin with four knowledge branches and one map:

```text
ROOT
├── Foundation
├── Current Knowledge
├── Learned Knowledge
└── History
```

- **Foundation** preserves stable purpose, principles, boundaries, and human intent.
- **Current Knowledge** contains current facts, status, decisions, constraints, and unresolved issues.
- **Learned Knowledge** contains validated reusable methods and failure lessons.
- **History** preserves superseded states that still matter for understanding change.
- **ROOT** acts as the map and digest used to find the required branch.

Start small. Create new branches because real retrieval patterns require them, not because a larger taxonomy looks complete.

---

## Core Principles

1. **Preserve selectively:** Save only what materially improves future reasoning.

2. **Keep one canonical current state:** Do not duplicate current truth across competing locations.

3. **Separate knowledge from models:** Project knowledge should survive model and tool replacement.

4. **Read selectively:** Load only the branches required for the current task.

5. **Verify before persistence:** Model inference must not silently become project fact.

6. **Patch minimally and prune locally:** Update the smallest necessary area and clean knowledge when interacting with it.

The save gate is:

> **Would losing this information materially increase the chance that a future AI must rediscover it, make a worse decision, or repeat a previous failure?**

---

## What Root Engineering Is Not

Root Engineering is not a transcript archive and does not mean saving everything.

It does not prescribe a specific model, database, vector store, graph, or agent framework. Those technologies may participate in an implementation, but the methodology focuses on the knowledge lifecycle around them:

```text
Acquire → Evaluate → Use → Verify → Persist Selectively → Retrieve Selectively → Update / Prune
```

It complements AI memory and RAG:

- a memory system asks what information can be retrieved later
- RAG asks which existing information should be retrieved now
- Root Engineering also asks what deserves to become authoritative project knowledge after the interaction

---

## Documentation

The [detailed methodology reference](./docs/ROOT_ENGINEERING_REFERENCE.md) contains the full definitions, conceptual model, operating rules, comparisons, examples, roadmap, philosophy, and terminology that previously lived in this README.

Start with the path that matches your goal:

| Goal | Document |
|---|---|
| Install and verify a working Root | [English installer](./installer/ROOT_ENGINEERING_INSTALLER.md) |
| Install using Korean user guidance | [Korean installer](./installer/ROOT_ENGINEERING_INSTALLER_KO.md) |
| Understand the complete methodology | [Detailed reference](./docs/ROOT_ENGINEERING_REFERENCE.md) |
| Review the paired experiment | [Project Atlas Benchmark v0.1](./benchmarks/project-atlas-v0.1/) |
| Follow experimental Shadow Carrier research | [Research log](./research/SHADOW_CARRIER_RESEARCH_LOG.md) |
| Read the Shadow Carrier operating protocol | [Operating protocol](./docs/SHADOW_CARRIER_OPERATING_PROTOCOL.md) |
| Reproduce the benchmark prompts | [Prompt package](./benchmarks/project-atlas-v0.1/prompts/README.md) |

---

## Current Status

Root Engineering is an early-stage methodology and reference architecture.

Current work focuses on:

- testing model-independent persistence
- reducing context reconstruction
- improving selective retrieval
- validating write, verification, and pruning rules
- expanding reproducible before/after benchmarks
- testing speculative Interceptor / Shadow Carrier acceleration as an experimental track
- testing portable installation across AI systems

The methodology is expected to evolve through practical use, documented failure cases, and measurable evaluation.

---

## Contributing

Useful contributions include:

- implementation patterns
- failure cases
- benchmark designs and reproductions
- storage adapters
- retrieval and pruning strategies
- model portability tests
- practical case studies

Strong evidence is more valuable than additional terminology.

---

## Citation

If you reference Root Engineering as defined in this repository, cite this repository and the specific release or commit used.

A formal citation file and versioned releases will be added as the methodology stabilizes.

---

## License

Except where otherwise noted, the methodology, documentation, installers, and benchmark materials in this repository are licensed under the [Creative Commons Attribution 4.0 International License](./LICENSE).

Copyright © 2026 Valon-Jang.

When sharing or adapting the material, provide appropriate attribution, link to this repository and the license, and indicate whether changes were made.

---

## About the Name

The phrase **Root Engineering** may appear in unrelated technical, biological, or engineering contexts.

In this repository, it specifically refers to the methodology defined here for persistent external knowledge architecture around AI systems.

---

> # Model is replaceable. Root persists.

An AI project should not lose its accumulated understanding every time the model, session, agent, or tool changes.
