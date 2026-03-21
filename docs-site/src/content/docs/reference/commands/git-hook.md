---
title: git-hook
description: Install or remove native Git integration hooks.
---

The `git-hook` command extends Workstate's power into your Git workflow.

## Usage

```bash
workstate git-hook [COMMAND]
```

## Sub-commands

### `install`
Installs `post-checkout` and `pre-push` hooks in `.git/hooks/`.
- **post-checkout**: Triggers on branch change, suggesting a `sync`.
- **pre-push**: Triggers on push, suggesting a `save`.

### `uninstall`
Removes the hooks installed by Workstate.

## Examples

```bash
workstate git-hook install
```
