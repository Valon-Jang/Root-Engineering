# Root Engineering 1.0 Rebirth — External Backup Policy

Status: normative policy for Root Engineering 1.0.0 Rebirth  
Version impact: none; package and schema remain `1.0.0`

## 1. Purpose

Rebirth uses the chat-local Root as the primary current-runtime authority. External storage such as Google Drive, Git, or an exported bundle is a backup, recovery, collaboration, or migration adapter.

The backup policy must protect recovery without turning every ordinary conversation turn into an external write.

## 2. Core rule

> **Local state is saved by meaning. External backup is synchronized by event.**

Do not depend on a hidden background timer in an ordinary Chat.

```text
Local Root change
→ verify local write
→ compute canonical Root hash
→ wait for a qualifying backup event
→ unchanged hash: skip
→ changed hash: update verified latest backup
```

## 3. Default cadence

| Event | Action |
|---|---|
| ordinary conversation | no external write |
| verified Local Root patch | mark backup pending when canonical hash changed |
| `압축해` / `compact` | update `latest` only if adapter is configured and hash changed |
| critical authority, routing, or structure change | update `latest` immediately when configured |
| `백업해` / `backup` | force immediate verified `latest` backup |
| `백업하고 압축해` / `backup and compact` | require verified external backup before compaction |
| `마무리하자` / explicit closeout | update `latest` when changed |
| release, named milestone, migration, restore, destructive change | update `latest` and create immutable snapshot |
| no hash change | skip upload |

## 4. Latest and snapshots

Recommended layout:

```text
Root Engineering Backups/
└── <PROJECT_ID>/
    ├── latest/
    │   ├── root-engineering-latest.zip
    │   └── BACKUP_MANIFEST.json
    └── snapshots/
        └── <ISO_DATE>_epoch-<N>_<REASON>.zip
```

`latest` is replaceable and optimized for recovery. Replace it only after upload and read-back/hash verification pass.

A snapshot is immutable and should exist only for a meaningful transition:

- release or named milestone;
- adapter/runtime migration;
- restore before accepting different canonical state;
- critical authority, routing, or schema change;
- potentially destructive operation;
- explicit user request.

Do not create a new snapshot for every compaction.

## 5. Canonical hash

Hash a deterministic canonical export set:

```text
BOOT.md
ROOT.md
MANIFEST.json
knowledge/**
runtime/CHECKPOINT.md
runtime/STATE.json
runtime/CAPABILITIES.json
small linked canonical Sources explicitly included by policy
```

Exclude scratch files, caches, timestamps generated only by packaging, and other unstable non-semantic data.

If the current hash equals the last verified backup hash, do not upload again.

## 6. Backup manifest

Minimum fields:

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

The manifest and bundle must agree on identity and hash.

## 7. Failure semantics

Required local persistence and optional external backup are different contracts.

```text
Local Root or CHECKPOINT save failure
→ STOP
→ NO COMPACT
```

For ordinary `압축해`:

```text
optional external backup failure
→ keep verified Local Root authoritative
→ set external_backup_pending = true
→ show a warning
→ compaction may continue
```

For strict `백업하고 압축해`:

```text
Local save and external backup must both verify
→ any required failure = NO COMPACT
```

Retry a pending optional backup at the next qualifying event or explicit `백업해`. Do not loop repeatedly through the same failed path.

## 8. Authority direction

After migrating a Drive-based Root to Rebirth:

```text
Drive canonical read
→ Local conversion
→ Local identity/content verification
→ final migration snapshot
→ former Drive Root retained as legacy/read-only recovery source
→ normal operation becomes Local → external backup
```

Do not automatically merge external changes back into the Local Root during normal operation.

Restore is explicit. Before restoration, verify:

- Project ID;
- Root ID;
- version/schema compatibility;
- backup manifest;
- content hash;
- intended restore scope.

## 9. Runtime state

Recommended optional fields in `runtime/STATE.json`:

```json
{
  "external_backup_adapter": "NONE",
  "external_backup_pending": false,
  "current_root_hash": null,
  "last_backup_root_hash": null,
  "last_backup_at": null,
  "last_snapshot_at": null
}
```

These fields track backup state; they do not change project truth.

## 10. User-visible behavior

During ordinary `압축해`:

```text
현재 작업을 저장 중입니다…
로컬 저장 완료. 복구본을 동기화 중입니다…
복구본 동기화 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행합니다.
```

When optional backup fails:

```text
로컬 저장은 완료됐지만 복구본 동기화는 보류됐습니다. 대화 압축은 계속합니다.
```

When strict backup fails:

```text
로컬 저장은 완료됐지만 요청한 복구본을 검증하지 못해 대화 압축을 중단했습니다.
```

## 11. Acceptance conditions

PASS only when:

1. package and schema versions remain `1.0.0`;
2. backup is event-driven rather than timer-dependent;
3. unchanged canonical hashes skip upload;
4. `latest` is verified before replacement is accepted;
5. snapshots are milestone/explicit/migration/critical-change gated;
6. ordinary optional-backup failure marks pending and may continue compaction;
7. strict backup-and-compact failure blocks compaction;
8. normal authority direction is Local → external;
9. restore is explicit and identity/hash verified.