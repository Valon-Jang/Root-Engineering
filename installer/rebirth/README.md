# Root Engineering 1.0 — Rebirth RC.1

> **Context can die. The project can resume. The same thread continues.**

This release candidate moves the Root Engineering runtime into an ordinary ChatGPT chat-local workspace and separates:

```text
human-visible transcript
compactable active model context
local canonical Root
transient resume Checkpoint
```

## Entry points

- [Executable single-file installer](../ROOT_ENGINEERING_REBIRTH_INSTALLER.py)
- [English installer contract](../ROOT_ENGINEERING_REBIRTH_INSTALLER.md)
- [Korean installer contract](../ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md)
- [Agent Skill](./root-engineering/SKILL.md)
- [Architecture](../../docs/ROOT_ENGINEERING_REBIRTH.md)
- [RC.1 release gate](../../docs/REBIRTH_RC1_RELEASE_GATE.md)

## Core transaction

```text
Persist durable state
→ Write exact resume Checkpoint
→ Verify and seal hashes
→ Compact through an exposed native action or previously verified minimal boundary
→ Advance epoch only after observed success
→ Rehydrate from BOOT + ROOT + CHECKPOINT
→ Continue the same Chat
```

The executable is standard-library-only and includes `self-test`, local preflight, installation, verification, checkpoint creation, sealed compaction state, abort, completion, status, and ZIP export commands.

This branch is an RC. The stable 0.x installer remains untouched until repeated live compaction, recovery, and migration gates pass.
