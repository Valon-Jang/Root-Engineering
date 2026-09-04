---
name: root-engineering-rebirth
description: Install and operate Root Engineering 1.0 Rebirth in one long-lived ordinary ChatGPT conversation using a chat-local Root, resumable Checkpoint, verified compaction transaction, and same-thread rehydration. Use when the user asks to install Rebirth, keep one project in one chat, save and compact the chat, resume after compaction, verify or repair the local Root, or migrate an existing Root Engineering project to the chat-local runtime.
---

# Root Engineering 1.0 — Rebirth Skill

Package version: `1.0.0-rc.1`

## Trigger phrases

Use this Skill for:

- `설치해`, when this Rebirth package is attached or selected;
- `압축해`, `컴팩션`, `리버스`, `rebirth`;
- `현재 작업 저장하고 압축해`;
- `이 프로젝트는 이 채팅 하나로 계속 가자`;
- local Root verify/repair/export/migration requests.

## Operating model

```text
Transcript      = human-visible history
Active context  = compactable working memory
Local ROOT      = durable canonical state
CHECKPOINT      = transient resume state
```

Default local path:

```text
/mnt/data/root-engineering
```

## Installation

Do not merely explain the installer. When local writable execution is available:

1. read the complete installer and protocol;
2. run a real write/read/rename/delete preflight under `/mnt/data`;
3. detect an existing Rebirth installation;
4. create or repair only missing/invalid paths;
5. preserve existing canonical files unless an exact upgrade delta is required;
6. generate actual project IDs and replace all placeholders;
7. install `rebirth_runtime.py` and `noop_boundary.py`;
8. run `verify`;
9. report ACTIVE only after readback and hash verification pass.

Do not require ChatGPT Project, Project Instructions, or Google Drive.

## `압축해` transaction

### Visible status 1

Before tool/file operations, say:

```text
현재 작업을 저장 중입니다…
```

### Save

- Read `PROTOCOL.md`, `ROOT.md`, current canonical owners, and CHECKPOINT.
- Promote only new durable state to the smallest correct owner.
- Put in-flight continuation state in CHECKPOINT.
- Use atomic replacement and readback verification.
- Run `verify`, then `prepare-compact`.

If any required write or verification fails, do not compact.

### Visible status 2

After the transaction is sealed:

```text
저장 완료. 대화를 압축 중입니다…
```

### Compact

1. Use an explicit native compact action only if the host actually exposes it.
2. Otherwise use exactly one zero-output boundary only if `CAPABILITIES.json` says it was verified under matching conditions and success can be observed.
3. Otherwise stop or run bounded diagnostics; never flood the chat by default.
4. Never invent a private RPC.

The reference no-op is:

```python
pass
```

The useful event is the tool/sampling boundary, not the statement.

### Complete and rehydrate

On verified success:

1. run `complete-compact --observed --method <method> --signal <signal>`;
2. read BOOT, ROOT, CHECKPOINT;
3. read only needed owners;
4. continue the exact next action in the same chat;
5. say:

```text
압축 완료. 이어서 진행할게.
```

If success is not verifiable, run `abort-compact` and state plainly that the context was not marked compacted.

## Non-negotiable guards

- Save failure = no compact.
- Do not dump the transcript into ROOT.
- Do not store temporary work in canonical knowledge.
- Do not claim `/mnt/data` is universally permanent.
- Do not claim visible transcript was deleted.
- Do not claim provider-side raw records were deleted.
- Do not increment context epoch without evidence.
- Stop immediately after verified compaction.
- Do not create a new chat merely because the current one is long when verified Rebirth can preserve continuity.

## RC.1 deterministic command contract

Use the installed `tools/rebirth_runtime.py` helper for checkpoint sealing and epoch accounting:

```text
checkpoint
→ prepare-compact
→ host/native or verified boundary compaction
→ complete-compact --observed --method <method> --signal <signal>
```

`complete-compact` must fail closed when the current canonical digest or Checkpoint hash differs from the values sealed by `prepare-compact`. In that case abort and prepare again; never advance the context epoch against modified state.
