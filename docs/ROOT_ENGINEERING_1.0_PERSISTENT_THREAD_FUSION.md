# Root Engineering 1.0 Rebirth — Persistent Thread Fusion Contract

Status: normative integration contract for Root Engineering `1.0.0` Rebirth  
Version impact: none; package and schema remain `1.0.0`  
Research provenance: `Valon-Jang/persistent-project-thread`

## 1. Purpose

This document fuses the verified Persistent Project Thread findings into Root Engineering Rebirth **without creating a second canonical system or a competing `압축해` Skill**.

The integration principle is:

> **Research may discover behavior. Rebirth owns the production contract.**

Persistent Project Thread remains the independent experiment and evidence repository. Root Engineering Rebirth is the canonical operational implementation.

The 2026-09-05 long-horizon observation also falsified the stronger assumption that successful active-context compaction can make one ChatGPT thread indefinitely persistent. Rebirth therefore absorbs a new architectural conclusion:

> **The thread is an execution resource, not the persistence authority.**

Current Rebirth `1.0.0` still operates inside one Chat when that Chat remains viable. Automatic thread/session rollover is **not** claimed as implemented in this version. The research direction, however, now treats thread replacement as compatible with project continuity because project authority belongs to Root/Checkpoint rather than the thread itself.

## 2. Authority map

Each document has one role.

| Resource | Authority role |
|---|---|
| `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md` | canonical English installation/runtime contract |
| `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md` | Korean semantic mirror of the English installer |
| `docs/ROOT_ENGINEERING_1.0_REBIRTH.md` | architecture explanation; must not override the installer |
| `docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md` | normative delegated external-backup policy |
| `docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY_KO.md` | Korean semantic mirror of the backup policy |
| this document | normative fusion and cross-document ownership contract |
| `installer/rebirth/root-engineering/SKILL.md` | executable hot path; summarizes and routes, but must not invent competing policy |
| `installer/rebirth/runtime/rebirth_transaction.py` | deterministic local transaction guard; does not itself compact ChatGPT or provide a Google Drive adapter |
| `Valon-Jang/persistent-project-thread` | research/evidence provenance; not a runtime authority for an installed Rebirth Root |

When two files appear to conflict, resolve by this order:

```text
current user/system/project instructions
→ canonical Rebirth installer
→ delegated normative policy/fusion documents
→ Rebirth Skill
→ explanatory docs
→ research evidence
```

Recency alone does not create authority.

## 3. One trigger owner

Within a Rebirth installation, `root-engineering-rebirth` is the sole operational owner of:

- `압축해`
- `컴팩션`
- `채팅 정리해`
- `백업하고 압축해`
- same-thread rehydration while the current Chat remains viable

Do not install a second `persistent-project-thread` Skill into the same trigger scope. Its verified findings are absorbed into the Rebirth Skill; its repository remains linked as evidence.

This prevents:

- duplicate save gates;
- conflicting compaction priority;
- double backup attempts;
- repeated no-op boundaries;
- ambiguous success reporting.

Automatic provider-thread rollover is outside the current `1.0.0` executable trigger contract. If a future version implements it, Root Engineering remains the sole owner of the rollover policy and persistence gate.

## 4. Fused state model

Rebirth now distinguishes the thread/session surface from the memory and persistence layers:

```text
THREAD / CHAT SURFACE
= current product-level execution container; usable while viable, not canonical project identity

CHAT TRANSCRIPT
= human-visible retained history; may accumulate independently of active context

ACTIVE MODEL CONTEXT
= compactable inference working memory

LOCAL ROOT
= durable canonical project state

CHECKPOINT
= immediate resume bridge across context replacement and future session replacement

LOCAL CAPABILITY WORKSPACE
= reusable Skills, verified hot paths, helpers, manifests, and runtime assets
```

The tested long-horizon ChatGPT workflow showed that repeated active-context compaction did not make the same thread indefinitely usable. The exact internal cause of that product/thread-level boundary is unknown; this contract does not claim a specific OpenAI retention rule, token threshold, UI threshold, database limit, or private implementation detail.

The architecture-level invariant is narrower and stronger:

```text
PROJECT / AGENT IDENTITY
    ≠ THREAD
    ≠ CHAT TRANSCRIPT
    ≠ ACTIVE MODEL CONTEXT
    ≠ TOOL / MODEL RUNTIME
```

`CHECKPOINT` is not long-term knowledge. The Local Capability Workspace is not a second Root. The thread itself is also not a Root.

Canonical capability meaning belongs in:

- `knowledge/OPERATIONAL.md` for verified procedures, failure fingerprints, and do-not-repeat rules;
- `runtime/CAPABILITIES.json` for runtime availability, paths, hashes, scope, and verification state;
- `ROOT.md` only for routing/pointers when required.

Large model files, WAVs, caches, and generated artifacts are linked by path/hash when useful; they are not duplicated into canonical MD or included in the canonical Root hash by default.

## 5. Pre-Compaction Save Gate

A deliberate compact command is a state transaction, not a summary request.

The fused order is non-negotiable:

```text
1. Resolve the exact Local Root.
2. Read ROOT routing and the current CHECKPOINT only as needed.
3. Detect new durable state since the last canonical update.
4. Route each durable item to the smallest canonical owner.
5. Check the filesystem that actually contains the Root.
6. Patch the required owner(s) and refresh CHECKPOINT.
7. Read back and verify every required local write.
8. Seal the canonical digest + CHECKPOINT hash.
9. Synchronize configured recovery during this explicit compact maintenance window.
10. Attempt active-context compaction through the capability ladder.
11. Verify compaction.
12. Advance the context epoch only after verified success.
13. Rehydrate from BOOT → ROOT → CHECKPOINT → required owners only.
14. Continue the same Chat while that thread remains viable.
```

Compaction is therefore a **context-maintenance operation**, not a guarantee of thread permanence.

If the current thread later becomes unavailable, the current `1.0.0` package does not claim an automatic transparent rollover mechanism. The project state must already be safe in Root/Checkpoint and any configured recovery copy before an explicit restore or future rollover path is attempted.

### 5.1 Root resolution

Priority:

1. explicit Root path in current instructions;
2. already verified active Root binding;
3. documented project-local Root entry point;
4. default `/mnt/data/root-engineering` only when it is the verified installation path.

Once the Local Root is resolved, do not search File Library, Drive, GitHub, or Web for a competing copy merely to prepare compaction.

If a trustworthy Root cannot be resolved and new durable state must be saved, stop before compaction.

### 5.2 Smallest-owner routing

```text
ROOT.md                 → identity, authority, routing, compact digest
knowledge/FOUNDATION.md → durable purpose, principles, boundaries, Human Intent
knowledge/CURRENT.md    → currently valid facts, decisions, status, constraints, unresolved items
knowledge/LEARNED.md    → verified generalized learning
knowledge/OPERATIONAL.md→ verified hot paths, capability procedures, known failures, evidence gates
knowledge/HISTORY.md    → superseded state with transition/rollback/prevention value
runtime/CHECKPOINT.md   → immediate resume state only
runtime/CAPABILITIES.json → availability/path/hash/scope of executable capabilities
```

Do not dump the transcript. Do not create a second canonical owner when one already exists. Do not treat the current provider thread as a canonical owner.

## 6. Local Storage Gate

Before accepting the pre-compaction save, inspect the filesystem that owns the resolved Root path.

Verify at minimum:

- the filesystem and target directory exist;
- the target is writable;
- sufficient free bytes exist for the intended patch/checkpoint/export operation;
- sufficient free inodes exist where inode accounting is available;
- the actual write can be read back;
- a failed candidate write leaves the previous canonical state intact.

Do not hard-code the capacity measured in one Chat runtime. Storage size, quota, mount, and lifetime are environment properties.

> **Required local save failure = no compact.**

Free-space capacity and persistence lifetime are different. A large writable `/mnt/data` does not prove survival across every future runtime replacement.

## 7. External backup fusion

External backup behavior is owned by `ROOT_ENGINEERING_1.0_BACKUP_POLICY.md`.

### Ordinary `압축해`

```text
verified Local Root save
→ compute canonical Root hash
→ external adapter configured and target binding verified?
   ├── no  → no external write; continue to compaction
   └── yes
       ├── hash unchanged → skip upload
       └── hash changed   → update verified `latest`
```

A policy declaration is not an executable adapter. Google Drive synchronization occurs only when:

1. a Google Drive connector/tool or other valid adapter is actually available;
2. the project backup target is bound unambiguously;
3. the upload is executed;
4. the uploaded manifest/bundle is read back or otherwise verified.

For ordinary `압축해`, optional external-backup failure sets `external_backup_pending = true`; verified Local Root remains authoritative and compaction may continue with a visible warning.

### Strict `백업하고 압축해`

Local save and external backup must both verify. Missing adapter, ambiguous Drive target, upload failure, or failed read-back means **no compact**.

### Authority direction

Normal operation is one-way:

```text
Local Root → external latest/snapshot
```

Do not automatically merge Drive changes back into Local Root. Restore is explicit and identity/hash verified.

## 8. Compaction capability ladder

```text
A. host-exposed supported native compact action
↓ unavailable
B. exactly one previously verified zero-output boundary in matching scope
↓ unsuccessful/unverifiable
C. bounded diagnostic pressure in small increments
↓ unsuccessful
STOP and diagnose
```

Never invent a private RPC. Never treat a no-op as a universal force-compact command. Stop triggering immediately after verified success.

The minefield and trigger-reduction experiments are research provenance, not production assumptions.

Compaction success proves only that active-context maintenance succeeded. It does **not** prove that the human-visible transcript shrank or that the product thread gained unlimited lifetime.

## 9. Transcript and thread rule

Compaction maintains active model context; it does not request deletion or compression of the human-visible transcript.

The tested Persistent Project Thread retained scrollable pre-compaction messages while the active context was repeatedly compacted. A later long-horizon observation found that the accumulated thread eventually became unavailable for continued work despite successful context compaction.

These two findings must be kept together:

```text
human historical inspection → transcript
model working-memory relief → compaction
current execution container → thread / Chat surface
project truth              → Local Root
immediate continuation     → CHECKPOINT
reusable behavior          → capability workspace
```

Therefore:

> **Active-context lifetime and thread lifetime are different problems.**

The current ChatGPT-hosted limitation is treated as a product/thread boundary discovered by experiment, not as the end of the Root Engineering research program.

Research provenance:

- `Valon-Jang/persistent-project-thread/evidence/LONG_HORIZON_THREAD_LIMIT_2026-09-05.md`

## 10. Research continuation — thread-replaceable continuity

The falsified question was:

> **How do we make one ChatGPT thread permanent?**

Root Engineering continues with the more general question:

> **How do we make the project survive models, contexts, runtimes, and threads?**

Architecture-level research directions include:

- provider-session/thread rollover behind one stable project identity;
- Root + Checkpoint rehydration into a fresh execution surface;
- human-view compression where raw history is preserved separately from what is rendered by default;
- transcript/event retrieval without loading the whole history into active context;
- agent identity that survives model, session, and runtime replacement;
- lifecycle health signals for deciding when to compact context versus when to replace a session.

These are research directions. They are **not** claims that current ChatGPT Rebirth `1.0.0` already performs transparent thread rollover or human-visible transcript compression.

The generalized principle is:

> **Model is replaceable. Context is replaceable. Thread is replaceable. Root persists.**

## 11. MD synchronization rules

1. English installer is canonical; Korean installer must be a semantic mirror.
2. Backup details live in the backup-policy documents; other files summarize and link rather than fork the policy.
3. Persistent-thread research details remain in the research repository; Rebirth imports only verified operational conclusions.
4. The Skill stays shorter than the installer and routes to canonical owners.
5. A changed production rule must update every affected semantic mirror and validator in the same patch.
6. No patch may add a second canonical `압축해` owner.
7. Package/schema remain `1.0.0` for this fusion because the existing layout and identity contracts remain compatible.
8. Research conclusions about thread replaceability must not be misrepresented as an implemented transparent rollover feature.

## 12. Acceptance gate

PASS only when:

- document authority is explicit;
- one trigger owner exists;
- Root resolution precedes persistence;
- storage health is checked against the actual Root filesystem;
- smallest-owner save and CHECKPOINT read-back verify;
- external backup defaults to `EXPLICIT_COMPACT_ONLY`, remains hash-gated, adapter-gated, and one-way;
- ordinary and strict backup failure semantics remain distinct;
- compaction success is observed before epoch advancement;
- same-thread rehydration is defined for the current `1.0.0` operating scope;
- the current thread is not treated as canonical project identity or a guaranteed permanent resource;
- no automatic thread rollover is claimed unless separately implemented and verified;
- capability assets are indexed without becoming a competing Root;
- English/Korean semantics do not diverge in the touched scope;
- the research repository is cited as provenance, not production authority.

---

> **Transcript may remain. Active context can be compacted. Thread may still end. Checkpoint bridges transitions. Root preserves truth. Skills preserve reusable capability. The same project can continue beyond replaceable execution resources.**

> **Model is replaceable. Context is replaceable. Thread is replaceable. Root persists.**
