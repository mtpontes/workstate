---
title: list
description: List available backups for the current project on S3.
---

The `list` command displays all states you have previously saved to the cloud.

## Usage

```bash
workstate list [OPTIONS]
```

## Information Displayed

- **ID**: Short hash of the backup (e.g., `e4f1`).
- **Name**: The name you gave during `save`.
- **Date**: When the state was captured.
- **Status**: Icons indicating if it's encrypted (🔒) or protected (🔰).

## Options

- `--limit N`: Show only the last N backups.
- `--all-projects`: List backups from all projects in the bucket.

## Examples

```bash
workstate list --limit 5
```
