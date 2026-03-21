---
title: delete
description: Permanently remove backups from your S3 bucket.
---

The `delete` command helps you keep your bucket clean by removing old or unnecessary states.

## Usage

```bash
workstate delete [ID_OR_NAME] [OPTIONS]
```

## Safety Rules

- **Protected Backups**: Workstate will block the deletion of any backup marked as protected (🔒). Remove protection first with `protect --remove`.
- **Confirmation**: By default, the command asks for manual confirmation.

## Options

- `--force`: Remove without asking (still respects protection).
- `--older-than DAYS`: Delete all unprotected backups older than N days.

## Examples

```bash
# Delete a specific backup
workstate delete e4f1

# Cleanup old backups
workstate delete --older-than 30
```
