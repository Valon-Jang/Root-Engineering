<p align="center">
  <img src="./assets/root-engineering-social-preview.png" alt="Root Engineering tree and circuit-root emblem" width="100%">
</p>

# Root Engineering for AI — 1.0 Rebirth

> **Model is replaceable. Context is replaceable. Root persists.**

Root Engineering is a method for preserving validated project knowledge, decisions, constraints, reusable learning, operational experience, and source relationships outside transient model context.

**Root Engineering 1.0 — Rebirth** extends the original idea to the lifetime of an ordinary ChatGPT conversation. The human-facing Chat can remain the project workspace while the model's active context is checkpointed, compacted, and rehydrated.

[Install Rebirth](#install) · [Read the architecture](./docs/ROOT_ENGINEERING_1.0_REBIRTH.md) · [Read the backup policy](./docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md) · [Review the original benchmark](./benchmarks/project-atlas-v0.1/)

---

## Complete Chat Runtime — “완성형 Chat”

Rebirth calls its ChatGPT-native operating mode a **Complete Chat Runtime** — informally, a **완성형 Chat**.

This is Root Engineering terminology, not an official OpenAI product name or feature claim. It is also not a custom API client, CLI wrapper, coding-agent workspace, or external chat server. It is an operating pattern built around one ordinary ChatGPT Chat:

```text
one ordinary ChatGPT Chat
+ retained human-visible transcript
+ compactable active model context
+ chat-local ROOT
+ resumable CHECKPOINT
+ optional compact-time recovery mirror
= Complete Chat Runtime
```

The architecture separates resources that conventional chat usage often treats as one:

```text
Chat Transcript      = history the human can inspect
Active Model Context = replaceable working memory for inference
CHECKPOINT            = exact state needed to resume the current task
Local ROOT            = durable canonical project truth and routing
Recovery Mirror       = optional off-runtime backup for restore
```

The key product-level idea is simple:

> **The Chat remains the workspace. Context becomes maintainable. Root becomes the project memory.**

A long project no longer has to choose only between one increasingly heavy thread and many fragmented replacement chats.

---

## The Rebirth transaction

The command `압축해` / `compact` is not interpreted as “write a summary.” It opens an explicit maintenance transaction:

```text
Persist new durable state to the correct ROOT owner
→ refresh runtime/CHECKPOINT.md
→ verify and seal local state
→ synchronize the configured latest recovery copy
→ compact active model context through a supported or verified path
→ verify compaction
→ increment context epoch
→ rehydrate only the minimum required state
→ continue the same Chat
```

Hard invariant:

> **SAVE FAILURE = NO COMPACT**

If required Local ROOT or CHECKPOINT persistence cannot be verified, Rebirth preserves the current context and stops.

### Backup cadence: explicit compact-time only

The default 1.0.0 policy deliberately disables scheduled, idle, timer-based, and background backup synchronization.

```text
ordinary active work        → Local ROOT only
압축해 / compact             → update configured external latest recovery copy
백업해 / backup              → one explicit backup without compaction
백업하고 압축해              → external verification is required before compaction
```

Why:

- connector latency should not slow active work;
- a separately scheduled runtime may not see the same chat-local `/mnt/data`;
- `압축해` already provides a clear, user-controlled maintenance boundary;
- Local state can be sealed before an external tool call creates another host sampling boundary.

If the recovery bundle hash is unchanged, the remote write may be skipped. Optional backup failure during ordinary `압축해` is reported and recorded as pending; verified Local ROOT remains authoritative. Strict `백업하고 압축해` fails closed.

→ [External recovery synchronization policy](./docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md)

---

## Install

### ChatGPT — Rebirth 1.0.0

1. Open the [canonical Rebirth installer](./installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md).
2. Attach it to an ordinary ChatGPT Chat with a writable local workspace.
3. Say: **“Read the package and install it.”**
4. The installer verifies the workspace, creates the Local ROOT, installs the transaction guard, and validates the structure.

Korean installer: [ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md](./installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md)

Default layout:

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
├── runtime/
│   ├── CHECKPOINT.md
│   ├── STATE.json
│   └── CAPABILITIES.json
├── tools/
├── sources/
└── scratch/
```

The ChatGPT Project surface and Google Drive are not required for normal Rebirth operation. Chat-local `/mnt/data` is the preferred current-runtime store when writable, but Rebirth does **not** claim that it survives every future product/runtime lifecycle. Drive, Git, and exported bundles remain optional backup, migration, collaboration, and recovery adapters.

---

## Compaction capability ladder

Rebirth does not invent private ChatGPT endpoints.

1. Use an explicit native compact action only when the current host actually exposes and supports it.
2. Otherwise use exactly one zero-output tool/sampling boundary only when matching-scope evidence has already verified that path and success can be observed.
3. Use bounded pressure only for diagnosis, increasing gradually and stopping immediately on success.
4. If compaction cannot be verified, stop rather than claiming success.

The reference no-op is simply `pass`; the useful event is the host boundary, not the Python statement. Large synthetic output is retained as experiment history, not the normal path.

Research provenance: [Persistent Project Thread](https://github.com/Valon-Jang/persistent-project-thread)

---

## Minimal durable Root

```text
ROOT
├── Foundation
├── Current Knowledge
├── Learned Knowledge
├── Operational Memory
└── History
```

- **Foundation** — durable purpose, principles, boundaries, and Human Intent.
- **Current Knowledge** — currently valid facts, decisions, status, constraints, and unresolved items.
- **Learned Knowledge** — verified reusable methods and generalized lessons.
- **Operational Memory** — exact operation keys, failed-path constraints, verified hot paths, and required evidence.
- **History** — superseded state that still matters for transition, rollback, or failure prevention.
- **CHECKPOINT** — current resume state; deliberately separate from durable Root knowledge.

> **Navigate the Root. Do not dump the Root.**

---

## Core rules

1. Preserve selectively; do not archive the entire transcript into Root.
2. Keep one canonical current state.
3. Separate durable Root knowledge from transient CHECKPOINT state.
4. Read only the owners required for the current task.
5. Verify before persistence.
6. Preserve known failure paths as constraints and promote only verified replacements as hot paths.
7. Patch minimally and prune locally.
8. Persist and verify before deliberate compaction.
9. Advance context epoch only after compaction is actually observed.
10. Keep routine external-backup latency out of active work; synchronize at explicit maintenance boundaries.

Save gate:

> **Would losing this information materially increase the chance that a future AI must rediscover it, make a worse decision, or repeat a previous failure?**

---

## Other adapters

Rebirth is the default ChatGPT-native adapter. Existing adapters remain valid:

- [ChatGPT Project + Google Drive v0.1.12](./installer/ROOT_ENGINEERING_INSTALLER.md)
- [Codex installer](./installer/ROOT_ENGINEERING_CODEX_INSTALLER.md)
- [Claude + Google Drive installer](./installer/ROOT_ENGINEERING_CLAUDE_INSTALLER.md)

The kernel is storage-independent; adapters differ in persistence and execution contracts.

---

## Validation and status

Root Engineering remains an evidence-driven early-stage methodology. Rebirth's deterministic package tests cover Local ROOT creation, identity consistency, failure-safe writes, CHECKPOINT separation, save-failure compaction blocking, compact-time backup policy, and context-epoch advancement only after confirmed compaction.

Repeated real-host multi-epoch quality, latency, and retrieval degradation remain open benchmark targets.

- [Rebirth architecture](./docs/ROOT_ENGINEERING_1.0_REBIRTH.md)
- [Rebirth 1.0.0 release note](./docs/releases/v1.0.0-rebirth.md)
- [Detailed original methodology reference](./docs/ROOT_ENGINEERING_REFERENCE.md)
- [Project Atlas benchmark](./benchmarks/project-atlas-v0.1/)
- [Previous full README preserved for history](./docs/archive/README_REBIRTH_1.0_PRE_EXPLICIT_COMPACT.md)

---

## License

Except where otherwise noted, methodology, documentation, installers, and benchmark materials are licensed under the [Creative Commons Attribution 4.0 International License](./LICENSE).

Copyright © 2026 Valon-Jang.

---

> # Model is replaceable. Context is replaceable. Root persists.
>
> **The transcript may remain. The active context may die. The checkpoint bridges the transition. The Root preserves truth. The same project continues.**
