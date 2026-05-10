---
title: list
description: List available environment states on S3.
---

The `list` command displays states stored in your S3 bucket. By default, it performs a **global scan**, showing states from all projects in the bucket.

## Usage

```bash
workstate list [OPTIONS]
```

## Options

- `-p, --project`: Filter the list to show only states belonging to the current project.
- `-s, --system NAME`: Filter by operating system (e.g., `Windows`, `Linux`).
- `-b, --branch NAME`: Filter by Git branch name.
- `-o, --older-than DURATION`: Show states older than a duration (e.g., `30d` for 30 days, `1y` for 1 year).
- `-i, --interactive`: Enter interactive mode to browse and select states using fuzzy search.
- `--no-cache`: Bypass the local metadata cache and fetch the fresh list directly from S3.

## Examples

```bash
# List all states across all projects (Default)
workstate list

# Show only states for the current project
workstate list --project

# Find states from a specific branch
workstate list --branch feature/login

# Browse states interactively
workstate list -i

# Clean up check: find states older than 6 months
workstate list --older-than 6m
```

:::note
Workstate uses a local cache to speed up listings. If you suspect the list is outdated, use the `--no-cache` flag.
:::
