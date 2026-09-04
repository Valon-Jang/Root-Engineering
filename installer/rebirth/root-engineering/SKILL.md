---
name: root-engineering-rebirth
description: Operate Root Engineering 1.0 Rebirth in one long-lived ordinary ChatGPT conversation using a chat-local Root, resumable Checkpoint, verified compaction transaction, explicit compact-time external recovery sync, and reusable local capabilities. Use when the user asks to install Rebirth, keep one project in one chat, save and compact the chat, back up and compact, continue after compaction, verify or repair the local Root, export recovery state, or migrate an older Root.
---

# Root Engineering 1.0 — Rebirth Skill

Package version: `1.0.0`

## Canonical owners

This Skill is the single operational owner of `압축해` inside a Rebirth installation, but it is not the full specification.

Read only the owner required for the operation:

- canonical installer: `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md`
- Korean semantic mirror: `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md`
- fusion/authority contract: `docs/ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION.md`
- external-backup policy: `docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md`
- research provenance: `Valon-Jang/persistent-project-thread`

Do not install a second `persistent-project-thread` Skill into the same trigger scope. Its verified findings are fused here; its repository remains evidence, not runtime authority.

## Operating model

```text
Chat Transcript           = human-visible history
Active Model Context      = compactable working memory
Local ROOT                = durable canonical project truth
CHECKPOINT                = immediate resume bridge
Local Capability Workspace= Skills, verified hot paths, helpers, manifests, runtime assets
```

Default local path:

```text
/mnt/data/root-engineering
```

Use the actual verified Root path when the project binds a different location. ChatGPT Project and Google Drive are not routine requirements. `/mnt/data` lifetime remains host-controlled.

Capability meaning belongs in `knowledge/OPERATIONAL.md` and `runtime/CAPABILITIES.json`; large models, WAVs, caches, and generated artifacts remain linked by path/hash rather than copied into canonical MD by default.

## Install / verify

Follow the canonical Rebirth installer. When the transaction helper is available, copy it to:

```text
/mnt/data/root-engineering/tools/rebirth_transaction.py
```

Then run:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py self-test
python /mnt/data/root-engineering/tools/rebirth_transaction.py --root /mnt/data/root-engineering verify
```

Do not report READY unless Root identity, required owners, Checkpoint, and helper verify.

## `압축해` transaction

Treat `압축해`, `컴팩션`, `채팅 정리해`, `리버스`, and `rebirth` as:

```text
Resolve Root
→ Storage Gate
→ Persist
→ Checkpoint
→ Verify
→ Seal
→ Compact-time changed backup
→ Compact
→ Verify compaction
→ Rehydrate
```

### 1. Show save status

```text
현재 작업을 저장 중입니다…
```

### 2. Resolve the exact Local Root

Priority:

1. explicit Root path in current instructions;
2. already verified active Root binding;
3. documented project-local Root entry point;
4. `/mnt/data/root-engineering` only when that installation is verified.

After a valid Local Root is resolved, do not search File Library, Drive, GitHub, or Web for a competing canonical copy merely to prepare compaction.

If durable state must be saved and no trustworthy Root can be resolved, stop. Do not compact blindly.

### 3. Run the Local Storage Gate

Inspect the filesystem that actually owns the Root path. Verify:

- target directory exists and is writable;
- sufficient free bytes for the intended write/export;
- sufficient free inodes when the host exposes inode accounting;
- atomic or failure-safe candidate write is possible;
- write/read-back succeeds.

Never hard-code a capacity measured in another runtime. Free space does not prove future persistence lifetime.

### 4. Persist only new durable state

Read the latest exact owner and apply the minimum semantic patch:

- `knowledge/FOUNDATION.md`: durable purpose, principles, boundaries, Human Intent;
- `knowledge/CURRENT.md`: currently valid facts, decisions, status, constraints, important unresolved items;
- `knowledge/LEARNED.md`: verified reusable methods and generalized lessons;
- `knowledge/OPERATIONAL.md`: exact operation keys, verified hot paths, capability procedures, known failures, do-not-repeat rules, evidence gates;
- `knowledge/HISTORY.md`: superseded state with transition, rollback, or prevention value;
- `runtime/CAPABILITIES.json`: capability availability, path, hash, scope, verification state;
- `ROOT.md`: identity, routing, topology, compact digest only.

Do not dump the transcript. Do not duplicate canonical truth.

### 5. Refresh the resume Checkpoint

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering checkpoint \
  --goal "<CURRENT_GOAL>" \
  --active-work "<ACTIVE_WORK>" \
  --completed "<COMPLETED_SINCE_LAST_CHECKPOINT>" \
  --promoted "<DURABLE_STATE_PROMOTED>" \
  --unresolved "<IMPORTANT_UNRESOLVED>" \
  --next-action "<EXACT_NEXT_ACTION>" \
  --resume "Read BOOT, ROOT, and CHECKPOINT; load only owners required for the exact next action."
```

Every field is explicit. Use `None` when there is genuinely no item; do not leave blanks.

### 6. Verify and seal

Read back every affected local owner, then run:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering prepare-compact --reason user-requested
```

This seals the canonical digest and Checkpoint hash.

> **Required local save or verification failure = no compact.**

### 7. Evaluate external backup

External recovery sync is explicit-compact-time, hash-gated, adapter-gated, and one-way.

Default recovery trigger = explicit `압축해` / `compact` only. Scheduled sync = disabled. Idle/background sync = disabled.

For ordinary `압축해`:

```text
external adapter not configured/bound → skip external write
configured + hash unchanged           → skip upload
configured + hash changed             → update verified `latest`
```

Google Drive sync is successful only when a Drive connector/tool is actually available, the project target is bound unambiguously, upload executes, and the remote bundle/manifest is verified.

When upload is required and begins:

```text
로컬 저장 완료. 복구본을 동기화 중입니다…
```

After verified success:

```text
복구본 동기화 완료. 대화를 압축 중입니다…
```

If optional backup fails during ordinary `압축해`:

- keep Local Root authoritative;
- set `external_backup_pending = true`;
- show: `로컬 저장은 완료됐지만 복구본 동기화는 보류됐습니다. 대화 압축은 계속합니다.`
- continue to compaction.

When no upload is required:

```text
저장 완료. 대화를 압축 중입니다…
```

### 8. Strict `백업하고 압축해`

Treat `백업하고 압축해` / `backup and compact` as strict mode.

Local save and external backup must both verify. Missing adapter, ambiguous target, failed upload, or failed remote verification means:

```text
로컬 저장은 완료됐지만 요청한 복구본을 검증하지 못해 대화 압축을 중단했습니다.
```

Do not compact.

### 9. Compact with capability gating

Priority:

1. explicit host-exposed supported native compact action;
2. exactly one zero-output tool/sampling boundary only when matching-scope evidence already verified it and success can be observed;
3. bounded diagnostic pressure in small increments only when diagnosis is required;
4. stop if success cannot be verified.

Never invent or call a private/internal RPC. Never assume a no-op universally forces compaction. Never default to thousands of disposable lines. Stop triggering immediately after success.

Reference no-op semantics:

```python
pass
```

The useful event is the boundary, not the statement.

### 10. Complete or abort

On observed success:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering complete-compact \
  --observed \
  --method <native|zero-output-boundary|manual-confirmation|diagnostic> \
  --signal <HOST_EVENT|CONTEXT_REPLACEMENT_OBSERVED|MANUAL_CONFIRMATION>
```

If success is not verifiable:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering abort-compact \
  --reason "compaction not observed"
```

The helper refuses epoch advancement if Root or Checkpoint changed after sealing.

### 11. Rehydrate and continue

Read:

```text
BOOT.md
→ ROOT.md
→ runtime/CHECKPOINT.md
→ only owners required by Exact Next Action
```

Then say:

```text
압축 완료. 이어서 진행할게.
```

Continue the exact next action in the same Chat.

## Hard guards

- One Rebirth trigger owner; no duplicate compaction Skill.
- Required local save failure = no compact.
- Storage Gate failure = no compact.
- No observed success = no epoch increment.
- Ordinary optional-backup failure may continue only after pending state is recorded.
- Strict backup-and-compact failure = no compact.
- External policy text is not proof that an adapter executed.
- Normal authority direction is Local → external; no automatic Drive-to-Local merge.
- Do not claim compaction deletes the visible transcript or provider-side records.
- Do not claim `/mnt/data` is universally permanent.
- Do not repeatedly fire boundaries when success cannot be verified.
- Do not load the entire transcript or Root tree after compaction.

## Explicit backup / milestone snapshot

When the user requests `백업해`, export and send through the configured adapter after verification. At release, named milestone, migration, restore, destructive change, or explicit snapshot request, create an immutable snapshot in addition to `latest`.

The local helper can produce an export ZIP:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering export
```

The helper prepares local transaction state and export artifacts. It does not itself prove that Google Drive upload or ChatGPT compaction occurred.

---

> **Transcript can remain. Active context can be compacted. Checkpoint bridges the transition. Root preserves truth. Skills preserve reusable capability. The same project continues.**
