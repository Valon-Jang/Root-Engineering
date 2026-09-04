# Root Engineering 1.0 — Rebirth Runtime

> **Model is replaceable. Context is replaceable. Root persists. The thread continues.**

This folder turns the canonical Rebirth method into an executable compaction transaction for one long-lived ordinary ChatGPT conversation.

## Components

- `../ROOT_ENGINEERING_REBIRTH_INSTALLER.md` — canonical English installation and architecture contract;
- `../ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md` — Korean installation contract;
- `root-engineering/SKILL.md` — agent operating procedure;
- `runtime/rebirth_transaction.py` — deterministic Checkpoint, sealing, backup-record, epoch, abort, and export guard;
- `../../tools/validate_rebirth_runtime.py` — package validator and self-test launcher.

## What the runtime does

```text
write exact CHECKPOINT
→ verify Root identity and canonical owners
→ seal canonical digest + Checkpoint hash
→ export/synchronize recovery state during explicit compact maintenance if configured
→ record VERIFIED / PENDING / SKIPPED backup outcome
→ wait for host/native or verified boundary compaction
→ reject completion if sealed canonical state changed
→ advance context epoch only after observed success
```

It does **not** implement ChatGPT's private compaction service, invent an internal RPC, upload to Google Drive without an exposed connector, or claim that `/mnt/data` survives every product/runtime lifecycle.

## Validate the package

From a repository checkout:

```bash
python tools/validate_rebirth_installer.py
python tools/rebirth_local_selftest.py
python tools/validate_rebirth_runtime.py
```

Expected final validator output:

```text
REBIRTH_RUNTIME_VALIDATION_PASS
runtime_bytes=<size>
self_tests=10
```

## Install the runtime guard

After the canonical Rebirth installer creates and verifies `/mnt/data/root-engineering`, copy:

```text
installer/rebirth/runtime/rebirth_transaction.py
```

to:

```text
/mnt/data/root-engineering/tools/rebirth_transaction.py
```

Then run:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py self-test
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering verify
```

## `압축해`

The Skill defines the user command as:

```text
Persist → Checkpoint → Verify → Backup if configured → Compact → Rehydrate
```

The transaction must be prepared before any external/tool boundary. Completion requires explicit observed compaction evidence, and any canonical or Checkpoint change after preparation fails closed. Save or verification failure means no compaction.

A configured recovery adapter is synchronized only inside this explicit maintenance window. Scheduled, idle, timer-based, and background synchronization are disabled by default. This keeps backup latency out of active work and avoids assuming another runtime can read the same `/mnt/data`.

Use `record-backup` to persist the outcome:

```bash
python /mnt/data/root-engineering/tools/rebirth_transaction.py \
  --root /mnt/data/root-engineering record-backup \
  --status VERIFIED \
  --adapter google-drive \
  --artifact-sha256 <SHA256> \
  --remote-reference <VERIFIED_ID_OR_URL>
```

Optional backup failure is recorded as `PENDING` and reported. The Local Root remains canonical unless the user explicitly requires a verified external backup before compaction.

## Storage boundary

The local Root is primary for the current persistent thread. Google Drive, GitHub, and exported ZIPs are optional backup/recovery adapters. They are not routine dependencies of the Rebirth runtime.
