---
title: save
description: Capture and upload the current environment state to S3.
---

The `save` command creates a "snapshot" of your environment and stores it securely in the cloud.

## Usage

```bash
workstate save [NAME] [OPTIONS]
```

## Options

- `--encrypt`: Encrypt sensitive files locally before uploading.
- `--protect`: Mark the backup as "protected" to prevent accidental deletion.
- `-m, --message TEXT`: Add a descriptive note to the backup.

## Examples

```bash
# Simple save
workstate save "base-setup"

# Encrypted and protected save
workstate save "prod-env" --encrypt --protect
```

:::caution[Important]
If you use `--encrypt`, you will be asked for a password. Don't forget it! We don't store your passwords anywhere.
:::
