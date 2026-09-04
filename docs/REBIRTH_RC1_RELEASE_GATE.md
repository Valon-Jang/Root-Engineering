# Root Engineering 1.0 — Rebirth RC.1 release gate

The release candidate may be promoted to `1.0.0` only after all of the following pass.

## Package integrity

- version consistency across installer, Skill, Protocol, templates, runtime helper;
- exact no-op payload (`pass\n`);
- no project-specific facts or identifiers;
- no assumption that a private compaction RPC exists;
- standard-library-only runtime helper;
- tests and package validator pass.

## Fresh install

- writable local preflight;
- full topology creation;
- identity consistency;
- atomic write/readback;
- ACTIVE only after verification.

## Rebirth transaction

- durable-state promotion to correct owners;
- CHECKPOINT contains exact next action;
- save/verify failure blocks compaction;
- pending transaction is sealed before compact;
- epoch advances only after observed compaction;
- rehydration resumes without user reconstruction.

## Repeated compaction

Run at least ten cycles in one long-lived ordinary ChatGPT thread.

Record per cycle:

- same chat/thread retained;
- transcript visibility behavior;
- context epoch and compaction count;
- checkpoint recovery accuracy;
- durable decision retention;
- operational failure guard retention;
- latency/quality observations;
- any summary drift or lost constraint.

## Runtime loss and recovery

- export snapshot;
- simulate local runtime loss in an isolated test;
- restore without overwriting a newer Root;
- verify identity and digest;
- resume from CHECKPOINT.

## Migration

- migrate one verified 0.x project without modifying the old Root;
- preserve source provenance;
- separate durable knowledge from active checkpoint state;
- verify semantic completeness.

## Promotion rule

Do not replace the stable 0.x installer or merge the RC branch until the evidence above is recorded and reviewed.
