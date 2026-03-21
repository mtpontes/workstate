---
title: compare
description: Compare your local state against a specific backup.
---

The `compare` command provides a line-by-line diff of what has changed between your local files and a remote state.

## Usage

```bash
workstate compare [ID_OR_NAME]
```

## Information Displayed

- **Added Lines (+)**: New environment variables or settings you added locally.
- **Removed Lines (-)**: Settings that exist in the cloud but are missing locally.
- **Modified Lines**: Value changes for the same key.

## Examples

```bash
workstate compare e4f1
```
