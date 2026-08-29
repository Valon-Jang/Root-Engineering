# Root Engineering Installation Paths

Choose the path by the state of the ChatGPT Project.

## New installation

Use the [canonical English installer](./ROOT_ENGINEERING_INSTALLER.md). Attach that single file to the first chat of a new ChatGPT Project and say:

> Read the package and install it.

Korean user guidance is available in the separate [Korean installer](./ROOT_ENGINEERING_INSTALLER_KO.md).

## Existing installation

Use the [canonical updater](./ROOT_ENGINEERING_UPDATER.md). It reads the installed version and follows the exact versioned path in the [patch registry](./patches/README.md).

Korean user guidance is available in the separate [Korean updater](./ROOT_ENGINEERING_UPDATER_KO.md). Both updaters use the same canonical English patch files.

Do not run a fresh installation to apply an ordinary update. Do not choose a patch by filename alone: the updater must first verify the installed version in both Manifests.

## Package layout

```text
installer/
├── README.md
├── ROOT_ENGINEERING_INSTALLER.md
├── ROOT_ENGINEERING_INSTALLER_KO.md
├── ROOT_ENGINEERING_UPDATER.md
├── ROOT_ENGINEERING_UPDATER_KO.md
└── patches/
    ├── README.md
    ├── v0.1.1-to-v0.1.2.md
    ├── v0.1.2-to-v0.1.3.md
    ├── v0.1.3-to-v0.1.4.md
    └── v0.1.4-to-v0.1.5.md
```
