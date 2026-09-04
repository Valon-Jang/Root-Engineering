---
name: root-engineering-rebirth
description: Operate Root Engineering 1.0 Rebirth in one long-lived ordinary ChatGPT conversation using a chat-local Root, resumable Checkpoint, verified compaction transaction, and same-thread rehydration. Use when the user asks to install Rebirth, keep one project in one chat, save and compact the chat, continue after compaction, verify or repair the local Root, export a recovery snapshot, or migrate an older Root.
---

# Root Engineering 1.0 — Rebirth Skill

Package version: `1.0.0`

## Operating model

```text
Chat Transcript      = human-visible history
Active Model Context = compactable working memory
Local ROOT           = durable canonical project state
CHECKPOINT            = transient resume state
```

Default local path:

```text
/mnt/data/root-engineering
```

ChatGPT Project and Google Drive are not routine requirements. `/mnt/data` lifetime remains host-controlled, so external snapshots may be used for backup or recovery.

## Install / verify

Follow the canonical Rebirth installer. When the transaction helper is available, copy it into:

```text
/mnt/data/root-engineering/tools/rebirth_transaction.py
```

Then run:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py self-test
python /mnt/data/root-engineering/tools/rebirth_transaction.py --root /mnt/data/root-engineering verify
```

Do not report the runtime ready unless the local Root and helper both verify.

## `압축해` transaction

Treat `압축해`, `컴팩션`, `리버스`, and `rebirth` as:

```text
Persist → Checkpoint → Verify → Compact → Rehydrate
```

### 1. Show save status

```text
현재 작업을 저장 중입니다…
```

### 2. Persist durable state

Read the latest exact owners. Promote only new durable state to the smallest correct location:

- `knowledge/FOUNDATION.md`: durable purpose, principles, boundaries, Human Intent;
- `knowledge/CURRENT.md`: currently valid facts, decisions, status, constraints, important unresolved items;
- `knowledge/LEARNED.md`: verified reusable methods and generalized lessons;
- `knowledge/OPERATIONAL.md`: exact operation keys, known failures, do-not-repeat rules, verified hot paths, evidence gates;
- `knowledge/HISTORY.md`: superseded states with transition, rollback, or prevention value;
- `ROOT.md`: identity, routing, topology, compact digest only.

Do not dump the transcript. Do not store transient work in canonical knowledge.

### 3. Write the resume Checkpoint

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering checkpoint \
  --goal "<CURRENT_GOAL>" \
  --active-work "<ACTIVE_WORK>" \
  --completed "<COMPLETED_SINCE_LAST_CHECKPOINT>" \
  --promoted "<DURABLE_STATE_PROMOTED>" \
  --unresolved "<IMPORTANT_UNRESOLVED>" \
  --next-action "<EXACT_NEXT_ACTION>" \
  --resume "Read BOOT, ROOT, and CHECKPOINT; load only owners needed for the exact next action."
```

Every field must be explicit. Use `None` when there is genuinely no item; do not leave fields blank.

### 4. Seal the transaction

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering prepare-compact --reason user-requested
```

This seals the canonical digest and Checkpoint hash. **Save or verification failure means no compaction.**

### 5. Show compact status

Only after the transaction is sealed:

```text
저장 완료. 대화를 압축 중입니다…
```

### 6. Compact with capability gating

Priority:

1. Use an explicit native compact action only when the current host actually exposes and supports it.
2. Otherwise use exactly one zero-output tool/sampling boundary only when matching environment evidence already verified that path and success can be observed.
3. Otherwise stop or use bounded diagnostic pressure in small increments. Never default to thousands of disposable lines.

Never invent or call a private/internal RPC.

The reference no-op is semantically:

```python
pass
```

The useful event is the boundary, not the statement.

### 7. Complete or abort

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

The helper refuses to advance the epoch if Root or Checkpoint changed after sealing.

### 8. Rehydrate and continue

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

- Save failure = no compact.
- No observed success = no epoch increment.
- Do not claim compaction deletes the visible transcript or provider-side records.
- Do not claim `/mnt/data` is universally permanent.
- Do not repeatedly fire boundaries when success cannot be verified.
- Stop triggering immediately after success.
- Do not create a new Chat merely because the current one is long when verified Rebirth continuity is available.

## Backup

At meaningful milestones:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering export
```

Use the resulting ZIP as an optional external recovery snapshot.
