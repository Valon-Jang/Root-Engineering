# Root Engineering 1.0 Rebirth — Persistent Thread Fusion Contract

Status: normative integration contract for Root Engineering `1.0.0` Rebirth  
Version impact: none; package and schema remain `1.0.0`  
Research provenance: `Valon-Jang/persistent-project-thread`

## 1. Purpose

This document fuses the verified Persistent Project Thread findings into Root Engineering Rebirth **without creating a second canonical system or a competing `압축해` Skill**.

The integration principle is:

> **Research may discover behavior. Rebirth owns the production contract.**

Persistent Project Thread remains the independent experiment and evidence repository. Root Engineering Rebirth is the canonical operational implementation.

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
- same-thread rehydration

Do not install a second `persistent-project-thread` Skill into the same trigger scope. Its verified findings are absorbed into the Rebirth Skill; its repository remains linked as evidence.

This prevents:

- duplicate save gates;
- conflicting compaction priority;
- double backup attempts;
- repeated no-op boundaries;
- ambiguous success reporting.

## 4. Fused state model

Rebirth keeps the three-memory-layer model and adds two supporting resources:

```text
CHAT TRANSCRIPT
= human-visible retained history

ACTIVE MODEL CONTEXT
= compactable inference working memory

LOCAL ROOT
= durable canonical project state

CHECKPOINT
= immediate resume bridge across context replacement

LOCAL CAPABILITY WORKSPACE
= reusable Skills, verified hot paths, helpers, manifests, and runtime assets
```

`CHECKPOINT` is not long-term knowledge. The Local Capability Workspace is not a second Root.

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
14. Continue the same Chat.
```

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

Do not dump the transcript. Do not create a second canonical owner when one already exists.

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

## 9. Transcript rule

Compaction maintains active model context; it does not request deletion of the human-visible transcript.

The tested Persistent Project Thread retained scrollable pre-compaction messages while the active context was repeatedly compacted. This supports an operational distinction, not a claim about ChatGPT's private database design.

```text
human historical inspection → transcript
model working-memory relief → compaction
project truth              → Local Root
immediate continuation     → CHECKPOINT
reusable behavior          → capability workspace
```

## 10. MD synchronization rules

1. English installer is canonical; Korean installer must be a semantic mirror.
2. Backup details live in the backup-policy documents; other files summarize and link rather than fork the policy.
3. Persistent-thread research details remain in the research repository; Rebirth imports only verified operational conclusions.
4. The Skill stays shorter than the installer and routes to canonical owners.
5. A changed production rule must update every affected semantic mirror and validator in the same patch.
6. No patch may add a second canonical `압축해` owner.
7. Package/schema remain `1.0.0` for this fusion because the existing layout and identity contracts remain compatible.

## 11. Acceptance gate

PASS only when:

- document authority is explicit;
- one trigger owner exists;
- Root resolution precedes persistence;
- storage health is checked against the actual Root filesystem;
- smallest-owner save and CHECKPOINT read-back verify;
- external backup defaults to `EXPLICIT_COMPACT_ONLY`, remains hash-gated, adapter-gated, and one-way;
- ordinary and strict backup failure semantics remain distinct;
- compaction success is observed before epoch advancement;
- same-thread rehydration is defined;
- capability assets are indexed without becoming a competing Root;
- English/Korean semantics do not diverge in the touched scope;
- the research repository is cited as provenance, not production authority.

---

> **Transcript can remain. Active context can be compacted. Checkpoint bridges the transition. Root preserves truth. Skills preserve reusable capability. The same project continues.**
