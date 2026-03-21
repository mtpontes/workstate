---
title: init
description: Initialize Workstate tracking in the current directory.
---

The `init` command prepares your project folder to be tracked by Workstate.

## Usage

```bash
workstate init
```

## How it works

- Creates a hidden `.workstate` folder (if it doesn't exist).
- Generates a local configuration file with a unique project ID.
- Scans for common development files to track.

## Examples

```bash
cd my-project
workstate init
```

:::note[Note]
Initializing a project doesn't upload anything to S3 yet. Use `save` for that.
:::
