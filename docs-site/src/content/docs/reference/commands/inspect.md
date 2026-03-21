---
title: inspect
description: View detailed metadata of a backup on S3 without downloading it.
---

The `inspect` command allows you to look "inside" a backup to see its contents, creator, and system info.

## Usage

```bash
workstate inspect [ID_OR_NAME] [OPTIONS]
```

## Options

- `--files`: List only the file tree contained in the backup.
- `--meta`: Show only system metadata (author, version, date).

## Examples

```bash
# Full inspection
workstate inspect e4f1

# List files only
workstate inspect e4f1 --files
```
