---
name: root-engineering-rebirth
description: Operate Root Engineering 1.0 Rebirth in one long-lived ordinary ChatGPT conversation using a chat-local Root, resumable Checkpoint, explicit compact-time recovery sync, verified compaction, and same-thread rehydration. Use for install, verify, repair, backup, compact, or migration requests.
---

# Root Engineering 1.0 — Rebirth Skill

Package version: `1.0.0`

## Operating model

```text
Chat Transcript      = human-visible history
Active Model Context = compactable working memory
Local ROOT           = durable canonical project truth
CHECKPOINT            = immediate resume state
Recovery Mirror       = optional external backup synchronized at explicit maintenance
```

Default Local Root:

```text
/mnt/data/root-engineering
```

ChatGPT Project and Google Drive are not routine requirements. `/mnt/data` lifetime remains host-controlled.

## Install and verify

Follow the canonical Rebirth installer. Install the helper at:

```text
/mnt/data/root-engineering/tools/rebirth_transaction.py
```

Then run:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py self-test
python /mnt/data/root-engineering/tools/rebirth_transaction.py --root /mnt/data/root-engineering verify
```

Do not report READY unless the Local Root, identity, Checkpoint, policy state, and helper verify.

## `압축해` transaction

Treat `압축해`, `컴팩션`, `채팅 정리해`, `리버스`, `rebirth`, and `compact` as:

```text
Persist → Checkpoint → Verify → Backup if configured → Compact → Rehydrate
```

This is the only default external-recovery synchronization boundary. Scheduled sync = disabled. Idle/background sync = disabled.

### 1. Show save status

```text
현재 작업을 저장 중입니다…
```

### 2. Resolve and verify the Local Root

Use an explicit or already verified binding first. Use `/mnt/data/root-engineering` only after identity and write/read-back verification. If durable state must be saved and no trustworthy Root can be resolved, stop. Save failure = no compact.

### 3. Persist new durable state

Patch only the smallest correct owner:

- `knowledge/FOUNDATION.md`: durable purpose, principles, boundaries, Human Intent;
- `knowledge/CURRENT.md`: currently valid facts, decisions, status, constraints, unresolved items;
- `knowledge/LEARNED.md`: verified reusable methods and generalized lessons;
- `knowledge/OPERATIONAL.md`: exact operation keys, known failures, do-not-repeat rules, verified hot paths, evidence gates;
- `knowledge/HISTORY.md`: superseded state with transition, rollback, or prevention value;
- `ROOT.md`: identity, routing, topology, compact digest only.

Do not dump the transcript. Do not store transient work in canonical knowledge.

### 4. Refresh CHECKPOINT

Write current goal, active work, completed work, durable state promoted, important unresolved items, exact next action, and resume instruction to `runtime/CHECKPOINT.md`. Read it back and verify it.

### 5. Seal local state

Run:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering prepare-compact --reason user-requested
```

The helper seals the canonical digest and Checkpoint hash. Required Local Root or Checkpoint save/verification failure means no compact.

### 6. Synchronize external recovery only now

For ordinary `압축해`:

```text
no configured adapter      → skip
configured + unchanged     → skip remote write
configured + changed       → update verified latest recovery object
```

When needed, show:

```text
로컬 저장 완료. 복구본을 동기화 중입니다…
```

Use an actually exposed connector/tool. Verify the returned file identity, hash, or equivalent read-back evidence. Then record the result with `record-backup`:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering record-backup \
  --status VERIFIED \
  --adapter google-drive \
  --artifact-sha256 "<SHA256>" \
  --remote-reference "<VERIFIED_ID_OR_URL>"
```

If optional synchronization fails, record `PENDING`, keep Local Root authoritative, tell the user the recovery copy is pending, and ordinary compaction may continue. Do not silently report success.

For `백업하고 압축해`, external verification is mandatory. Any required failure means no compact.

Do not create scheduled, timer-based, idle, or background synchronization. An explicit `백업해` command may perform one backup without compaction.

### 7. Show compact status

After local state is sealed and backup handling is complete:

```text
저장 완료. 대화를 압축 중입니다…
```

### 8. Compact with capability gating

Priority:

1. use an explicit host-exposed supported native compact action;
2. otherwise use exactly one zero-output tool/sampling boundary only when matching-scope evidence already verified it and success can be observed;
3. use bounded diagnostic pressure only when diagnosis is required;
4. stop if success cannot be verified.

Never invent or call a private/internal RPC. Never assume a no-op universally forces compaction. Stop triggering immediately after success.

An external backup tool call may itself produce the host boundary at which compaction occurs. If that event is confirmed, reuse it as this transaction's compaction and do not fire another trigger.

### 9. Complete or abort

On observed success:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering complete-compact \
  --observed \
  --method <native|zero-output-boundary|manual-confirmation|diagnostic> \
  --signal <HOST_EVENT|CONTEXT_REPLACEMENT_OBSERVED|MANUAL_CONFIRMATION>
```

If success is not verifiable, use `abort-compact`; do not increment context epoch.

### 10. Rehydrate and continue

Read:

```text
BOOT.md
→ ROOT.md
→ runtime/CHECKPOINT.md
→ only owners required by the Exact Next Action
```

Then say:

```text
압축 완료. 이어서 진행할게.
```

Continue the exact next action in the same Chat.

## Hard guards

- Save failure = no compact.
- Storage verification failure = no compact.
- No observed success = no epoch increment.
- External backup sync trigger = explicit compact only.
- Scheduled sync = disabled.
- Idle/background sync = disabled.
- Optional backup failure is visible and recorded as pending.
- Strict backup-and-compact failure = no compact.
- Normal authority direction is Local → external.
- Never invent or call a private/internal RPC.
- Do not claim compaction deletes the visible transcript or provider-side records.
- Do not claim `/mnt/data` is universally permanent.
- Do not load the full transcript or Root tree after compaction.

> **Transcript may remain. Active context may die. Checkpoint bridges the transition. Root preserves truth. The same project continues.**
