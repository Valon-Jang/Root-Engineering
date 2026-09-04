# Root Engineering 1.0 — Rebirth

> **Model is replaceable. Context is replaceable. Root persists. The thread continues.**

Root Engineering 1.0 — Rebirth separates a long-running AI project into three operational layers:

```text
CHAT TRANSCRIPT      = human-visible history
ACTIVE MODEL CONTEXT = compactable working memory
LOCAL ROOT           = durable canonical project state
```

The release targets an ordinary ChatGPT conversation with a writable chat-local workspace such as `/mnt/data`. It does not require a ChatGPT Project or Google Drive for routine operation.

## Major-version change

Root Engineering 0.x preserved project state across chats and models through an external canonical Root.

Rebirth adds a persistent-thread runtime:

```text
work in one chat
→ promote durable state into the Local Root
→ write a resumable Checkpoint
→ verify every required write
→ compact active model context
→ rehydrate from BOOT + ROOT + CHECKPOINT
→ continue the same chat
```

The chat transcript may remain visible to the human while the active model context is compacted. Rebirth does not claim that compaction deletes provider-side raw records or that `/mnt/data` survives every product/runtime lifecycle.

## Default local topology

```text
/mnt/data/root-engineering/
├── BOOT.md
├── PROTOCOL.md
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
├── sources/
│   └── INDEX.md
├── tools/
│   ├── rebirth_runtime.py
│   └── noop_boundary.py
└── scratch/
```

## The `압축해` contract

`압축해` is not a summarization-only command. It is a transaction:

```text
Persist → Checkpoint → Verify → Compact → Rehydrate
```

The visible progress language is intentionally simple:

```text
현재 작업을 저장 중입니다…
저장 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행할게.
```

If persistence or verification fails, compaction must not start.

## ROOT vs CHECKPOINT

`ROOT` stores durable project truth: purpose, current decisions, verified methods, operational constraints, and useful history.

`CHECKPOINT` stores transient continuation state: what is being done now, what just completed, what remains, and the exact next action.

This separation prevents temporary work-in-progress from polluting canonical knowledge while still allowing the task to resume after active-context replacement.

## Compaction priority

1. Use a supported native compact action only when the current host actually exposes it.
2. Otherwise use a zero-output tool/sampling boundary only when the same environment has already demonstrated that behavior and compaction can be verified.
3. Use bounded diagnostic pressure only for diagnosis, with small increments and immediate stop on success.
4. Never invent or call a private/internal RPC that is not exposed as a supported host capability.

## RC.1 deterministic runtime helper

The executable installer/runtime provides atomic local writes, identity and package validation, canonical-state hashing, resumable checkpoint creation, sealed compaction transactions, fail-closed completion, epoch accounting, and snapshot export.

A prepared transaction records both the canonical digest and Checkpoint hash. `complete-compact --observed` refuses to advance the epoch if either changed after preparation. Compaction therefore cannot be marked successful against a different state than the one that was saved.

## Release status

`1.0.0-rc.1` is a staged release candidate. It must not replace the stable 0.x installer until fresh-install, migration, persistence, repeated-compaction, and recovery acceptance tests pass.
