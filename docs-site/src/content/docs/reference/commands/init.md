---
title: init
description: Initialize Workstate tracking in the current directory.
---

The `init` command prepares your project folder to be tracked by Workstate by creating the necessary configuration files.

## Usage

```bash
workstate init
```

## How it works

1. **Creates `.workstateinclude`**: Generates a whitelist file in your root directory. Only files and patterns listed here will be captured by the `save` command.
2. **Populates Defaults**: Automatically adds sensible defaults to the include file (e.g., `src/`, `README.md`, `pyproject.toml`).
3. **Auto-detection**: Attempts to detect your project stack (Python, Node, etc.) to tailor the environment setup.

## Examples

```bash
cd my-project
workstate init
```

:::note[Note]
Initializing a project doesn't upload anything to S3 yet. It only prepares the local configuration. Use `workstate save` to create your first snapshot.
:::
