---
package_id: root-engineering-rebirth
package_version: 1.0.0-rc.1
codename: Rebirth
status: release-candidate
target_environment: ordinary ChatGPT chat with writable /mnt/data and Python execution
primary_storage: chat-local-filesystem
project_required: false
google_drive_required: false
context_compaction: host-owned-observed-transaction
---

# Root Engineering 1.0 — Rebirth Installer RC.1

> **Model is replaceable. Context is replaceable. Root persists. The thread continues.**

This package installs a deterministic local Root runtime for one long-lived ordinary ChatGPT conversation. It does not implement or impersonate ChatGPT's private compaction service. It saves and verifies project state around a host-owned compaction event.

## Installation agent contract

When this installer and `ROOT_ENGINEERING_REBIRTH_INSTALLER.py` are available in the current chat, do not merely explain them. Perform every supported step.

```bash
python /mnt/data/ROOT_ENGINEERING_REBIRTH_INSTALLER.py self-test
python /mnt/data/ROOT_ENGINEERING_REBIRTH_INSTALLER.py \
  --root /mnt/data/root-engineering \
  install --project-name "<PROJECT_NAME>"
python /mnt/data/ROOT_ENGINEERING_REBIRTH_INSTALLER.py \
  --root /mnt/data/root-engineering verify
```

Declare the installation ACTIVE only when self-test, preflight, creation, identity checks, digest generation, and readback all pass.

## Installed topology

```text
/mnt/data/root-engineering/
├── BOOT.md
├── PROTOCOL.md
├── ROOT.md
├── MANIFEST.json
├── knowledge/
│   ├── FOUNDATION.md
│   ├── CURRENT.md
│   ├── LEARNED.md
│   ├── OPERATIONAL.md
│   └── HISTORY.md
├── runtime/
│   ├── CHECKPOINT.md
│   ├── STATE.json
│   └── CAPABILITIES.json
├── sources/INDEX.md
├── tools/
│   ├── rebirth_runtime.py
│   └── noop_boundary.py
└── scratch/
```

## `압축해` / Rebirth transaction

This command means:

```text
Persist → Checkpoint → Verify → Compact → Rehydrate
```

Visible progress:

```text
현재 작업을 저장 중입니다…
저장 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행할게.
```

Required order:

1. Read `PROTOCOL.md`, `ROOT.md`, `runtime/CHECKPOINT.md`, and only the canonical owners affected by new durable state.
2. Route durable facts, decisions, verified methods, operational failures/hot paths, and history to their smallest correct owners. Do not dump the transcript.
3. Write the resumable checkpoint with the exact next action:

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering checkpoint \
  --goal "<CURRENT_GOAL>" \
  --active-work "<ACTIVE_WORK>" \
  --completed "<COMPLETED>" \
  --promoted "<DURABLE_STATE_PROMOTED>" \
  --unresolved "<IMPORTANT_UNRESOLVED>" \
  --next-action "<EXACT_NEXT_ACTION>" \
  --resume "Read BOOT, ROOT, and CHECKPOINT; load only owners needed for the exact next action."
```

4. Seal the transaction:

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering prepare-compact --reason user-requested
```

5. If any save or verification fails, stop. **Save failure = no compact.**
6. Prefer a native compact action only when the host explicitly exposes it. Otherwise use exactly one zero-output tool boundary only when that behavior was previously verified under matching conditions and success can be observed. Never invent a private RPC or default to pressure flooding.
7. After observed success:

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering complete-compact \
  --observed \
  --method zero-output-boundary \
  --signal CONTEXT_REPLACEMENT_OBSERVED
```

8. If success cannot be established:

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering abort-compact \
  --reason "compaction not observed"
```

9. Read `BOOT.md`, `ROOT.md`, `runtime/CHECKPOINT.md`, and only needed owners. Continue the exact next action in the same chat.

The completion command refuses to advance the context epoch if the sealed canonical digest or checkpoint hash changed after preparation.

## Backup

`/mnt/data` lifetime is controlled by the host. At important milestones:

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering export
```

Google Drive and GitHub are optional backup/recovery adapters, not routine dependencies.

## RC boundary

This is `1.0.0-rc.1`, not the final stable release. Promotion to `1.0.0` requires live repeated-compaction, recovery, and migration evidence. Do not replace the stable 0.x installer before the release gate passes.
