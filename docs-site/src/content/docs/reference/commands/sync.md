---
title: sync
description: Automatically synchronize with the latest backup on S3.
---

The `sync` command is the "automation" version of download. It's designed for scripts and hands-free operations.

## Usage

```bash
workstate sync [OPTIONS]
```

## How it works

1. It checks the latest backup available on S3 for the current project.
2. If the local state is different, it updates files automatically.
3. If the backup is encrypted, it will look for the password in the `WORKSTATE_PASSWORD` environment variable or prompt the user.

## Examples

```bash
# Basic sync
workstate sync

# Force sync without asking
workstate sync --force
```

:::tip[Tip]
Use `sync` in your development shell's startup to ensure your environment is always up-to-date.
:::
