# Root Engineering 1.0 — Rebirth

Release package: `1.0.0`

## Major-version change

Root Engineering 0.x focused on preserving validated project knowledge across models, sessions, and tools.

Root Engineering 1.0 adds a second replaceable resource: **active conversation context**.

> **Model is replaceable. Context is replaceable. Root persists.**

The Rebirth goal is not to make a transcript itself become the project database. It separates project continuity into distinct layers so a long-running human-facing Chat can continue even when the model's working context is compacted.

## Complete Chat Runtime

Rebirth defines an independent **Complete Chat Runtime** for ordinary ChatGPT Chat — the “완성형 Chat” concept.

It does not replace ChatGPT with a custom API client, CLI, coding-agent workspace, or external chat server. Instead, it adds a project-state and context-maintenance lifecycle around the ordinary Chat surface:

```text
one ordinary ChatGPT Chat
        + retained human transcript
        + compactable active context
        + chat-local ROOT
        + resumable CHECKPOINT
        + optional compact-time recovery mirror
        = Complete Chat Runtime
```

The architectural objective is to separate the lifetime of the human-facing thread from the lifetime of the model's active working context. The thread may continue while context epochs are compacted and renewed.

“Complete Chat Runtime” is Root Engineering terminology, not an official OpenAI product name or feature claim.

## Five operational resources

```text
CHAT TRANSCRIPT
= human-visible history

ACTIVE MODEL CONTEXT
= transient working memory for inference

CHECKPOINT
= immediate resume state across context reduction

LOCAL ROOT
= durable canonical project truth and routing

EXTERNAL RECOVERY MIRROR
= optional off-runtime backup, synchronized at explicit maintenance
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

The user command `압축해` / `compact` is not interpreted as "write a summary." It is a state-preservation and recovery-maintenance transaction:

```text
Persist durable state
→ Refresh CHECKPOINT
→ Verify and seal local state
→ Synchronize external recovery mirror if configured
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

An optional external-backup failure is a different class of failure. The Local Root remains canonical for the current runtime; the failure is recorded as pending and reported rather than silently treated as success. A strict user request such as `backup and compact` may require external verification before compaction.

## Backup cadence: compact-time, not background-time

The default Rebirth 1.0 policy deliberately avoids scheduled, idle, timer-based, and background synchronization.

External backup runs only when the user explicitly opens a maintenance boundary:

- `압축해` / `compact`;
- an explicit `백업해` / `backup` request.

Why:

1. backup should not introduce connector latency while the user is actively working;
2. a scheduled task may execute in a separate runtime that cannot see the same chat-local `/mnt/data`;
3. explicit maintenance produces a clear state boundary that can be sealed, verified, and resumed;
4. backup and compaction tool calls may themselves create host sampling boundaries, so the Local Root and Checkpoint must be sealed first.

Configured compact-time flow:

```text
Local persist + Checkpoint
→ local verification
→ seal canonical digest + Checkpoint hash
→ export recovery snapshot
→ update external latest mirror
→ verify or mark backup pending
→ compact / rehydrate / continue
```

When the snapshot hash matches the verified remote latest mirror, the remote write may be skipped. Important milestones may also create immutable snapshots, but only inside the same explicit maintenance window or an explicit backup command.

If a backup tool call itself triggers confirmed host compaction, it counts as the transaction's compaction boundary. Rehydrate, verify the backup outcome, complete the epoch transition, and do not emit another compact trigger.

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
- external recovery status;
- latency/context trend where observable;
- quality loss across repeated compactions.

The state also records the backup policy and current outcome:

```json
{
  "external_backup_sync_trigger": "EXPLICIT_COMPACT_ONLY",
  "scheduled_backup_sync": false,
  "idle_backup_sync": false,
  "external_backup_pending": false,
  "last_external_backup": null
}
```

## Storage adapters

Rebirth separates the method from storage:

```text
Root Engineering Kernel
├── Chat-local /mnt adapter     ← default ChatGPT runtime
├── Google Drive adapter        ← optional compact-time backup/recovery
├── Git/filesystem adapter      ← optional versioned persistence
└── future adapters
```

Drive-based 0.x Roots remain valid migration/recovery sources. A 1.0 upgrade should preserve proven Project/Root identity, migrate semantic canonical state into local owners, and leave large Sources external unless there is a reason to copy them.

Normal recovery synchronization is one-way:

```text
verified Local Root → external recovery mirror
```

External-to-local merge is a separate explicit recovery/migration operation, not an automatic background reconciliation loop.

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
로컬 저장 완료. 복구본을 동기화 중입니다…   # configured adapter only
저장 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행합니다.
```

## Compatibility

Root Engineering 1.0 does not invalidate the Codex, Claude, or Drive-native adapters. The major-version change is architectural:

- Root Kernel is storage-independent;
- ChatGPT Rebirth makes chat-local state the default runtime adapter;
- external stores become optional persistence/recovery adapters;
- external backup synchronization occurs at explicit maintenance boundaries by default;
- active context becomes an explicitly replaceable resource;
- Checkpoint becomes a first-class runtime owner.

## Evidence boundary

Rebirth distinguishes verified architecture from host-specific behavior.

It does not claim:

- that every ChatGPT thread exposes the same compaction trigger;
- that `/mnt/data` survives every runtime transition;
- that compaction deletes the visible transcript or provider-side raw records;
- that ChatGPT's private implementation is identical to open-source Codex;
- that a scheduled ChatGPT task can access the current Chat's Local Root.

Host capabilities are recorded in `runtime/CAPABILITIES.json` and promoted to a hot path only after verification in the relevant scope.

## 1.0 validation

The package includes:

- `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md`
- `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md`
- `installer/rebirth/root-engineering/SKILL.md`
- `installer/rebirth/runtime/rebirth_transaction.py`
- `tools/validate_rebirth_installer.py`
- `tools/rebirth_local_selftest.py`
- `tools/validate_rebirth_runtime.py`

The local runtime self-tests validate:

1. complete required file creation;
2. Project/Root identity consistency;
3. independent Checkpoint updates;
4. atomic file replacement when available;
5. save-failure blocking of compaction;
6. compact-time backup status recording;
7. scheduled/idle sync rejection;
8. context-epoch increment only after simulated compaction confirmation.

Repeated real host compaction quality remains an empirical benchmark target, not a universal guarantee.

---

> **The transcript may remain. The active context may die. The checkpoint bridges the transition. The Root preserves truth. The same project continues.**
