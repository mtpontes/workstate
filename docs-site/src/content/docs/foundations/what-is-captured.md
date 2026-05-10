---
title: What is Captured
description: Understand how Workstate uses an explicit inclusion system (whitelist) to manage your environment state.
---

Workstate follows a **strict inclusion model** (whitelist). Instead of trying to guess what to exclude, it only captures what you explicitly tell it to. This approach ensures your backups are lean, secure, and predictable.

## The `.workstateinclude` File

The core of Workstate's selection engine is the `.workstateinclude` file. It works similarly to a `.gitignore`, but in reverse: **only the paths and patterns listed here will be captured.**

### Default Inclusions
When you run `workstate init`, a minimalist `.workstateinclude` is created with sensible defaults:

- `.workstateinclude` (it always tracks its own config)
- `src/` (core source code)
- `pyproject.toml` / `package.json` (dependency definitions)
- `README.md`

### Why Whitelisting?
1. **Security**: You never accidentally backup sensitive logs or binaries that weren't meant to be shared.
2. **Performance**: Smaller snapshots mean faster uploads and downloads.
3. **Control**: You know exactly what constitutes your "work state".

## Critical Files Auto-Inclusion

Even if not explicitly listed, Workstate ensures the following are always handled correctly:
- **Config**: The `.workstateinclude` file itself is always included.
- **Metadata**: Internal metadata used for restoration is automatically managed.

## Legacy Support (Blacklist)

If you have an existing project using `.workstateignore`, Workstate will still respect it as a fallback. However, **new projects always use `.workstateinclude`**, and we strongly recommend migrating legacy projects to the inclusion model.

:::caution[Heads Up]
If both files exist, `.workstateinclude` takes precedence and the ignore file will be bypassed.
:::
