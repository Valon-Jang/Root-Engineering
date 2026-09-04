# Root Engineering 1.0 — Rebirth Runtime

> **Model is replaceable. Context is replaceable. Root persists. The thread continues.**

This folder turns the canonical Rebirth method into an executable compaction transaction for one long-lived ordinary ChatGPT conversation.

## Components

- `../ROOT_ENGINEERING_REBIRTH_INSTALLER.md` — canonical English installation and architecture contract;
- `../ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md` — Korean installation contract;
- `root-engineering/SKILL.md` — agent operating procedure;
- `runtime/rebirth_transaction.py` — deterministic Checkpoint, sealing, epoch, abort, and export guard;
- `../../tools/validate_rebirth_runtime.py` — package validator and self-test launcher.

## What the runtime does

```text
write exact CHECKPOINT
→ verify Root identity and canonical owners
→ seal canonical digest + Checkpoint hash
→ wait for host/native or verified boundary compaction
→ reject completion if sealed state changed
→ advance context epoch only after observed success
→ export recovery snapshots when requested
```

It does **not** implement ChatGPT's private compaction service, invent an internal RPC, or claim that `/mnt/data` survives every product/runtime lifecycle.

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
self_tests=7
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
Persist → Checkpoint → Verify → Compact → Rehydrate
```

The transaction must be prepared before compaction. Completion requires explicit observed evidence, and any canonical or Checkpoint change after preparation fails closed. Save or verification failure means no compaction.

## Storage boundary

The local Root is primary for the current persistent thread. Google Drive, GitHub, and exported ZIPs are optional backup/recovery adapters. They are not routine dependencies of the Rebirth runtime.
