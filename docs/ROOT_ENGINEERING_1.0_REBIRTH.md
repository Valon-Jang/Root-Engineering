# Root Engineering 1.0 — Rebirth

## Major-version change

Root Engineering 0.x focused on preserving validated project knowledge across models, sessions, and tools.

Root Engineering 1.0 adds a second replaceable resource: **active conversation context**.

> **Model is replaceable. Context is replaceable. Root persists.**

Rebirth does not make the transcript itself become the project database. It separates human history, model working memory, immediate resume state, durable project truth, and reusable capability so one long-running human-facing Chat can continue across repeated context replacement.

Normative fusion/authority contract:

- `ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION.md`
- Korean mirror: `ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION_KO.md`

Research provenance:

- `Valon-Jang/persistent-project-thread`

The research repository supplies evidence. Rebirth owns the production contract.

The ChatGPT-native mode is a **Complete Chat Runtime** — informally, a **완성형 Chat**. This is Root Engineering terminology, not an official OpenAI feature or product name.

## Resource model

```text
CHAT TRANSCRIPT
= human-visible history

ACTIVE MODEL CONTEXT
= transient compactable inference memory

CHECKPOINT
= immediate resume bridge across context reduction

LOCAL ROOT
= durable canonical project truth and routing

LOCAL CAPABILITY WORKSPACE
= reusable Skills, verified hot paths, helpers, manifests, and runtime assets
```

These resources are not interchangeable.

- Root stores only knowledge that deserves to survive future tasks.
- Checkpoint stores what must survive the next context transition but may become irrelevant after the current task.
- Capability Workspace stores or links executable behavior, but it does not become a second Root.
- Transcript remains useful to the human even when the model-visible context is compacted.

Capability semantics are canonicalized in:

```text
knowledge/OPERATIONAL.md   → verified methods, failures, evidence gates
runtime/CAPABILITIES.json  → path, hash, scope, availability, verification
ROOT.md                    → routing pointer only when required
```

Large model files, WAVs, caches, and disposable outputs are linked by path/hash rather than copied into canonical MD or included in the canonical Root hash by default.

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

This does **not** claim `/mnt/data` is permanent across every future Runtime. External storage remains an optional backup/recovery adapter.

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
├── tools/                 ← optional verified local helpers
├── sources/
└── scratch/
```

`tools/` and other capability assets are indexed through Operational Memory and CAPABILITIES rather than promoted into project truth by mere presence.

## Document authority

Root Engineering avoids MD competition.

```text
canonical English installer
→ delegated normative fusion/backup policies
→ Rebirth Skill hot path
→ explanatory architecture docs
→ independent research evidence
```

The Korean installer/policies are semantic mirrors. A production-rule change must update affected mirrors and validators in the same patch.

Only `root-engineering-rebirth` owns the `압축해` trigger inside a Rebirth installation. Do not install the independent Persistent Project Thread Skill into the same trigger scope.

## The fused Rebirth transaction

The user command `압축해` / `compact` is not interpreted as “write a summary.” It is a state-preservation transaction:

```text
Resolve exact Local Root
→ inspect Root filesystem
→ promote durable state to smallest canonical owners
→ refresh CHECKPOINT
→ verify local writes
→ seal Root digest + CHECKPOINT hash
→ perform changed external backup when a configured adapter requires it
→ compact active context
→ verify compaction
→ increment context epoch
→ rehydrate minimal required state
→ continue the same Chat
```

### Root resolution

Use, in order:

1. an explicit Root path in current instructions;
2. a previously verified active binding;
3. the documented project-local Root entry point;
4. `/mnt/data/root-engineering` only when verified as the actual installation.

Once resolved, do not search remote copies merely to prepare compaction.

### Local Storage Gate

Before compaction, inspect the filesystem that actually owns the Root path. Verify:

- target exists and is writable;
- enough free bytes exist for the intended patch/export;
- free inodes exist where exposed;
- write/read-back succeeds;
- failed candidates do not replace healthy canonical files.

Do not hard-code capacity from a previous Runtime.

### Critical invariant

> **REQUIRED LOCAL SAVE FAILURE = NO COMPACT**

This prevents context reduction from racing ahead of durable state.

## External backup semantics

Backup defaults to explicit compact-time synchronization and remains hash-gated, adapter-gated, and one-way. Scheduled, idle, timer-based, and background sync are disabled.

For ordinary `압축해`:

```text
no configured adapter      → no external write
configured, hash unchanged → skip upload
configured, hash changed   → update verified `latest`
```

A Google Drive policy is not proof that a Drive adapter ran. Sync is successful only when the connector/tool exists, the project target is bound, upload executes, and the remote bundle/manifest is verified.

Optional backup failure during ordinary `압축해` marks `external_backup_pending = true`; the verified Local Root remains authoritative and compaction may continue with a warning.

`백업하고 압축해` is strict: local save and external backup must both verify or compaction is blocked.

Normal direction:

```text
Local Root → external backup
```

External-to-Local restore is explicit and identity/hash verified; it is never an automatic merge.

The detailed policy is owned by `ROOT_ENGINEERING_1.0_BACKUP_POLICY.md`.

## Compaction capability ladder

Rebirth does not invent host internals.

1. **Native supported compact action** — only when the current host exposes one.
2. **Verified zero-output boundary fallback** — only when matching-scope evidence already demonstrated host auto-compaction at a tool/sampling boundary and success can be verified.
3. **Bounded diagnostic pressure** — small increments, diagnostic-only, stop immediately on success.
4. **Stop and diagnose** — when success cannot be verified.

Never claim a no-op universally forces compaction. Never default to thousands of disposable lines. Never invent a private RPC.

The independent Persistent Project Thread experiments established the motivation and evidence boundary for this ladder:

- broad local process/file/socket/cgroup “minefield” instrumentation did not expose a decisive container-local compaction operation;
- trigger output was reduced from thousands of lines to a zero-output boundary in the tested already-eligible thread;
- pre-compaction messages remained scrollable to the human afterward.

These are environment-specific observations, not disclosure of ChatGPT internals.

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

Advance the epoch only after verified compaction. This creates a measurable unit for:

- compaction count;
- same-thread resume accuracy;
- decision retention;
- capability reuse;
- backup state;
- latency/context trend where observable;
- quality loss across repeated compactions.

## Root vs Checkpoint vs Capability

Durable Root state:

```text
Decision: verified success methods enter Operational Memory only after evidence passes.
Constraint: known failed paths are not repeated unchanged under the same preconditions.
```

Checkpoint state:

```text
Current task: finish Rebirth MD-fusion validation.
Completed: canonical Skill and backup policy were synchronized.
Next: run cross-document validator.
```

Capability state:

```text
Capability: zero-output compaction boundary
Status: VERIFIED only for a recorded environment/scope
Helper path/hash: recorded in CAPABILITIES.json
Procedure/failure guards: owned by OPERATIONAL.md
```

Mixing these would pollute durable knowledge, lose immediate continuity, or turn executable files into an accidental second source of truth.

## Production behavior

Ordinary self-contained requests use the Fast Path and should not load Root merely because Root exists.

Project-dependent work boots selectively:

```text
BOOT
→ ROOT
→ CHECKPOINT only when resuming
→ only required knowledge/capability owners
```

During explicit compaction, short status messages are appropriate:

```text
현재 작업을 저장 중입니다…
로컬 저장 완료. 복구본을 동기화 중입니다…   # only when actually applicable
저장 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행합니다.
```

## Compatibility

Root Engineering 1.0 does not invalidate Codex, Claude, or Drive-native adapters.

- Kernel remains storage-independent.
- ChatGPT Rebirth uses chat-local state as the default Runtime adapter.
- external stores are optional persistence/recovery adapters;
- active context is explicitly replaceable;
- Checkpoint is a first-class transition owner;
- reusable capability is indexed separately from canonical knowledge.

The Persistent Thread fusion does not change package/schema identity. It closes cross-document semantics and introduces no incompatible Root layout requirement.

## Evidence boundary

Rebirth does not claim:

- every ChatGPT thread exposes the same compaction trigger;
- `/mnt/data` survives every Runtime transition;
- compaction deletes visible transcript or provider-side records;
- ChatGPT is implemented identically to open-source Codex;
- a documented Google Drive policy means an adapter executed;
- capability files are authoritative merely because they exist.

Host capabilities belong in `runtime/CAPABILITIES.json` and become a hot path only after verification in the relevant scope.

## 1.0 validation

The package includes:

- `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md`
- `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md`
- `installer/rebirth/root-engineering/SKILL.md`
- `installer/rebirth/runtime/rebirth_transaction.py`
- `docs/ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION.md`
- `docs/ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION_KO.md`
- `docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md`
- `docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY_KO.md`
- `tools/validate_rebirth_md_fusion.py`

Validation must prove:

1. authority and semantic-mirror relationships are explicit;
2. one compaction trigger owner exists;
3. Pre-Compaction Save and Storage Gates exist;
4. backup defaults to `EXPLICIT_COMPACT_ONLY` and remains hash/adapter gated with optional vs strict failure separation;
5. capability assets cannot become a competing Root;
6. context epoch advances only after observed success;
7. package and schema remain `1.0.0`.

Repeated real-host compaction quality remains an empirical benchmark target, not a universal guarantee.

---

> **The transcript may remain. The active context may die. The checkpoint bridges the transition. The Root preserves truth. Skills preserve reusable capability. The same project continues.**
