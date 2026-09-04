<p align="center">
  <img src="./assets/root-engineering-social-preview.png" alt="Root Engineering tree and circuit-root emblem" width="100%">
</p>

# Root Engineering for AI — 1.0 Rebirth

> **Model is replaceable. Context is replaceable. Root persists.**

Root Engineering is a context-engineering methodology for preserving validated project knowledge, decisions, constraints, learning, and source relationships around AI systems.

**Root Engineering 1.0 — Rebirth** extends the original idea: not only the model, but also the model's active conversation context can be treated as replaceable working memory.

The Chat-native Rebirth adapter separates:

```text
Chat Transcript      = human-visible history
Active Model Context = compactable working memory
Checkpoint           = immediate resume state
Local ROOT           = durable canonical project state
```

The goal is now:

> **Preserve project truth, compact working context when safe, and continue the same human-facing Chat.**

[Install Rebirth](#install-and-verify) · [Read the Rebirth architecture](./docs/ROOT_ENGINEERING_1.0_REBIRTH.md) · [Review the benchmark](#preliminary-benchmark) · [Read the detailed reference](./docs/ROOT_ENGINEERING_REFERENCE.md)

---

## Complete Chat Runtime — “완성형 Chat”

Rebirth calls its ChatGPT-native mode a **Complete Chat Runtime** — informally, a **완성형 Chat**.

This is Root Engineering terminology, not an official OpenAI product name or feature claim. It is not a custom API client, CLI wrapper, coding-agent workspace, or external chat server. It is an operating pattern around one ordinary ChatGPT Chat:

```text
one ordinary ChatGPT Chat
+ retained human-visible transcript
+ compactable active model context
+ chat-local ROOT
+ resumable CHECKPOINT
+ optional compact-time recovery mirror
= Complete Chat Runtime
```

> **The Chat remains the workspace. Context becomes maintainable. Root becomes the project memory.**

### Recovery synchronization without active-work latency

```text
ordinary active work        → Local ROOT only
압축해 / compact             → synchronize configured latest recovery copy
백업해 / backup              → one explicit backup without compaction
scheduled / idle / timer     → disabled
background synchronization   → disabled
```

Local state is persisted and verified before any external tool boundary. Optional backup failure is visible and recorded as pending; strict `백업하고 압축해` fails closed.

→ [Explicit compact-time recovery policy](./docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md)

---

## What changed in 1.0 — Rebirth

Root Engineering 0.x primarily solved cross-session continuity by keeping project state outside the model, with ChatGPT using Google Drive as a canonical store.

Rebirth adds a Chat-native runtime:

```text
ordinary ChatGPT Chat
        ↓
/mnt/data/root-engineering/
        ↓
ROOT + knowledge owners + CHECKPOINT
        ↓
Persist → Verify → Synchronize configured recovery copy → Compact → Rehydrate
        ↓
continue the same Chat
```

For the default ChatGPT Rebirth adapter:

- **ChatGPT Project is not required.**
- **Google Drive is not required.**
- Chat-local `/mnt/data` is the primary current-runtime store when it is writable.
- Google Drive, Git, and exported bundles become optional backup/recovery adapters.
- `runtime/CHECKPOINT.md` is a first-class owner for the current work-in-progress state.
- the command `압축해` / `compact` means **save durable state → refresh checkpoint → verify → synchronize the configured recovery copy → compact → rehydrate**, not merely "summarize the chat."
- **save failure blocks deliberate compaction.**

Rebirth does not claim that `/mnt/data` survives every future runtime, nor that every ChatGPT thread exposes the same compaction trigger. Host-specific compaction paths are capability-gated and must be verified in their actual scope.

→ [Root Engineering 1.0 Rebirth architecture](./docs/ROOT_ENGINEERING_1.0_REBIRTH.md)

---

## Origin

Root Engineering did not start as a methodology. I was using ChatGPT and Claude heavily — often pushing high-reasoning models until both plans hit their limits. ChatGPT Chat still gave me a separate surface to experiment with, so I started asking a different question: **how much smarter could ordinary chat feel if I improved the external context instead of just spending more model?**

That led to Markdown as manually maintained project memory. The first version was primitive: upload the MD files, talk with the model, replace the files when things changed. Even that was surprisingly powerful.

The next bottleneck was predictable: manually moving and replacing the MD files. Root Engineering formalized what should be read, verified, updated, preserved, and pruned.

Rebirth came from the next bottleneck: long-lived Chat threads themselves. Once human-visible transcript history, active model context, and durable Root state were treated as different resources, a new path appeared — **keep the project thread, replace the active context, preserve the Root.**

---

## Install and Verify

### ChatGPT — Rebirth 1.0.0 (default)

1. Open the [canonical Rebirth installer](./installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md).
2. Attach it to an ordinary ChatGPT Chat with a writable local workspace.
3. Say: **“Read the package and install it.”**
4. The installer verifies the chat-local workspace, creates the Local Root, and runs local consistency checks.

Korean users can use [ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md](./installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md).

Default local layout:

```text
/mnt/data/root-engineering/
├── BOOT.md
├── ROOT.md
├── MANIFEST.json
├── knowledge/
│   ├── FOUNDATION.md
│   ├── CURRENT.md
│   ├── LEARNED.md
│   ├── OPERATIONAL.md
│   └── HISTORY.md
└── runtime/
    ├── CHECKPOINT.md
    ├── STATE.json
    └── CAPABILITIES.json
```

The package includes explicit guards for local write verification, save-before-compact, capability-scoped compaction, context epochs, selective boot, Operational Memory, and Checkpoint-based rehydration.

Validation tools:

- [Rebirth installer validator](./tools/validate_rebirth_installer.py)
- [Rebirth local runtime self-test](./tools/rebirth_local_selftest.py)

### ChatGPT Project + Google Drive — legacy/external adapter

The existing Drive-native 0.x installer remains available for existing installations and as an external persistence/recovery path:

- [ChatGPT Drive installer v0.1.12](./installer/ROOT_ENGINEERING_INSTALLER.md)
- [ChatGPT Drive installer v0.1.12 — Korean](./installer/ROOT_ENGINEERING_INSTALLER_KO.md)

A Drive-based Root can be migrated into a Rebirth Local Root while preserving proven Project/Root identity. Large source documents do not need to be copied automatically; their Drive IDs/URLs may remain external evidence routes.

### Codex

Install the repository's standalone `root-engineering` Skill with Codex's built-in installer:

```text
$skill-installer install the skill from https://github.com/Valon-Jang/Root-Engineering/tree/main/installer/codex/root-engineering
```

- [Codex installer and acceptance guide](./installer/ROOT_ENGINEERING_CODEX_INSTALLER.md)
- [Codex 설치 및 검증](./installer/ROOT_ENGINEERING_CODEX_INSTALLER_KO.md)
- [Installable Skill folder](./installer/codex/root-engineering/)

### Claude Project + Google Drive

The Claude adapter remains available for environments where Drive-backed Markdown persistence is the appropriate runtime:

- [Claude installer](./installer/ROOT_ENGINEERING_CLAUDE_INSTALLER.md)
- [Claude package folder](./installer/claude/root-engineering/)

---

## How Rebirth works

```text
User works in one primary Chat
        ↓
New durable state?
        ↓ yes
Patch the smallest correct Root owner
        ↓
Refresh CHECKPOINT when context maintenance is requested
        ↓
Verify writes
        ↓
Compact active model context only through a supported or verified path
        ↓
Rehydrate BOOT + CHECKPOINT + only required owners
        ↓
Continue the same Chat
```

### The hard invariant

> **SAVE FAILURE = NO COMPACT**

A compaction request is a state transaction. If required Root/Checkpoint persistence cannot be verified, Rebirth keeps the active context and stops instead of risking silent state loss.

### Root vs Checkpoint

`ROOT / knowledge/*` stores durable project truth.

`runtime/CHECKPOINT.md` stores the temporary resume state of the current work:

```text
Current goal
Completed work relevant to resumption
Current transient state
Next actions
Pending blockers
Resume instruction
```

This prevents short-lived work progress from polluting long-term project knowledge while still allowing a compacted context to resume immediately.

### Context epochs

Each confirmed compaction advances the runtime context epoch:

```text
Epoch 0 → Epoch 1 → Epoch 2 → ...
```

This provides a measurable basis for long-horizon tests such as resume accuracy, decision retention, no-repeat behavior, latency/context trend, and quality loss across repeated compactions.

---

## The compaction path

Rebirth deliberately does not invent private ChatGPT endpoints.

Priority order:

1. **Native supported compact action** — only when the current host actually exposes one.
2. **Verified zero-output tool/sampling boundary** — only when the same environment has demonstrated that behavior and success can be verified.
3. **Bounded diagnostic pressure** — diagnosis only, small increments, immediate stop on success.

The related public experiment is maintained separately in [persistent-project-thread](https://github.com/Valon-Jang/persistent-project-thread). In the tested long-lived ChatGPT thread, trigger reduction reached a zero-output `pass` boundary after earlier oversized pressure experiments. That observation is environment-specific evidence, not a universal ChatGPT guarantee.

---

## A practical workflow: Chat → Root → execution

1. **Think in Chat first.** Turn a vague idea into a concrete one.
2. **Use Question-Driven Deepening.** Ask only what can change the next decision.
3. **Persist useful state.** Confirmed facts, decisions, constraints, important unresolved items, and verified lessons go to the correct Root owner.
4. **Keep transient work in Checkpoint.** Do not turn every task-progress detail into durable knowledge.
5. **Compact safely when needed.** Save → verify → synchronize the configured recovery copy → compact → rehydrate.
6. **Use isolated execution environments where appropriate.** Codex, agents, destructive tests, or security boundaries may still use separate execution threads.
7. **Feed verified results back into the Root.**

> **Chat shapes the work. Execution tools perform isolated work. Root preserves truth. Checkpoint preserves immediate continuity.**

---

## Minimal Root

The durable knowledge tree remains intentionally small:

```text
ROOT
├── Foundation
├── Current Knowledge
├── Learned Knowledge
├── Operational Memory
└── History
```

- **Foundation** — stable purpose, principles, boundaries, Human Intent.
- **Current Knowledge** — currently valid facts, decisions, constraints, status, unresolved issues.
- **Learned Knowledge** — verified reusable methods and generalized lessons.
- **Operational Memory** — exact repeated-operation keys, failed-path constraints, verified hot paths, required evidence.
- **History** — superseded states that still matter for transition, rollback, or failure prevention.

Create additional children only when real independent retrieval/update patterns require them.

> **Navigate the Root. Do not dump the Root.**

---

## Core principles

1. **Preserve selectively.** Save only what materially improves future reasoning or execution.
2. **Keep one canonical current state.** Do not duplicate current truth across competing owners.
3. **Separate project knowledge from models and active context.** Both are replaceable execution resources.
4. **Separate durable Root from transient Checkpoint.**
5. **Read selectively.** Load only what the current task needs.
6. **Verify before persistence.** Model inference must not silently become project fact.
7. **Reuse verified successful paths and preserve failed paths as constraints.**
8. **Patch minimally and prune locally.**
9. **Do not compact before required state is safely persisted.**

The save gate remains:

> **Would losing this information materially increase the chance that a future AI must rediscover it, make a worse decision, or repeat a previous failure?**

---

## Root and Loop

> **Loop Engineering improves the current run.**  
> **Root Engineering improves what survives the run.**

Rebirth adds:

> **Context maintenance keeps the human-facing project thread viable without making raw conversation history the project database.**

---

## Preliminary benchmark

[Project Atlas Benchmark v0.1](./benchmarks/project-atlas-v0.1/) remains the original paired Root-vs-native continuity experiment.

It found early divergence when exact configuration scope and source provenance became important, while also showing that Root maintenance itself has non-trivial update/canonicalization cost. These are preliminary small-n manual observations, not statistical proof.

Inspect:

- [Benchmark overview](./benchmarks/project-atlas-v0.1/README.md)
- [Methodology and controls](./benchmarks/project-atlas-v0.1/methodology.md)
- [Observed results](./benchmarks/project-atlas-v0.1/results.md)
- [Timing interpretation](./benchmarks/project-atlas-v0.1/timing.md)

Rebirth adds a new benchmark direction: repeated `Persist → Checkpoint → Compact → Rehydrate` cycles in the same primary Chat, measuring state accuracy and degradation across context epochs.

---

## What Root Engineering is not

Root Engineering is not a transcript archive and does not mean saving everything.

It does not prescribe one database, vector store, graph, or agent framework. Rebirth also does not claim that a ChatGPT-local filesystem is universally permanent or that compaction physically deletes transcript/provider records.

The methodology focuses on the knowledge and runtime lifecycle:

```text
Acquire
→ Evaluate
→ Use
→ Verify
→ Persist Selectively
→ Checkpoint Transient Work
→ Compact Working Context When Safe
→ Retrieve Selectively
→ Update / Prune
```

---

## Documentation

| Goal | Document |
|---|---|
| Install Rebirth in ordinary ChatGPT Chat | [Rebirth installer](./installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md) |
| Rebirth 한글 설치 | [Rebirth 한글 설치기](./installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md) |
| Understand Rebirth architecture | [Rebirth 1.0 architecture](./docs/ROOT_ENGINEERING_1.0_REBIRTH.md) |
| Existing ChatGPT Drive installation | [Legacy Drive installer](./installer/ROOT_ENGINEERING_INSTALLER.md) |
| Install with Codex | [Codex installer](./installer/ROOT_ENGINEERING_CODEX_INSTALLER.md) |
| Install with Claude + Drive | [Claude installer](./installer/ROOT_ENGINEERING_CLAUDE_INSTALLER.md) |
| Detailed original methodology | [Detailed reference](./docs/ROOT_ENGINEERING_REFERENCE.md) |
| Review the original paired experiment | [Project Atlas Benchmark](./benchmarks/project-atlas-v0.1/) |

---

## Current status

**Root Engineering 1.0.0 — Rebirth** is the current Chat-native architecture.

Verified locally for the release package:

- Rebirth installer structural validator: PASS
- chat-local Root file creation: PASS
- identity read-back across canonical owners: PASS
- Checkpoint independent update: PASS
- save-failure compaction guard simulation: PASS
- context epoch increment only after simulated confirmation: PASS

Host-specific compaction remains capability-gated. The earlier long-lived ChatGPT experiment provides evidence for a zero-output boundary fallback in that tested environment, while repeated multi-epoch quality testing remains an open benchmark target.

---

## Contributing

Useful contributions include:

- repeated-compaction experiments
- host compaction capability observations
- state-loss and recovery failure cases
- storage adapters
- benchmark designs and reproductions
- retrieval/pruning improvements
- model/runtime portability tests
- practical long-horizon case studies

Strong evidence is more valuable than additional terminology.

---

## License

Except where otherwise noted, the methodology, documentation, installers, and benchmark materials in this repository are licensed under the [Creative Commons Attribution 4.0 International License](./LICENSE).

Copyright © 2026 Valon-Jang.

---

> # Model is replaceable. Context is replaceable. Root persists.
>
> **The transcript may remain. The active context may die. The checkpoint bridges the transition. The Root preserves truth. The same project continues.**
