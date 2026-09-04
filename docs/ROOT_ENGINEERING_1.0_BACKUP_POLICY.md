# Root Engineering 1.0 Rebirth — External Recovery Sync Policy

Status: normative policy for Root Engineering 1.0.0 Rebirth  
Version impact: none; package and schema remain `1.0.0`

## 1. Purpose

Rebirth uses the Chat-local Root as the primary authority for the current runtime. Google Drive, Git, or an exported bundle may hold a recovery copy, but external synchronization must not make ordinary Chat work slower.

This policy therefore uses an explicit maintenance boundary:

> **Work locally while the user is working. Synchronize the recovery copy when the user says `압축해` / `compact`.**

An explicit standalone `백업해` / `backup` request is also allowed. Scheduled, idle, timer-based, and background synchronization are disabled by default.

## 2. Why compact-time synchronization

`압축해` already marks the moment when Rebirth must:

1. promote durable state to the correct Root owner;
2. refresh the current-work Checkpoint;
3. verify Local Root integrity;
4. maintain the active model context;
5. rehydrate and continue the same Chat.

Using this same boundary for the external recovery copy has three advantages:

- no connector latency is added during ordinary active work;
- the state being backed up has already been classified and verified;
- the design does not assume that a separate scheduled runtime can read the same Chat-local `/mnt/data`.

## 3. Default trigger contract

| Event | External recovery action |
|---|---|
| ordinary conversation | none |
| Local Root patch during active work | local save only; mark changed state locally |
| `압축해` / `compact` | synchronize configured recovery copy when content changed |
| `백업해` / `backup` | synchronize once without compaction |
| `백업하고 압축해` / `backup and compact` | require verified external recovery copy before compaction |
| scheduled task, idle period, timer, background worker | disabled by default |
| no semantic/hash change | skip external write |

The default synchronization trigger recorded in runtime state is:

```text
EXPLICIT_COMPACT_ONLY
```

## 4. Transaction order

The Local Root and Checkpoint must be safe before any external connector/tool boundary:

```text
Persist durable Local Root state
→ Refresh CHECKPOINT
→ Verify local writes
→ Seal canonical Root digest + Checkpoint hash
→ Export deterministic recovery bundle
→ Synchronize configured external latest copy
→ Verify or record PENDING
→ Compact active context if it has not already compacted
→ Rehydrate minimal state
→ Continue the same Chat
```

An external backup tool call may itself become the host sampling boundary where compaction occurs. When that compaction is confirmed, it counts as the transaction's compaction event. Rehydrate and finish the transaction; do not fire a second compaction trigger.

## 5. Recovery bundle and hash gate

Recommended external layout:

```text
Root Engineering Backups/
└── <PROJECT_ID>/
    ├── latest/
    │   ├── root-engineering-latest.zip
    │   └── BACKUP_MANIFEST.json
    └── snapshots/
        └── <ISO_DATE>_epoch-<N>_<REASON>.zip
```

The normal compact-time write updates only `latest`. Skip the external write when the deterministic bundle hash matches the last verified recovery copy.

An immutable snapshot is optional and should be created only during the same explicit maintenance window for a release, named milestone, migration, restore boundary, critical authority/schema change, destructive operation, or explicit user request. Do not create a new immutable snapshot for every compaction.

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
  "sync_trigger": "EXPLICIT_COMPACT_ONLY",
  "verification": "PASS"
}
```

Accept a recovery copy as current only after identity, artifact existence, and content/hash evidence are verified through the exposed adapter.

## 7. Failure semantics

Required Local persistence and optional external recovery synchronization are different contracts.

```text
Local Root or CHECKPOINT save/verification failure
→ STOP
→ NO COMPACT
```

For ordinary `압축해`:

```text
optional external recovery sync failure
→ keep verified Local Root authoritative
→ set external_backup_pending = true
→ report the failure
→ compaction may continue
```

For strict `백업하고 압축해`:

```text
Local save and external recovery copy must both verify
→ any required failure = NO COMPACT
```

Do not silently call a pending or unverified upload successful. Do not repeatedly retry the same failed path inside one maintenance operation.

## 8. Authority direction and restore

After a Drive-based Root is migrated into Rebirth, normal operation is one-way:

```text
Local Root → external recovery copy
```

Do not automatically merge external changes back into the Local Root during normal work. Restore is a separate explicit operation that verifies Project ID, Root ID, version/schema compatibility, manifest, content hash, and intended restore scope.

## 9. Runtime state

Recommended fields in `runtime/STATE.json`:

```json
{
  "external_backup_sync_trigger": "EXPLICIT_COMPACT_ONLY",
  "scheduled_backup_sync": false,
  "idle_backup_sync": false,
  "external_backup_pending": false,
  "last_external_backup": null
}
```

These fields describe recovery state and policy; they do not change project truth.

## 10. Complete Chat Runtime relationship

The compact-time policy supports Rebirth's **Complete Chat Runtime** framing:

```text
ordinary ChatGPT Chat
+ Local Root
+ Checkpoint
+ explicit compact-time recovery sync
+ active-context compaction
= one long-lived project Chat without mid-work backup latency
```

“Complete Chat Runtime” is Root Engineering terminology, not an official OpenAI product name or feature claim.

## 11. Acceptance conditions

PASS only when:

1. package and schema versions remain `1.0.0`;
2. default recovery sync trigger is `EXPLICIT_COMPACT_ONLY`;
3. scheduled, idle, timer-based, and background sync are disabled;
4. Local Root and Checkpoint are verified before external synchronization;
5. unchanged recovery content skips the external write;
6. optional sync failure is visible and recorded as pending;
7. strict backup-and-compact failure blocks compaction;
8. a compaction observed during the external tool boundary is reused rather than triggered twice;
9. normal authority direction remains Local → external;
10. ordinary active work carries no routine external-backup latency.
