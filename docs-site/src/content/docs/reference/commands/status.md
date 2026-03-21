---
title: status
description: Show differences between local state and the latest backup on S3.
---

The `status` command helps you understand if your local environment is up-to-date or if you have unsaved changes.

## Usage

```bash
workstate status
```

## Information Displayed

- **Sync Status**: Tells you if you are ahead or behind the cloud.
- **Changed Files**: Lists environment variables or config files that differ.
- **Last Sync**: Shows the timestamp of the last successful `save` or `download`.

## Examples

```bash
$ workstate status
🔍 Checking state...

[MODIFIED] .env
[UNCHANGED] package.json

You have local changes not yet saved to S3.
```
