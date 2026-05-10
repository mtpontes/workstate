---
title: status
description: View which files are currently being tracked and included for snapshots.
---

The `status` command lists all files in your project that match the rules in your `.workstateinclude` (whitelist) or `.workstateignore` (legacy blacklist). It's the best way to verify what will be uploaded before running `save`.

## Usage

```bash
workstate status
```

## Information Displayed

- **Included Files**: A list of all files that Workstate is currently tracking.
- **Total Size**: The combined size of all tracked files.
- **Project Context**: Information about your current project name and AWS bucket.

## Examples

```bash
$ workstate status
🔍 Analyzing project state...

Current project: workstate
S3 Bucket: my-work-states

Tracked files (Whitelist mode):
- .workstateinclude
- src/main.py
- src/services/file_service.py
- README.md

Total: 4 files (145.2 KB)
```
