---
title: protect
description: Enable or remove deletion protection for a backup on S3.
---

The `protect` command ensures important backups are not accidentally removed by `delete`.

## Usage

```bash
workstate protect [ID_OR_NAME] [OPTIONS]
```

## Options

- `--remove`: Remove protection from a backup.
- `--all`: Protect all backups in the current project.

## Examples

```bash
# Add protection
workstate protect e4f1

# Remove protection
workstate protect e4f1 --remove
```
