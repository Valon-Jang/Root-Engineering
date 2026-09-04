---
package_id: root-engineering-rebirth-chat-installer
package_version: 1.0.0
codename: Rebirth
schema_version: 1.0.0
release_date: 2026-09-04
target_environment: ordinary ChatGPT Chat with writable chat-local workspace
primary_storage_adapter: chat-local-mnt
project_required: false
google_drive_required: false
single_file_package: true
supported_modes:
  - INSTALL
  - VERIFY
  - REPAIR
  - UPGRADE_FROM_DRIVE
  - EXPORT
  - COMPACT
three_layer_memory_model: transcript-active-context-local-root
checkpoint_owner: runtime/CHECKPOINT.md
context_epoch: true
compaction_transaction: persist-verify-compact-rehydrate
save_failure_blocks_compaction: true
native_compaction_policy: exposed-supported-only
boundary_fallback_policy: same-environment-verified-only
large_pressure_policy: diagnostic-only-bounded
external_storage_role: optional-backup-recovery-source
backup_sync_policy: event-driven-dirty-only
backup_on_compaction: configured-and-hash-changed
backup_latest_policy: verified-replace
backup_snapshot_policy: milestone-explicit-migration
optional_backup_failure_blocks_compaction: false
strict_backup_compaction_command: true
backup_direction: local-to-external-one-way
---

# ROOT ENGINEERING 1.0.0 — REBIRTH

> **Model is replaceable. Context is replaceable. Root persists.**
>
> **Save the state → compact the context → rehydrate the work → continue the same Chat.**

This is the canonical Chat-native installer for Root Engineering 1.0.0 — **Rebirth**.
It is designed for an ordinary ChatGPT conversation and does not require a ChatGPT Project or Google Drive.

## 0. Rebirth architecture

Rebirth separates three resources that a long-running Chat must not confuse:

```text
CHAT TRANSCRIPT
= human-visible history

ACTIVE MODEL CONTEXT
= compactable model working memory

LOCAL ROOT
= durable canonical project state inside the current Chat Runtime
```

Two supporting resources complete the operating system:

```text
CHECKPOINT
= immediate resume bridge across active-context replacement

LOCAL CAPABILITY WORKSPACE
= reusable Skills, verified hot paths, helpers, manifests, and runtime assets
```

The Capability Workspace is not a second Root. Canonical capability meaning belongs in `knowledge/OPERATIONAL.md`; availability, path, hash, scope, and verification belong in `runtime/CAPABILITIES.json`.

Default Runtime path:

```text
/mnt/data/root-engineering/
```

The method does not claim that `/mnt/data` survives every future Chat/Runtime lifecycle. Local ROOT is the primary **current-runtime** store. Google Drive, Git, or exported files may be used as optional backup/recovery adapters.

The independent `Valon-Jang/persistent-project-thread` repository is research/evidence provenance. Rebirth owns the production contract. Do not install its separate Skill beside `root-engineering-rebirth` in the same trigger scope.

## 1. Installation agent contract

When the user says `설치해`, `install`, or equivalent, do the work instead of merely explaining it.

### Preflight

1. Confirm a writable chat-local file workspace exists.
2. Prefer `/mnt/data`; if unavailable, use the host-exposed writable workspace and record the actual path.
3. Verify create → read → update → read-back on a temporary file.
4. Inspect free bytes and, where available, free inodes on the filesystem that will own the Root.
5. Detect whether a Root already exists at the chosen path.
6. Never overwrite an unidentified existing Root.

Do not hard-code a storage capacity observed in another Runtime. Capacity, quota, mount, and persistence lifetime are environment properties.

### New installation

Create:

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
├── tools/                 ← optional verified local helpers
├── sources/
└── scratch/
```

Use random stable `PROJECT_ID`, `ROOT_ID`, and `NODE_ID` values. Human-readable names may change; IDs do not.

`tools/`, Skills, model files, WAVs, caches, and generated artifacts do not become canonical merely by existing. Index verified procedures in Operational Memory and path/hash/scope in CAPABILITIES. Do not include large or disposable assets in the canonical Root hash by default.

### Existing Drive-based Root

If an older Root Engineering installation is explicitly available and the user is upgrading:

1. Read the latest Drive ROOT and required Branches through exact IDs/live access.
2. Preserve the existing Project ID and Root ID when identity is proven.
3. Copy canonical semantic content into matching local MD owners.
4. Do not indiscriminately download large Sources. Preserve Source IDs/URLs and retrieve them only when needed.
5. Leave the Drive Root intact as a recovery source unless the user explicitly changes that policy.
6. Verify the local Root before making it primary.
7. After migration, normal authority direction is Local → external backup; do not automatically merge Drive changes back.

## 2. Kernel rules

### 2.1 Fast path

If the current request is self-contained and does not require stored project state, answer from the current conversation without loading the Root.

### 2.2 Project-dependent boot

When stored project state is required:

```text
read BOOT.md
→ read ROOT.md
→ read runtime/CHECKPOINT.md only when continuing active work
→ read only routed knowledge/capability owners needed for the request
```

Do not preload the entire tree.

### 2.3 Save gate

Persist only information whose loss would materially increase the chance that a future model must rediscover it, make a worse decision, or repeat a previous failure.

Do not store:

- raw transcript dumps;
- private chain-of-thought;
- disposable brainstorming;
- unverified model inference as fact;
- duplicate canonical truth;
- large capability assets inside MD merely to make them “persistent.”

### 2.4 Save placement

- `knowledge/FOUNDATION.md`: purpose, durable principles, long-term boundaries, essential Human Intent.
- `knowledge/CURRENT.md`: currently valid facts, state, decisions, constraints, important unresolved items.
- `knowledge/LEARNED.md`: verified reusable methods and generalized lessons.
- `knowledge/OPERATIONAL.md`: exact operation keys, safe failure fingerprints, do-not-repeat constraints, verified hot paths, capability procedures, required evidence.
- `knowledge/HISTORY.md`: superseded states whose rationale, rollback, or failure-prevention value remains useful.
- `runtime/CHECKPOINT.md`: ephemeral-but-essential resume state for work currently in progress.
- `runtime/CAPABILITIES.json`: executable capability availability, paths, hashes, scope, and verification state.
- `ROOT.md`: routing, identity, compact digest, and Child ownership only.

### 2.5 Operational Memory

Before a non-trivial repeated operation, repair, upgrade, or retry, derive a stable key:

```text
subsystem/action/failure-mode
```

Apply only exact matching records whose scope and preconditions match.
Prefer `VERIFIED_FAST_PATH` or `ACTIVE_CONSTRAINT` before exploring alternatives.
Never replay an unchanged known failed path under the same conditions.

### 2.6 Question-driven deepening

Ask only when missing Human Ground Truth, priority, or value judgment can change the next decision and cannot be resolved from Root, Sources, or tools.

> **Taproot before branching. Ask only what changes the next decision.**

## 3. Local write and storage transaction

For durable local state changes:

```text
resolve exact Root
→ resolve exact owner
→ inspect owning filesystem
→ read current owner
→ compute minimum semantic patch
→ write candidate atomically when possible
→ read back affected logical scope
→ accept only after verification
```

### Root resolution priority

1. explicit Root path in current user/system/project instructions;
2. already verified active Root binding;
3. documented project-local Root entry point;
4. `/mnt/data/root-engineering` only when verified as the actual installation.

Once a valid Local Root is resolved, do not search File Library, Drive, GitHub, or Web for a competing canonical copy merely to prepare compaction.

### Local Storage Gate

Check the filesystem that actually owns the resolved Root path. Verify at minimum:

- the filesystem and target directory exist;
- the target is writable;
- sufficient free bytes exist for the intended patch/checkpoint/export;
- sufficient free inodes exist when inode accounting is available;
- actual write/read-back succeeds;
- a failed candidate write leaves the previous canonical state intact.

When code/file tools allow it, prefer same-directory temporary write + `os.replace()` to avoid torn files.
For ordinary low-risk patches, exact affected-scope read-back is sufficient.
For high-risk identity/routing changes, verify the complete affected relationship.

If a write cannot be verified, report the failure and keep the previous canonical state.

> **Required local save or Storage Gate failure = no compact.**

Free capacity does not prove persistence across every future Runtime replacement.

## 4. CHECKPOINT contract

`runtime/CHECKPOINT.md` is not long-term knowledge. It exists to survive active-context reduction.

It should contain only what another context instance needs to continue immediately:

```text
# ACTIVE CHECKPOINT

## Current Goal
<one current outcome>

## Completed
<only completed work relevant to resumption>

## Current State
<key working state that may not belong in durable knowledge>

## Next
<ordered next actions>

## Pending / Risks
<important unresolved blockers>

## Resume Instruction
Read ROOT routing, then this checkpoint, then only required owners. Continue from Next without reconstructing completed discussion.
```

Every deliberate compaction refreshes CHECKPOINT even when no new long-term Root knowledge was created.

## 5. `압축해` / COMPACT transaction

When the user says `압축해`, `컴팩션`, `채팅 정리해`, `compact`, or equivalent, treat it as a state transaction, not a summarization request.

`root-engineering-rebirth` is the single operational trigger owner in a Rebirth installation.

### User-visible status

At the start:

```text
현재 작업을 저장 중입니다…
```

After local persistence verifies:

- when no external backup is configured or the local Root hash is unchanged:

```text
저장 완료. 대화를 압축 중입니다…
```

- when an external backup adapter is configured and the local Root changed:

```text
로컬 저장 완료. 복구본을 동기화 중입니다…
```

After verified backup success:

```text
복구본 동기화 완료. 대화를 압축 중입니다…
```

If optional backup fails during ordinary `압축해`, keep the local save, mark backup pending, and say:

```text
로컬 저장은 완료됐지만 복구본 동기화는 보류됐습니다. 대화 압축은 계속합니다.
```

For `백업하고 압축해` / `backup and compact`, backup is strict. If external backup cannot be verified, stop before compaction and report that the local save is safe but the requested backup did not complete.

After successful compaction and rehydration:

```text
압축 완료. 이어서 진행합니다.
```

### Internal order — non-negotiable

```text
1. Resolve the exact verified Local Root.
2. Read ROOT routing and current CHECKPOINT only as needed.
3. Inspect new durable state since the last canonical update.
4. Route durable items to the smallest correct Root owners.
5. Run the Local Storage Gate against the actual Root filesystem.
6. Patch required owners and refresh runtime/CHECKPOINT.md.
7. Verify every required local write.
8. IF local verification fails → STOP. DO NOT COMPACT.
9. Seal canonical digest + CHECKPOINT hash.
10. Compute current canonical Root hash and compare with last_backup_root_hash.
11. If an external adapter is configured and the event requires sync:
    - unchanged hash → skip upload;
    - changed hash → update verified latest backup;
    - milestone/explicit/migration event → also create immutable snapshot.
12. If optional backup fails during ordinary `압축해`:
    - set external_backup_pending = true;
    - keep verified Local Root authoritative;
    - continue with a visible warning.
13. If strict `백업하고 압축해` backup fails → STOP. DO NOT COMPACT.
14. Attempt active-context compaction using the priority below.
15. Verify compaction using a host-exposed/native confirmation or previously demonstrated reliable signal.
16. On success, increment context_epoch in runtime/STATE.json.
17. Rehydrate from BOOT + CHECKPOINT + only required Root/capability owners.
18. Continue the same Chat.
```

### External adapter reality gate

A policy declaration is not an executable adapter. Google Drive synchronization counts as successful only when:

1. a Drive connector/tool or other valid adapter is actually available;
2. the project backup target is bound unambiguously;
3. upload executes;
4. the uploaded manifest/bundle is read back or otherwise verified.

If no adapter is configured, ordinary `압축해` performs no external write. Strict `백업하고 압축해` blocks before compaction.

### Compaction priority

#### Priority A — supported native compact action

If the current host explicitly exposes and supports a compact action/API/tool, use it.
Never invent or assume access to a private/internal RPC.

#### Priority B — verified zero-output boundary fallback

Use only when ALL are true:

1. the same environment/thread class has demonstrated automatic compaction at a tool/sampling boundary;
2. a zero-output/no-op boundary is available;
3. compaction success can be observed or reliably confirmed.

Then:

```text
persist + verify + seal
→ execute exactly one zero-output boundary
→ verify compaction
→ STOP triggering on success
→ rehydrate
```

The reference no-op may be semantically only:

```python
pass
```

The useful event is the tool/sampling boundary, not the Python statement.

#### Priority C — bounded diagnostic pressure

Only for diagnosis when compaction is required, no native path is exposed, and Priority B is insufficient.
Use small bounded increments and verify after each boundary. Never default to thousands of disposable lines.

Example maximum progression without explicit deeper-experiment authorization:

```text
1 small chunk → verify
20 lines      → verify
100 lines     → verify
400 lines     → verify
STOP
```

### Hard safety rule

> **SAVE FAILURE = NO COMPACT**

Never deliberately compact meaningful active context when required durable state, CHECKPOINT, Storage Gate, or strict external backup is unverified.

## 6. Context Epoch

`runtime/STATE.json` tracks context lifecycle and backup status, not project truth.

Minimum fields:

```json
{
  "schema_version": "1.0.0",
  "context_epoch": 0,
  "compaction_count": 0,
  "checkpoint_revision": 0,
  "root_revision": 0,
  "last_compaction": null,
  "boundary_compaction_verified": false,
  "boundary_verification_scope": null,
  "external_backup_adapter": "NONE",
  "external_backup_pending": false,
  "current_root_hash": null,
  "last_backup_root_hash": null,
  "last_backup_at": null,
  "last_snapshot_at": null
}
```

Increment `context_epoch` and `compaction_count` only after compaction is confirmed.
A verified boundary fallback is scoped to proven environment/preconditions and must not silently transfer to another Runtime.

## 7. Transcript rule

Compaction is not transcript deletion.
Do not claim provider-side raw logs, audit records, safety records, or the user's visible Chat have been physically deleted.

Operationally keep the layers separate:

```text
Human wants historical conversation → visible transcript / explicit retrieval
Model needs smaller working memory  → active-context compaction
Project needs authoritative truth    → Local ROOT
Work needs immediate resumption      → CHECKPOINT
Reusable behavior is needed          → capability workspace
```

The Persistent Project Thread experiment observed scrollable pre-compaction messages after repeated context compaction. This supports the operational distinction but does not reveal ChatGPT's private database design.

## 8. Production Quiet

During ordinary work, perform routing, reads, and verified persistence quietly.
Do not expose internal Root/Branch/Flush jargon unless the user asks about architecture or maintenance is underway.

`압축해` is an explicit maintenance command, so the short save/backup/compact status messages in Section 5 are allowed and recommended.

## 9. Backup and recovery adapters

Rebirth separates Kernel from storage.

```text
Root Engineering Kernel
    ↓
Primary ChatGPT adapter: /mnt/data
    ↓ optional
Google Drive / Git / export bundle / filesystem backup
```

External adapters are not required for normal Rebirth operation.
Use them for cross-runtime recovery, durable off-chat backup, collaboration, version history, or migration.

### 9.1 Event-driven cadence — no timer loop

Backup cadence is based on meaningful events, not elapsed time. Do not claim or depend on an invisible background timer in an ordinary Chat.

| Event | External backup action |
|---|---|
| ordinary conversation | none |
| verified Local Root patch | mark backup pending when canonical hash changed |
| `압축해` / `compact` | update `latest` only when adapter is configured and hash changed |
| critical authority/routing/structure change | update `latest` immediately when configured |
| `백업해` / `backup` | force immediate verified `latest` backup |
| `백업하고 압축해` / `backup and compact` | require verified external backup before compaction |
| `마무리하자` / explicit closeout | update `latest` when changed |
| release, major milestone, migration, restore, destructive change | update `latest` and create immutable snapshot |
| no semantic/hash change | skip external write |

The Local Root remains authoritative during the current Runtime.

### 9.2 Hash-gated latest backup

Compute a deterministic hash over the canonical export set, excluding disposable scratch files and unstable packaging metadata.

Recommended set:

```text
BOOT.md
ROOT.md
MANIFEST.json
knowledge/**
runtime/CHECKPOINT.md
runtime/STATE.json
runtime/CAPABILITIES.json
linked small canonical Sources explicitly included by policy
```

Do not include large model files, generated WAVs, caches, or disposable artifacts unless explicit project policy makes them canonical.

If `current_root_hash == last_backup_root_hash`, do not upload again.

When changed, update a single recoverable `latest` bundle:

```text
Root Engineering Backups/
└── <PROJECT_ID>/
    ├── latest/
    │   ├── root-engineering-latest.zip
    │   └── BACKUP_MANIFEST.json
    └── snapshots/
        └── <ISO_DATE>_epoch-<N>_<REASON>.zip
```

Minimum `BACKUP_MANIFEST.json`:

```json
{
  "project_id": "<PROJECT_ID>",
  "root_id": "<ROOT_ID>",
  "root_engineering_version": "1.0.0",
  "context_epoch": 0,
  "canonical_root_hash": "<HASH>",
  "backed_up_at": "<ISO-8601>",
  "backup_kind": "LATEST",
  "verification": "PASS"
}
```

Replace `latest` only after upload and read-back/hash verification succeed.
Do not create a new immutable snapshot for every compaction.

### 9.3 Snapshot gate

Create an immutable snapshot only for:

- release or named milestone;
- adapter/runtime migration;
- restore before accepting different canonical state;
- critical authority/routing/schema change;
- potentially destructive operation;
- explicit user request.

Snapshots explain or recover significant transitions. They are not an activity log.

### 9.4 Failure semantics

```text
required Local Root / CHECKPOINT / Storage Gate failure
→ STOP
→ NO COMPACT

optional external backup failure during ordinary `압축해`
→ Local Root remains authoritative
→ external_backup_pending = true
→ compaction may continue with visible warning
```

Strict mode:

```text
`백업하고 압축해`
→ Local save and external backup must both verify
→ any required failure = NO COMPACT
```

Retry pending optional backup at the next qualifying event or explicit `백업해`.
Do not repeatedly retry the same failed operation without a materially different path.

### 9.5 One-way authority and restore

After migrating a Drive-based Root to Local Rebirth:

```text
Drive latest canonical read
→ Local Root conversion
→ Local identity/content verification
→ final Drive migration snapshot
→ former Drive Root retained as legacy/read-only recovery source
→ normal flow becomes Local → external backup
```

Do not automatically merge Drive changes back into Local Root during normal operation.
Restore is explicit: select one backup, verify Project ID, Root ID, version compatibility, manifest, and content hash, then restore only the requested scope.

Never claim chat-local `/mnt/data` is permanent across all future Sessions unless that durability is actually verified by the host.

## 10. INSTALL templates

### BOOT.md

```markdown
# ROOT ENGINEERING 1.0 — REBIRTH BOOT

Root: /mnt/data/root-engineering/ROOT.md
Checkpoint: /mnt/data/root-engineering/runtime/CHECKPOINT.md
State: /mnt/data/root-engineering/runtime/STATE.json

For self-contained requests, answer directly.
For project-dependent work, read ROOT and only required routed owners.
When resuming active work, read CHECKPOINT.

COMPACT transaction:
Resolve Root → Storage Gate → Persist durable state → Refresh CHECKPOINT → Verify + seal → Sync changed optional backup → Compact → Rehydrate → Continue same Chat.

Backup policy:
- Local Root is authoritative.
- Sync external `latest` on qualifying events only when canonical hash changed and an executable adapter/target is verified.
- Create immutable snapshots only for milestones, explicit requests, migration/restore, or critical changes.
- `백업하고 압축해` requires verified external backup.
- ordinary `압축해` may continue after optional backup failure with `external_backup_pending = true`.

Capability policy:
- canonical procedures belong in OPERATIONAL.md;
- availability/path/hash/scope belong in CAPABILITIES.json;
- large assets remain linked unless explicitly canonical.

Hard rule: required local save or Storage Gate failure = no compact.
```

### ROOT.md

```markdown
# PROJECT ROOT

## Identity
- Project Name: <PROJECT_NAME>
- Project ID: <PROJECT_ID>
- Root ID: <ROOT_ID>
- Root Engineering Version: 1.0.0
- Codename: Rebirth

## Foundation Digest
<SHORT_PURPOSE_AND_BOUNDARIES>

## Current Digest
### Current Status
<SHORT_CURRENT_STATE>

### Key Active Decisions
<SHORT_ACTIVE_DECISIONS>

### Important Unresolved
<SHORT_HIGH_IMPACT_UNRESOLVED>

## Root Map
- Foundation → knowledge/FOUNDATION.md
- Current Knowledge → knowledge/CURRENT.md
- Learned Knowledge → knowledge/LEARNED.md
- Operational Memory → knowledge/OPERATIONAL.md
- History → knowledge/HISTORY.md

## Runtime Map
- Checkpoint → runtime/CHECKPOINT.md
- State → runtime/STATE.json
- Capabilities → runtime/CAPABILITIES.json

## Knowledge Lookup
Coverage: PARTIAL
<ADD_ROUTES_ONLY_WHEN_REAL_RETRIEVAL_PATTERNS_REQUIRE_THEM>
```

### knowledge/FOUNDATION.md

```markdown
# FOUNDATION

## Identity
- Project ID: <PROJECT_ID>
- Root ID: <ROOT_ID>

## Purpose
<CONFIRMED_PROJECT_PURPOSE>

## Principles / Boundaries
<CONFIRMED_DURABLE_PRINCIPLES>
```

### knowledge/CURRENT.md

```markdown
# CURRENT KNOWLEDGE

## Identity
- Project ID: <PROJECT_ID>
- Root ID: <ROOT_ID>

## Current Status
<ONLY_CURRENTLY_VALID_STATE>

## Active Decisions
<CONFIRMED_CURRENT_DECISIONS>

## Active Constraints
<CURRENT_CONSTRAINTS>

## Important Unresolved
<HIGH_IMPACT_UNRESOLVED>
```

### knowledge/LEARNED.md

```markdown
# LEARNED KNOWLEDGE

## Identity
- Project ID: <PROJECT_ID>
- Root ID: <ROOT_ID>

Store only verified, reusable, generalized methods and lessons.
```

### knowledge/OPERATIONAL.md

```markdown
# OPERATIONAL MEMORY

## Identity
- Project ID: <PROJECT_ID>
- Root ID: <ROOT_ID>

## Fast-Path Index
| Operation Key | Lifecycle State | Record |
|---|---|---|

## Records

Use exact subsystem/action/failure-mode keys.
Preserve known failed paths as Do-not-repeat evidence.
Promote replacements only after required evidence passes.
Index reusable local capabilities without duplicating their binaries into MD.
```

### knowledge/HISTORY.md

```markdown
# HISTORY

## Identity
- Project ID: <PROJECT_ID>
- Root ID: <ROOT_ID>

Store only superseded states that retain transition, rollback, or failure-prevention value.
```

### runtime/CHECKPOINT.md

```markdown
# ACTIVE CHECKPOINT

## Current Goal
None

## Completed
- Rebirth installation initialized.

## Current State
- Local Root is active.

## Next
- Continue normal project work.

## Pending / Risks
- Chat-local workspace lifetime is host-dependent unless separately verified.

## Resume Instruction
Read ROOT routing, then this checkpoint, then only required owners. Continue from Next without reconstructing completed discussion.
```

### runtime/STATE.json

```json
{
  "schema_version": "1.0.0",
  "context_epoch": 0,
  "compaction_count": 0,
  "checkpoint_revision": 0,
  "root_revision": 0,
  "last_compaction": null,
  "boundary_compaction_verified": false,
  "boundary_verification_scope": null,
  "external_backup_adapter": "NONE",
  "external_backup_pending": false,
  "current_root_hash": null,
  "last_backup_root_hash": null,
  "last_backup_at": null,
  "last_snapshot_at": null
}
```

### runtime/CAPABILITIES.json

```json
{
  "schema_version": "1.0.0",
  "local_workspace": "VERIFIED",
  "workspace_path": "/mnt/data/root-engineering",
  "native_compact_action": "UNKNOWN",
  "zero_output_boundary_compaction": "UNVERIFIED",
  "external_backup_adapter": "OPTIONAL",
  "external_backup_sync_policy": "EVENT_DRIVEN_HASH_GATED",
  "external_backup_strict_command": "백업하고 압축해",
  "capability_assets": []
}
```

### MANIFEST.json

```json
{
  "package_id": "root-engineering-rebirth-chat-installer",
  "package_version": "1.0.0",
  "codename": "Rebirth",
  "schema_version": "1.0.0",
  "project_id": "<PROJECT_ID>",
  "root_id": "<ROOT_ID>",
  "primary_storage_adapter": "chat-local-mnt",
  "status": "ACTIVE"
}
```

## 11. VERIFY

PASS only if:

1. all required files exist;
2. Project ID and Root ID match across canonical owners;
3. BOOT routes to actual Root/Checkpoint/State paths;
4. ordinary self-contained requests can avoid loading Root;
5. project-dependent requests load only required owners;
6. durable decisions can be minimally patched and read back;
7. CHECKPOINT refreshes independently from long-term knowledge;
8. a simulated failed save or Storage Gate prevents compaction;
9. known Operational failures are not replayed unchanged;
10. no installation step requires Google Drive or a ChatGPT Project;
11. `/mnt/data` durability is not overstated;
12. compaction capability state is honest: supported, verified fallback, or unavailable/unknown;
13. external backup cadence is event-driven and hash-gated;
14. unchanged canonical hash skips external upload;
15. policy text is not reported as adapter execution;
16. ordinary `압축해` may proceed after optional backup failure only after `external_backup_pending = true`;
17. strict `백업하고 압축해` blocks compaction when external backup is unverified;
18. immutable snapshots are milestone/explicit/migration/critical-change gated;
19. normal authority flow is Local → external with no automatic bidirectional merge;
20. capability assets are indexed without becoming a competing Root;
21. only one compaction trigger Skill owns the Rebirth scope;
22. English/Korean semantic mirrors and validators are synchronized for the touched rules.

## 12. REPAIR

Repair the smallest damaged owner.
Do not regenerate a healthy Root wholesale.
Preserve stable IDs and unrelated content.
When identity cannot be proven, stop instead of silently adopting another Root.

## 13. EXPORT / BACKUP

When the user requests backup or cross-runtime recovery:

1. create a deterministic export of the canonical Local Root;
2. compute and record its canonical Root hash;
3. skip unchanged `latest` upload unless a new snapshot is explicitly requested;
4. upload/commit through the configured executable external adapter;
5. verify the uploaded bundle and `BACKUP_MANIFEST.json`;
6. update `last_backup_root_hash`, `last_backup_at`, and `external_backup_pending` only after verification.

External backup does not change Local Root authority unless the user explicitly performs adapter migration or restore.

## 14. Acceptance gate for Rebirth

A strong Rebirth validation should test repeated cycles:

```text
work
→ durable-state promotion
→ CHECKPOINT
→ verified backup event when applicable
→ verified compaction
→ rehydrate
→ continue same Chat
```

Measure at minimum:

- same-thread continuation;
- state accuracy after compaction;
- decision retention;
- checkpoint resume accuracy;
- capability reuse;
- no-repeat operational behavior;
- external backup-state accuracy;
- context/latency trend where observable;
- quality loss across repeated compactions.

Do not claim universal one-chat-forever behavior from a single environment.

## 15. Completion report

```text
Root Engineering 1.0.0 — Rebirth ready

- Local Root: PASS
- ROOT routing: PASS
- CHECKPOINT runtime: PASS
- Local Storage Gate: PASS
- Local write/read-back: PASS
- Save-failure compaction guard: PASS
- Operational Memory: PASS
- Local Capability Workspace: PASS / LIMITED
- Google Drive required: NO
- ChatGPT Project required: NO
- Compaction path: NATIVE / VERIFIED-BOUNDARY / LIMITED
- Primary storage: chat-local workspace
- External backup: NOT CONFIGURED / READY / PENDING
- Backup cadence: EVENT-DRIVEN + HASH-GATED
- Backup authority direction: LOCAL → EXTERNAL
```

---

> **Rebirth principle**
>
> **The transcript may remain. The active context may die. The checkpoint bridges the transition. The Root preserves truth. Skills preserve reusable capability. The same project continues.**
