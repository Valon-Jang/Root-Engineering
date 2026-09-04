# Root Engineering 1.0 — Rebirth

## Major-version change

Root Engineering 0.x focused on preserving validated project knowledge across models, sessions, and tools.

Root Engineering 1.0 adds a second replaceable resource: **active conversation context**.

> **Model is replaceable. Context is replaceable. Root persists.**

The Rebirth goal is not to make a transcript itself become the project database. It separates project continuity into distinct layers so a long-running human-facing Chat can continue even when the model's working context is compacted.

## Four operational layers

```text
CHAT TRANSCRIPT
= human-visible history

ACTIVE MODEL CONTEXT
= transient working memory for inference

CHECKPOINT
= immediate resume state across context reduction

LOCAL ROOT
= durable canonical project truth and routing
```

The key new distinction from 0.x is `CHECKPOINT`.

Root is for knowledge that deserves to survive future tasks. Checkpoint is for information that must survive the next context transition but may become irrelevant once the current task ends.

## Chat-native default

The default ChatGPT adapter uses:

```text
/mnt/data/root-engineering/
```

and does not require:

- ChatGPT Project;
- Project Instructions;
- Google Drive;
- an external database.

This does **not** mean `/mnt/data` is claimed to be permanently durable across every future runtime. Rebirth treats external storage as optional backup/recovery adapters rather than the mandatory runtime store.

## Canonical layout

```text
root-engineering/
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
├── sources/
└── scratch/
```

## The Rebirth transaction

The user command `압축해` / `compact` is not interpreted as "write a summary." It is a state-preservation transaction:

```text
Persist durable state
→ Refresh CHECKPOINT
→ Verify writes
→ Compact active context
→ Verify compaction
→ Increment context epoch
→ Rehydrate minimal required state
→ Continue the same Chat
```

### Critical invariant

> **SAVE FAILURE = NO COMPACT**

If required Root or Checkpoint persistence is not verified, deliberate compaction is blocked.

This prevents context reduction from racing ahead of state durability.

## Compaction capability ladder

Rebirth does not invent host internals.

1. **Native supported compact action** — use only when the current host actually exposes one.
2. **Verified zero-output boundary fallback** — use only under conditions where the same environment has demonstrated host auto-compaction at a tool/sampling boundary and success can be verified.
3. **Bounded diagnostic pressure** — diagnostic-only, small increments, stop immediately on success.

Large disposable output is retained as research evidence, not the normal hot path.

The separate `persistent-project-thread` experiment established the operational motivation for this ladder and showed that, in the tested long-lived ChatGPT thread, zero-output tool boundaries were sufficient once the thread appeared already eligible for host auto-compaction.

## Context epochs

`runtime/STATE.json` tracks context lifecycle separately from project truth.

```text
Epoch 0
  ↓ confirmed compaction
Epoch 1
  ↓ confirmed compaction
Epoch 2
  ...
```

This creates a measurable unit for long-horizon experiments:

- compaction count;
- resume accuracy;
- decision retention;
- latency/context trend where observable;
- quality loss across repeated compactions.

## Storage adapters

Rebirth separates the method from storage:

```text
Root Engineering Kernel
├── Chat-local /mnt adapter     ← default ChatGPT runtime
├── Google Drive adapter        ← optional backup/recovery/collaboration
├── Git/filesystem adapter      ← optional versioned persistence
└── future adapters
```

Drive-based 0.x Roots remain valid migration/recovery sources. A 1.0 upgrade should preserve proven Project/Root identity, migrate semantic canonical state into local owners, and leave large Sources external unless there is a reason to copy them.

## Root vs Checkpoint

Example durable Root state:

```text
Decision: verified success methods are promoted to Operational Memory only after evidence passes.
Constraint: known failed paths are not repeated unchanged under the same preconditions.
```

Example Checkpoint state:

```text
Current task: finish Rebirth installer validation.
Completed: local write self-test passed.
Next: update README and release notes.
```

Putting both into the same owner would either pollute long-term Root knowledge or lose immediate task continuity. Rebirth makes the separation explicit.

## Production behavior

Ordinary self-contained requests use a Fast Path and should not load the Root merely because a Root exists.

Project-dependent work boots selectively:

```text
BOOT
→ ROOT
→ CHECKPOINT if resuming active work
→ only required knowledge owners
```

The human does not need to manage the internal tree during ordinary operation.

When the user explicitly requests compaction, short maintenance status messages are appropriate:

```text
현재 작업을 저장 중입니다…
저장 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행합니다.
```

## Compatibility

Root Engineering 1.0 does not invalidate the Codex, Claude, or Drive-native adapters. The major-version change is architectural:

- Root Kernel is storage-independent;
- ChatGPT Rebirth makes chat-local state the default runtime adapter;
- external stores become optional persistence/recovery adapters;
- active context becomes an explicitly replaceable resource;
- Checkpoint becomes a first-class runtime owner.

## Evidence boundary

Rebirth distinguishes verified architecture from host-specific behavior.

It does not claim:

- that every ChatGPT thread exposes the same compaction trigger;
- that `/mnt/data` survives every runtime transition;
- that compaction deletes the visible transcript or provider-side raw records;
- that ChatGPT's private implementation is identical to open-source Codex.

Host capabilities are recorded in `runtime/CAPABILITIES.json` and promoted to a hot path only after verification in the relevant scope.

## 1.0 validation

The package includes:

- `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md`
- `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md`
- `tools/validate_rebirth_installer.py`
- `tools/rebirth_local_selftest.py`

The local runtime self-test validates:

1. complete required file creation;
2. Project/Root identity consistency;
3. independent Checkpoint updates;
4. atomic file replacement when available;
5. save-failure blocking of compaction;
6. context-epoch increment only after simulated compaction confirmation.

Repeated real host compaction quality remains an empirical benchmark target, not a universal guarantee.

---

> **The transcript may remain. The active context may die. The checkpoint bridges the transition. The Root preserves truth. The same project continues.**
