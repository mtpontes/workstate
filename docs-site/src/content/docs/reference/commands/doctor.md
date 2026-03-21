---
title: doctor
description: Check the health and connectivity of your Workstate setup.
---

The `doctor` command is your first resource for troubleshooting. It runs a suite of tests.

## Usage

```bash
workstate doctor
```

## Tests Performed

1. **AWS Credentials**: Verifies if keys are valid and have permissions.
2. **S3 Connectivity**: Tests connection to the configured bucket.
3. **IAM Permissions**: Simulates basic operations.
4. **Local Config**: Validates `.workstate` and cache integrity.

## Examples

```bash
workstate doctor
```
