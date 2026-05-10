---
title: save
description: Capture and upload the current environment state to S3.
---

The `save` command creates a "snapshot" of your environment and stores it securely in the cloud. It follows the inclusion rules defined in your `.workstateinclude` file.

## Usage

```bash
workstate save [NAME] [OPTIONS]
```

## Options

- `-i, --include PATH`: Add extra files or patterns to the current snapshot (ad-hoc inclusion).
- `--encrypt`: Encrypt the backup locally before uploading.
- `-p, --protect`: Mark the backup as "protected" to prevent accidental deletion.
- `-m, --description TEXT`: Add a descriptive note or motive to the backup.
- `--tag KEY=VALUE`: Apply custom tags to the S3 object for easier filtering.
- `--dry-run`: Simulate the process and list files that would be captured without uploading.

## Examples

```bash
# Simple save using .workstateinclude rules
workstate save "base-setup"

# Save with ad-hoc inclusion (e.g., a specific log file)
workstate save "debug-session" --include "logs/error.log"

# Multi-pattern inclusion
workstate save "full-state" -i "config/*.yaml" -i "data/*.csv"

# Encrypted and protected save with a description
workstate save "prod-env" --encrypt --protect -m "Initial production sync"
```

:::tip[Pro Tip]
Use `workstate status` before saving to verify exactly which files are being picked up by your whitelist.
:::

:::caution[Important]
If you use `--encrypt`, you will be asked for a password. **We do not store your passwords.** If you lose it, the state cannot be restored.
:::
