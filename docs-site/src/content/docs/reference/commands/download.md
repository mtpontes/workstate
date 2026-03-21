---
title: download
description: Restore a specific state from S3 to your local machine.
---

The `download` command is how you recover your environment or set it up on a new device.

## Usage

```bash
workstate download [ID_OR_NAME] [OPTIONS]
```

## Options

- `--force`: Overwrite local files without asking for confirmation.
- `--interactive`: Prompt for every file before overwriting.

## Examples

```bash
# Restore by ID
workstate download e4f1

# Restore the latest backup interactively
workstate download --interactive
```

:::note[Note]
If the backup was encrypted, Workstate will prompt you for the decryption password during download.
:::
