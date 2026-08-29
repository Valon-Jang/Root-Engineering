---
package_id: root-engineering-chat-updater
target_package: root-engineering-chat-installer
target_version: 0.1.5
schema_version: 0.1.0
release_date: 2026-08-29
primary_entry_phrase: "Read the updater and update the existing installation."
direction: forward-only
patch_registry_url: https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/patches/README.md
fresh_installer_url: https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/ROOT_ENGINEERING_INSTALLER.md
---

# ROOT ENGINEERING — EXISTING INSTALLATION UPDATER v0.1.5

> **This file updates an existing installation. It does not perform a fresh installation.**
>
> Korean user guidance: [ROOT_ENGINEERING_UPDATER_KO.md](./ROOT_ENGINEERING_UPDATER_KO.md)

## Execution contract

The agent reading this file must execute the update when connected tools permit it, not merely explain the steps.

1. Locate the existing Project Binding, Global Manifest, and Project Manifest.
2. Read the Package ID, Package Version, Schema Version, document IDs, and installation status from both Manifests.
3. Require the Package ID to be `root-engineering-chat-installer`, both Package Versions to match, and the installation to identify one unambiguous project.
4. Read the canonical [patch registry](./patches/README.md), using its raw URL from this file when necessary.
5. Starting at the verified installed version, resolve the contiguous forward-only chain to `0.1.5`.
6. Read each named patch file in full immediately before applying it.
7. Require the patch `from_version` to equal the currently verified version.
8. Apply only that patch's declared operations and preserve everything in `must_not_touch`.
9. Run that patch's verification. Only after it passes, update the Package Version in both Manifests to the patch `to_version`.
10. Re-read the changed scopes and both Manifest versions, then continue with the next patch.
11. Finish only when both Manifests report `0.1.5` and the final acceptance checks pass.

## Routing and stop conditions

```text
No existing Binding or Manifest
→ STOP: this updater cannot prove an existing installation

Both Manifests already report 0.1.5
→ run final verification only; make no update writes

Both Manifests report an older listed version
→ follow the exact registry chain, one patch at a time

Manifest versions disagree
→ STOP: report both values; do not choose one

Installed version is newer than 0.1.5
→ STOP: do not downgrade

Starting version or next transition is absent from the registry
→ STOP: report "Missing patch: <from> → <to>"; do not improvise
```

Do not run INSTALL, create a replacement folder, regenerate project documents, change document IDs, merge patch steps, or use memory of a prior release as patch instructions. Never permanently attach the updater, registry, or patch files as Project Sources.

If connected web access is unavailable, ask the user to attach this updater, `patches/README.md`, and only the exact patch files named by the resolved chain. Do not search unrelated Drive content for a substitute.

## Final verification

- Global and Project Manifest Package Versions both equal `0.1.5`.
- Schema Version remains `0.1.0` unless an exact patch says otherwise.
- Existing document and folder IDs are unchanged.
- Existing Foundation, Current Knowledge, Learned Knowledge, History, Sources, and Skills content is preserved.
- Fresh-chat retrieval still reaches the same Project Binding and project records.

Report only the verified start version, applied patch filenames, final version, and PASS/FAIL result.
