# Root Engineering 1.0 — Rebirth Runtime

> **Model is replaceable. Context is replaceable. Root persists. The thread continues.**

This folder turns the canonical Rebirth method into an executable state/compaction transaction for one long-lived ordinary ChatGPT conversation.

## Canonical package composition

The files are fused by responsibility rather than copied into competing documents.

- `../ROOT_ENGINEERING_REBIRTH_INSTALLER.md` — canonical English installation/runtime contract
- `../ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md` — Korean semantic mirror
- `../../docs/ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION.md` — normative authority and fusion contract
- `../../docs/ROOT_ENGINEERING_1.0_PERSISTENT_THREAD_FUSION_KO.md` — Korean semantic mirror
- `../../docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md` — delegated external-backup policy
- `../../docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY_KO.md` — Korean semantic mirror
- `root-engineering/SKILL.md` — single operational owner for `압축해`
- `runtime/rebirth_transaction.py` — deterministic Checkpoint, sealing, epoch, abort, and export guard
- `../../tools/validate_rebirth_runtime.py` — runtime validator/self-test launcher
- `../../tools/validate_rebirth_md_fusion.py` — cross-document authority and semantic-fusion validator

The independent `Valon-Jang/persistent-project-thread` repository is research/evidence provenance. Do not install its Skill beside `root-engineering-rebirth` in the same trigger scope; verified behavior is already fused into the Rebirth Skill.

## State model

```text
Chat Transcript            → human-visible history
Active Model Context       → compactable working memory
Local ROOT                 → durable canonical project truth
CHECKPOINT                 → immediate resume bridge
Local Capability Workspace → Skills, hot paths, helpers, manifests, runtime assets
```

Capability assets do not become a second Root. Their verified procedures belong in `knowledge/OPERATIONAL.md`; path/hash/scope/availability belong in `runtime/CAPABILITIES.json`.

## What the runtime guard does

```text
write exact CHECKPOINT
→ verify Root identity and canonical owners
→ seal canonical digest + Checkpoint hash
→ wait for host/native or verified boundary compaction
→ reject completion if sealed state changed
→ advance context epoch only after observed success
→ export recovery bundles when requested
```

It does **not**:

- implement ChatGPT's private compaction service;
- invent an internal RPC;
- upload to Google Drive by itself;
- prove that a policy-declared external adapter is actually available;
- claim that `/mnt/data` survives every product/runtime lifecycle.

## `압축해` fused transaction

```text
Resolve Local Root
→ inspect the Root filesystem
→ persist smallest canonical owners
→ refresh CHECKPOINT
→ verify + seal
→ if a configured adapter exists and hash changed, update verified external `latest`
→ compact through the capability ladder
→ verify compaction
→ advance context epoch
→ rehydrate minimally
→ continue the same Chat
```

Required local save or Storage Gate failure means **no compact**.

For ordinary `압축해`, optional external-backup failure marks `external_backup_pending = true` and may continue because the verified Local Root remains authoritative.

For `백업하고 압축해`, external backup is strict; missing adapter, ambiguous target, upload failure, or failed remote verification means **no compact**.

Google Drive synchronization is real only when a Drive connector/tool is available, the backup target is bound, upload is executed, and the remote artifact/manifest is verified.

## Validate the package

From a repository checkout:

```bash
python tools/validate_rebirth_installer.py
python tools/validate_rebirth_backup_policy.py
python tools/validate_rebirth_md_fusion.py
python tools/rebirth_local_selftest.py
python tools/validate_rebirth_runtime.py
```

## Install the runtime guard

After the canonical installer creates and verifies the Local Root, copy:

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

## Storage and authority boundary

The Local Root is primary for the current Runtime. Google Drive, GitHub, and exported ZIPs are optional backup/recovery adapters. Normal authority is one-way:

```text
Local Root → external latest/snapshot
```

No automatic external-to-Local merge occurs. Restore is explicit and identity/hash verified.
