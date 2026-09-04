---
package_id: root-engineering-rebirth-chat-installer
package_version: 1.1.0
codename: Rebirth
release_name: Sidecar Work Graph
schema_version: 1.1.0
release_date: 2026-09-04
status: staged-next-version
base_compatible_version: 1.0.0
primary_environment: existing project workspace with Markdown knowledge files
supported_topologies:
  - isolated-root
  - sidecar-workspace
preferred_existing_workspace_topology: sidecar-workspace
control_plane_path: .root
content_registry_path: .root/runtime/CONTENT_REGISTRY.json
existing_markdown_adoption: byte-exact-register-in-place
existing_markdown_move_during_adoption: forbidden
existing_markdown_rename_during_adoption: forbidden
existing_markdown_rewrite_during_adoption: forbidden
line_ending_normalization_during_adoption: forbidden
encoding_normalization_during_adoption: forbidden
adoption_verification: pre-and-post-sha256
routing_model: root-to-core-to-exact-work-node
specialized_project_content: excluded
---

# ROOT ENGINEERING 1.1.0 — REBIRTH: SIDECAR WORK GRAPH

> **Model is replaceable. Context is replaceable. Existing knowledge is preserved. Root persists.**

This staged next-version installer formalizes a structure proven in long-running project work without importing any project-specific facts, names, procedures, or domain rules.

The central change is simple:

> **Do not rewrite an existing Markdown corpus to make it look like Root Engineering. Add a Root Engineering control plane beside it, register every existing document byte-for-byte, and route to the exact authoritative work node.**

Root Engineering 1.0.0 remains the compatible Kernel baseline. Version 1.1.0 adds the **Sidecar Work Graph** topology and a non-destructive adoption transaction.

---

## 0. Scope

Version 1.1.0 is for a project workspace that already contains useful Markdown files such as:

- a project operating profile;
- a work or context router;
- reusable standards;
- task-specific living context files;
- handoff or resume files;
- references and evidence notes.

It solves three recurring failures:

1. A flat folder forces the model to scan too much or guess which file owns the current truth.
2. Reformatting legacy files during installation can silently change facts, terminology, history, or line endings.
3. A single monolithic `CURRENT.md` becomes too large when many independent workstreams evolve at different speeds.

Version 1.1.0 therefore separates:

```text
CONTROL PLANE
= Root identity, routing, registry, checkpoint, verification

CONTENT PLANE
= the project's existing Markdown files, preserved in place
```

### Explicitly out of scope

- importing any specialized project content into this package;
- changing the meaning or wording of existing Markdown files;
- flattening all work into one generated summary;
- moving, renaming, deleting, or normalizing adopted files during installation;
- treating filenames alone as proof of authority;
- replacing Root Engineering 1.0.0 compaction, backup, or storage safety rules.

---

# PART A. Architecture

## 1. Sidecar Workspace Topology

For a workspace that already contains Markdown knowledge, install the Root control plane in `.root/` and leave the content plane untouched.

```text
<PROJECT_WORKSPACE>/
├── .root/
│   ├── BOOT.md
│   ├── ROOT.md
│   ├── MANIFEST.json
│   ├── knowledge/
│   │   ├── FOUNDATION.md
│   │   ├── CURRENT.md
│   │   ├── LEARNED.md
│   │   ├── OPERATIONAL.md
│   │   └── HISTORY.md
│   └── runtime/
│       ├── CHECKPOINT.md
│       ├── STATE.json
│       ├── CAPABILITIES.json
│       └── CONTENT_REGISTRY.json
│
├── <existing profile Markdown>          ← unchanged
├── <existing routing/core Markdown>     ← unchanged
├── <existing standards Markdown>        ← unchanged
├── <existing work-context Markdown>     ← unchanged
├── <existing handoff Markdown>          ← unchanged
└── <existing references and sources>    ← unchanged
```

The **Canonical Project Boundary** is `<PROJECT_WORKSPACE>`. The `.root/` directory is the Root Engineering control plane inside that boundary. Registered content files remain canonical at their existing paths.

### 1.1 Why a sidecar

A sidecar topology allows Root Engineering to provide:

- exact boot and routing;
- one authoritative owner per fact or decision;
- active-work resume;
- structural verification;
- content hashes and change detection;

without rewriting a mature project's documents.

### 1.2 Isolated Root compatibility

The 1.0.0 isolated topology remains valid:

```text
/mnt/data/root-engineering/
```

Use isolated mode for a new project with no existing corpus. Use sidecar mode when a meaningful project workspace already exists and preservation matters.

---

## 2. Control Plane Responsibilities

### `BOOT.md`

Minimal runtime entry point. It identifies the workspace, Root ID, current checkpoint path, and the exact sequence for project-dependent boot.

### `ROOT.md`

Small identity and routing document. It contains:

- Project ID and Root ID;
- control-plane paths;
- compact digests;
- route to `CURRENT.md`;
- route to `CONTENT_REGISTRY.json`;
- direct-child ownership only.

It must not duplicate detailed work-node content.

### `knowledge/FOUNDATION.md`

Stable project purpose, durable boundaries, and essential Human Intent that belong to Root Engineering itself. Existing project profile files are not copied into it; they are registered as content nodes.

### `knowledge/CURRENT.md`

Current routing digest, active work-node pointer, unresolved cross-work risks, and a compact map to the registered routing core. It is not a replacement for detailed task files.

### `knowledge/LEARNED.md`

Verified reusable methods generalized by Root Engineering. Existing project standards remain registered in place rather than copied.

### `knowledge/OPERATIONAL.md`

Exact repeated-operation keys, verified fast paths, known failure fingerprints, and required evidence.

### `knowledge/HISTORY.md`

Superseded Root-level routing states and topology transitions. It does not absorb the full history already present in adopted files.

### `runtime/CHECKPOINT.md`

Immediate continuation state for one active execution path: goal, completed work, current state, next actions, blockers, and resume instruction.

### `runtime/CONTENT_REGISTRY.json`

The authoritative machine-readable map of preserved content nodes.

---

# PART B. Content Registry and Roles

## 3. Registry Schema

Minimum structure:

```json
{
  "schema_version": "1.1.0",
  "project_id": "REP-...",
  "root_id": "RR-...",
  "workspace": ".",
  "preservation_mode": "BYTE_EXACT_REGISTER_IN_PLACE",
  "generated_at": "2026-09-04T00:00:00Z",
  "nodes": [
    {
      "node_id": "RN-...",
      "relative_path": "WORK_EXAMPLE.md",
      "role": "WORK_CONTEXT",
      "authority": "CANONICAL_CONTENT_OWNER",
      "status": "ACTIVE",
      "sha256": "...",
      "size_bytes": 12345,
      "parent_route": "ROUTING_CORE",
      "direct_children": []
    }
  ]
}
```

The registry stores metadata and hashes, not copied document text.

## 4. Generic Node Roles

The installer may classify by strong structural evidence. Filename heuristics are hints, not unquestionable truth.

### `OPERATING_PROFILE`

Defines **how to judge, review, prioritize, or report**. It is behavioral policy, not project fact.

Typical filename hints:

```text
*PROFILE*.md
*OPERATING*.md
```

### `ROUTING_CORE`

Defines **which work context to use**, the registered work map, and routing boundaries.

Typical hints:

```text
*WORK_CORE*.md
*ROUTER*.md
*CORE*.md when routing semantics are explicit
```

### `EXECUTION_STANDARD`

Defines **how a recurring class of work is performed**.

Typical hints:

```text
*STANDARD*.md
*PROTOCOL*.md
*GUIDE*.md
```

### `WORK_CONTEXT`

Owns the actual long-running state of one workstream: facts, judgments, completed actions, pending responses, schedule, next actions, gates, and resume point.

Typical hint:

```text
WORK_*.md
```

### `HANDOFF`

Temporary or transitional continuation material whose purpose is to bridge a stage, chat, owner, or implementation boundary.

Typical hints:

```text
*HANDOFF*.md
*CHAT_SUMMARY*.md
*STAGE_PLAN*.md when it is a transition plan rather than the authoritative work owner
```

### `REFERENCE`

Evidence, background, data notes, reports, or supporting material that does not own current project decisions.

### `UNCLASSIFIED`

Use when evidence is insufficient. Preservation is more important than forced classification.

## 5. Authority Separation

Never confuse these roles:

```text
OPERATING_PROFILE
= how to judge

ROUTING_CORE
= which context to load

EXECUTION_STANDARD
= how to perform a recurring method

WORK_CONTEXT
= what actually happened and what is currently true

REFERENCE
= supporting evidence
```

A profile cannot create project facts. A standard cannot silently override a task-specific decision. A router cannot become the detailed owner of every workstream.

---

# PART C. Non-Destructive Adoption Transaction

## 6. Hard Preservation Contract

During adoption, every pre-existing Markdown file is protected.

The installer must not:

- rewrite content;
- prepend metadata;
- append routing blocks;
- normalize headings;
- normalize whitespace;
- normalize line endings;
- change encoding;
- rename the file;
- move the file;
- delete the file;
- replace it with a generated version.

The only allowed writes are new or previously Root-owned files under `.root/`.

## 7. Adoption Sequence

```text
1. Resolve the exact project workspace.
2. Verify the workspace is writable.
3. Detect an existing valid `.root/` before creating anything.
4. Inventory every pre-existing Markdown file outside `.root/`.
5. Record relative path, byte size, and SHA-256.
6. Classify each file by role using conservative evidence.
7. Generate the candidate `.root/` control plane in a temporary sibling path.
8. Write ROOT, routing digest, checkpoint, manifest, state, capabilities, and registry.
9. Read back and validate every generated control-plane file.
10. Re-hash every inventoried Markdown file.
11. If any path, size, or hash changed, delete only the candidate control plane and FAIL CLOSED.
12. Atomically activate the candidate `.root/` when possible.
13. Re-read the active registry and sample exact registered paths.
14. Report the preserved-file count and unchanged-hash result.
```

### 7.1 Existing `.root/`

If a valid Root already exists:

- do not create a second Root;
- compare schema and topology;
- enter VERIFY or UPGRADE;
- preserve all registered content files;
- patch only Root-owned control-plane files required by the version delta.

If `.root/` exists but identity cannot be proven, stop and surface the conflict. Do not overwrite it based on directory name alone.

### 7.2 Failure behavior

> **Any protected Markdown mismatch = adoption failure.**

Do not continue with partial activation. Do not “repair” the changed source by guessing its original content. Keep the prior workspace authoritative and report the exact changed path.

---

# PART D. Boot and Routing

## 8. Project-Dependent Boot

For a self-contained request, use the ordinary Fast Path and do not boot the Root.

For a request that depends on project state:

```text
read .root/BOOT.md
→ read .root/ROOT.md
→ read .root/knowledge/CURRENT.md
→ read the registered ROUTING_CORE when routing is needed
→ resolve the exact WORK_CONTEXT
→ read only the profile, standard, handoff, or reference needed for this task
```

Do not scan every work file.

## 9. Routing Priority

When content conflicts, use this generic priority:

```text
1. Current explicit user instruction
2. Exact authoritative WORK_CONTEXT or other registered content owner
3. Applicable OPERATING_PROFILE or EXECUTION_STANDARD for method
4. Root-level digest and routing metadata
5. General practice or model inference
```

A current user correction changes the meaning of prior stored state immediately. Persist it only through the exact content owner and normal Save Gate.

## 10. Work Identification

The router first determines the current workstream.

### Existing workstream

Read the exact registered `WORK_CONTEXT` and extract only what is needed:

- current state;
- confirmed facts;
- prior decisions;
- completed actions;
- responses/results pending;
- schedule;
- next actions;
- gates;
- resume point.

### New workstream

Do not create a new work node for every conversation. Create one when loss of continuity would materially increase risk, such as when:

- work spans multiple days;
- multiple people, teams, or vendors are involved;
- dates, approvals, tests, or gates exist;
- facts and decisions will accumulate;
- another chat or owner must continue later.

New work nodes may use the recommended structure below. Adopted nodes are never rewritten merely to match it.

## 11. Recommended New Work-Node Structure

```text
# WORK_<NAME>

## 0. Use Rules and Boundary
## 1. Purpose / Problem
## 2. Confirmed Facts
## 3. Current Judgment and Evidence
## 4. Completed Actions
## 5. Pending Responses / Results
## 6. Schedule
## 7. Risks
## 8. Next Actions
## 9. Gates / Completion Conditions
## 10. Resume Point
```

This is a creation template, not a migration requirement.

---

# PART E. Write and Update Rules

## 12. Single-Owner Write Rule

Detailed current truth has one authoritative owner.

- update the exact work node that owns the fact;
- update a routing core only when routing or registered-work metadata changed;
- update an operating profile only when judgment policy changed;
- update a standard only when the reusable method changed;
- update ROOT only when identity, topology, or direct routing changed;
- never copy the same detailed update into multiple nodes for convenience.

## 13. Protected Existing Content After Adoption

The byte-exact guarantee applies to the adoption transaction.

After activation, a user may intentionally continue editing living work files. Such a write is allowed only when:

1. the exact authoritative owner is resolved;
2. the semantic delta is explicit;
3. unrelated content is preserved;
4. the write is verified;
5. the registry hash and size are updated in the same successful transaction;
6. failure leaves the previous canonical file and registry intact.

Structural upgrades alone must not edit content-plane Markdown.

## 14. Current-State and History Rule

Prefer making the latest valid state clear in the authoritative work node. Preserve superseded state when transition rationale, rollback value, or failure-prevention value remains useful.

Do not create a second “latest summary” that competes with the work owner.

## 15. Checkpoint Rule

`CHECKPOINT.md` points to one current execution path and contains only enough state to resume immediately. It does not replace the work node.

Recommended checkpoint:

```text
# ACTIVE CHECKPOINT

## Current Goal
## Active Work Node
## Completed
## Current State
## Next
## Pending / Risks
## Resume Instruction
```

---

# PART F. Upgrade from Rebirth 1.0.0

## 16. Upgrade Modes

### Mode A — Existing isolated 1.0.0 Root

Keep the existing isolated topology unless the user explicitly asks to bind an external project workspace. Add the 1.1 registry and role semantics inside the existing Root. Do not move existing knowledge files.

### Mode B — Existing project workspace with Markdown corpus

Create `.root/` as a sidecar, register content in place, and activate only after pre/post hash verification.

### Mode C — Existing project already has its own router/core/work structure

Treat that structure as content-plane knowledge. Do not translate its names or rewrite its documents. Register the existing router as `ROUTING_CORE`, task files as `WORK_CONTEXT`, profiles as `OPERATING_PROFILE`, and reusable procedures as `EXECUTION_STANDARD` when evidence supports those roles.

### Mode D — Ambiguous mixed workspace

Register uncertain files as `UNCLASSIFIED`; do not force them into a role. The user or later verified evidence may reclassify metadata without changing file content.

## 17. Upgrade Write Scope

Allowed:

- create or patch `.root/` control-plane files;
- add registry metadata;
- change a node's registry role after verified evidence;
- update Root routing and checkpoint pointers.

Forbidden during structural upgrade:

- editing adopted Markdown;
- “cleaning up” old headings;
- merging two existing files automatically;
- deleting duplicates automatically;
- changing project terminology;
- importing specialized content into global Root Engineering policy.

---

# PART G. Verification and Completion

## 18. Acceptance Test

A v1.1.0 sidecar installation is complete only when all are true:

1. `.root/` identity is valid.
2. Every protected Markdown file has the same path, size, and SHA-256 before and after adoption.
3. `CONTENT_REGISTRY.json` resolves every registered path.
4. Exactly one Root is ACTIVE for the workspace.
5. A project-dependent query can route:
   - Root → Current → Routing Core → exact Work Context.
6. The same query does not require reading unrelated work files.
7. An applicable profile or standard is loaded as method, not mistaken for project fact.
8. `CHECKPOINT.md` can resume one active workstream without reconstructing the entire conversation.
9. No project-specific content exists in the installer package itself.

## 19. Completion Report

Report only:

```text
Mode: SIDECAR_WORKSPACE or ISOLATED_ROOT
Root: <verified path>
Protected Markdown files: <count>
Preservation check: <count>/<count> path-size-hash unchanged
Registered roles: <compact counts>
Active work node: <path or NONE>
Acceptance routing: PASS / FAIL
Unclassified files: <count>
```

Do not dump internal IDs unless they help diagnosis.

## 20. Reference Implementation

This repository includes:

```text
tools/root_sidecar_adopt.py
```

It is a conservative reference implementation for inventory, role classification, control-plane creation, and pre/post SHA-256 verification. It does not modify, move, rename, or delete existing Markdown files.

The tool is not a substitute for the Root Engineering authority and Save Gate. It demonstrates the structural transaction.

---

# PART H. Invariants

## 21. Non-Negotiable Invariants

> **Existing knowledge is adopted, not rewritten.**

> **Routing metadata may change; protected content bytes do not change during adoption.**

> **The router decides where to read. It does not become the owner of every fact.**

> **A profile explains how to judge. A work node records what happened. A standard explains how to execute.**

> **One current truth has one authoritative owner.**

> **Current explicit user instruction remains the highest project-level authority.**

> **Any preservation mismatch fails closed before activation.**

---

## 22. Version Position

Root Engineering 1.1.0 is an additive structural evolution of Rebirth 1.0.0.

It preserves the 1.0 Kernel and adds:

- sidecar installation for existing workspaces;
- byte-exact legacy Markdown adoption;
- role-aware content registry;
- Root → Core → exact Work Context routing;
- explicit separation of profile, routing, standard, work, handoff, and reference roles;
- hash-gated structural activation.

The existing 1.0.0 installer and all prior Markdown files remain unchanged until this staged version is explicitly promoted.
