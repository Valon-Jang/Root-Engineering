---
registry_id: root-engineering-patch-registry
target_package: root-engineering-chat-installer
latest_version: 0.1.5
schema_version: 0.1.0
direction: forward-only
---

# Root Engineering Patch Registry

This is the canonical ordered registry for updating an existing Root Engineering installation. Read it through [ROOT_ENGINEERING_UPDATER.md](../ROOT_ENGINEERING_UPDATER.md).

| From | To | Patch | Direct instructions |
|---|---|---|---|
| 0.1.1 | 0.1.2 | [v0.1.1-to-v0.1.2.md](./v0.1.1-to-v0.1.2.md) | [raw](https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/patches/v0.1.1-to-v0.1.2.md) |
| 0.1.2 | 0.1.3 | [v0.1.2-to-v0.1.3.md](./v0.1.2-to-v0.1.3.md) | [raw](https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/patches/v0.1.2-to-v0.1.3.md) |
| 0.1.3 | 0.1.4 | [v0.1.3-to-v0.1.4.md](./v0.1.3-to-v0.1.4.md) | [raw](https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/patches/v0.1.3-to-v0.1.4.md) |
| 0.1.4 | 0.1.5 | [v0.1.4-to-v0.1.5.md](./v0.1.4-to-v0.1.5.md) | [raw](https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/patches/v0.1.4-to-v0.1.5.md) |

## Resolution rules

1. Begin only at the Package Version verified in both Manifests.
2. Select the row whose `From` value exactly equals that version.
3. Apply and verify that one patch.
4. Update both Manifest versions only after verification passes.
5. Repeat until both Manifests equal `latest_version`.

The table order is authoritative. Transitions are contiguous and forward-only. Do not skip, combine, infer, or reorder patches. A version older than `0.1.1`, newer than `0.1.5`, absent from the table, or inconsistent across Manifests has no valid path in this registry and must stop without mutation.
