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
---

# ROOT ENGINEERING 1.0.0 — REBIRTH

> **Model is replaceable. Context is replaceable. Root persists.**
>
> **Save the state → compact the context → rehydrate the work → continue the same Chat.**

This is the canonical Chat-native installer for Root Engineering 1.0.0 — **Rebirth**.
It is designed for an ordinary ChatGPT conversation and does not require a ChatGPT Project or Google Drive.

## 0. Rebirth architecture

Rebirth separates three resources that a long-running chat must not confuse:

```text
CHAT TRANSCRIPT
= human-visible history

ACTIVE MODEL CONTEXT
= compactable working memory

LOCAL ROOT
= durable canonical project state inside the current Chat runtime
```

Default runtime path:

```text
/mnt/data/root-engineering/
```

The method does not claim that `/mnt/data` survives every future Chat/runtime lifecycle. Local ROOT is the primary **current-runtime** store. Google Drive, Git, or exported files may be used as optional backup/recovery adapters.

## 1. Installation agent contract

When the user says `설치해`, `install`, or equivalent, do the work instead of merely explaining it.

### Preflight

1. Confirm a writable chat-local file workspace exists.
2. Prefer `/mnt/data`; if unavailable, use the host-exposed writable workspace and record the actual path.
3. Verify create → read → update → read-back on a temporary file.
4. Detect whether a Root already exists at the chosen path.
5. Never overwrite an unidentified existing Root.

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
├── sources/
└── scratch/
```

Use random stable `PROJECT_ID`, `ROOT_ID`, and `NODE_ID` values. Human-readable names may change; IDs do not.

### Existing Drive-based Root

If an older Root Engineering installation is explicitly available and the user is upgrading:

1. Read the latest Drive ROOT and required Branches through exact IDs/live access.
2. Preserve the existing Project ID and Root ID when identity is proven.
3. Copy canonical semantic content into the matching local MD owners.
4. Do not indiscriminately download large Sources. Preserve Source IDs/URLs and retrieve them only when needed.
5. Leave the Drive Root intact as a recovery source unless the user explicitly changes that policy.
6. Verify the local Root before making it primary.

## 2. Kernel rules

### 2.1 Fast path

If the current request is self-contained and does not require stored project state, answer from the current conversation without loading the Root.

### 2.2 Project-dependent boot

When stored project state is required:

```text
read BOOT.md
→ read ROOT.md
→ read runtime/CHECKPOINT.md only when continuing active work
→ read only routed knowledge needed for the request
```

Do not preload the entire tree.

### 2.3 Save gate

Persist only information whose loss would materially increase the chance that a future model must rediscover it, make a worse decision, or repeat a previous failure.

Do not store:

- raw transcript dumps;
- private chain-of-thought;
- disposable brainstorming;
- unverified model inference as fact;
- duplicate canonical truth.

### 2.4 Save placement

- `knowledge/FOUNDATION.md`: purpose, durable principles, long-term boundaries, essential Human Intent.
- `knowledge/CURRENT.md`: currently valid facts, state, decisions, constraints, important unresolved items.
- `knowledge/LEARNED.md`: verified reusable methods and generalized lessons.
- `knowledge/OPERATIONAL.md`: exact repeated-operation keys, safe failure fingerprints, do-not-repeat constraints, verified hot paths, required evidence.
- `knowledge/HISTORY.md`: superseded states whose rationale, rollback, or failure-prevention value remains useful.
- `runtime/CHECKPOINT.md`: ephemeral-but-essential resume state for the work currently in progress.
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

## 3. Local write transaction

For durable local state changes:

```text
resolve exact owner
→ read current owner
→ compute minimum semantic patch
→ write candidate atomically when possible
→ read back affected logical scope
→ accept only after verification
```

When code/file tools allow it, prefer same-directory temporary write + `os.replace()` to avoid torn files.
For ordinary low-risk patches, exact affected-scope read-back is sufficient.
For high-risk identity/routing changes, verify the complete affected relationship.

If a write cannot be verified, report the failure and keep the previous canonical state.

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
Read ROOT routing, then this checkpoint, then only the required owners. Continue from Next without reconstructing completed discussion.
```

Every deliberate compaction refreshes CHECKPOINT even when no new long-term Root knowledge was created.

## 5. `압축해` / COMPACT transaction

When the user says `압축해`, `컴팩션`, `채팅 정리해`, `compact`, or equivalent, treat it as a state transaction, not a summarization request.

### User-visible status

At the start, show a short natural status such as:

```text
현재 작업을 저장 중입니다…
```

After persistence verifies:

```text
저장 완료. 대화를 압축 중입니다…
```

After successful compaction and rehydration:

```text
압축 완료. 이어서 진행합니다.
```

### Internal order — non-negotiable

```text
1. Inspect new durable state since the last canonical update.
2. Route durable items to the smallest correct Root owners.
3. Refresh runtime/CHECKPOINT.md.
4. Verify every required write.
5. IF verification fails → STOP. DO NOT COMPACT.
6. Attempt active-context compaction using the priority below.
7. Verify compaction using a host-exposed/native confirmation or a previously demonstrated reliable signal.
8. On success, increment context_epoch in runtime/STATE.json.
9. Rehydrate from BOOT + CHECKPOINT + only required Root owners.
10. Continue the same Chat.
```

### Compaction priority

#### Priority A — supported native compact action

If the current host explicitly exposes and supports a compact action/API/tool, use it.
Never invent or assume access to a private/internal RPC.

#### Priority B — verified zero-output boundary fallback

Use only when ALL are true:

1. the same environment/thread class has already demonstrated automatic compaction at a tool/sampling boundary;
2. a zero-output/no-op boundary is available;
3. compaction success can be observed or reliably confirmed.

Then:

```text
persist + verify
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

Only for diagnosis when compaction is required, no native path is exposed, and Priority B is not sufficient.
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

Never deliberately compact meaningful active context when required durable state or CHECKPOINT persistence is unverified.

## 6. Context Epoch

`runtime/STATE.json` tracks context lifecycle, not project truth.

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
  "boundary_verification_scope": null
}
```

Increment `context_epoch` and `compaction_count` only after compaction is confirmed.
A verified boundary fallback is scoped to its proven environment/preconditions and must not silently transfer to a different runtime.

## 7. Transcript rule

Compaction is not transcript deletion.
Do not claim that provider-side raw logs, audit records, safety records, or the user's visible chat have been physically deleted.

Operationally keep the layers separate:

```text
Human wants historical conversation → visible transcript / explicit retrieval
Model needs smaller working memory  → active-context compaction
Project needs authoritative truth    → Local ROOT
Work needs immediate resumption      → CHECKPOINT
```

## 8. Production Quiet

During ordinary work, perform routing, reads, and verified persistence quietly.
Do not expose internal Root/Branch/Flush jargon unless the user asks about the architecture or a maintenance operation is underway.

`압축해` is an explicit maintenance command, so the short save/compact status messages in Section 5 are allowed and recommended.

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
Use them when the user wants cross-runtime recovery, durable off-chat backup, collaboration, version history, or migration.

Never claim chat-local `/mnt/data` is permanent across all future sessions unless that durability is actually verified by the host.

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
Persist durable state → Refresh CHECKPOINT → Verify → Compact → Rehydrate → Continue same Chat.

Hard rule: save failure = no compact.
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

### runtime/CAPABILITIES.json

```json
{
  "schema_version": "1.0.0",
  "local_workspace": "VERIFIED",
  "workspace_path": "/mnt/data/root-engineering",
  "native_compact_action": "UNKNOWN",
  "zero_output_boundary_compaction": "UNVERIFIED",
  "external_backup_adapter": "OPTIONAL"
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
3. BOOT routes to the actual Root/Checkpoint/State paths;
4. an ordinary self-contained request can avoid loading the Root;
5. a project-dependent request can load only the required owners;
6. a durable decision can be patched and read back correctly;
7. CHECKPOINT can be refreshed independently of long-term knowledge;
8. a simulated failed save prevents the compaction phase;
9. known Operational failures are not replayed unchanged;
10. no installation step requires Google Drive or a ChatGPT Project;
11. `/mnt/data` durability is not overstated;
12. compaction capability state is honest: supported, verified fallback, or unavailable/unknown.

## 12. REPAIR

Repair the smallest damaged owner.
Do not regenerate a healthy Root wholesale.
Preserve stable IDs and unrelated content.
When identity cannot be proven, stop instead of silently adopting another Root.

## 13. EXPORT / BACKUP

When the user requests backup or cross-runtime recovery, create a complete export bundle of the canonical local Root structure. External adapters may then upload/commit that bundle without changing the local Root's authority unless the user explicitly changes the primary adapter.

## 14. Acceptance gate for Rebirth

A strong Rebirth validation should eventually test repeated cycles:

```text
work
→ durable-state promotion
→ CHECKPOINT
→ verified compaction
→ rehydrate
→ continue same Chat
```

Measure at minimum:

- same-thread continuation;
- state accuracy after compaction;
- decision retention;
- checkpoint resume accuracy;
- no-repeat operational behavior;
- context/latency trend where observable;
- quality loss across repeated compactions.

Do not claim universal one-chat-forever behavior from a single environment. Rebirth makes that an explicit runtime goal with capability-gated compaction.

## 15. Completion report

After installation and verification:

```text
Root Engineering 1.0.0 — Rebirth ready

- Local Root: PASS
- ROOT routing: PASS
- CHECKPOINT runtime: PASS
- Local write/read-back: PASS
- Save-failure compaction guard: PASS
- Operational Memory: PASS
- Google Drive required: NO
- ChatGPT Project required: NO
- Compaction path: NATIVE / VERIFIED-BOUNDARY / LIMITED
- Primary storage: chat-local workspace
```

---

> **Rebirth principle**
>
> **The transcript may remain. The active context may die. The checkpoint bridges the transition. The Root preserves truth. The same project continues.**
