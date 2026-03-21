---
title: Quickstart
description: Get up and running with Workstate in 2 minutes.
---

Learn the basic workflow of Workstate: Capture, View, and Restore.

## 1. Initialize

Start tracking your current directory:

```bash
workstate init
```

## 2. Save your State

Capture everything and send it to S3:

```bash
workstate save "my-first-backup"
```

## 3. List Backups

See what you have stored in the cloud:

```bash
workstate list
```

## 4. Restore

Need to go back or setup on a new machine?

```bash
workstate download [ID]
```

## Next Steps

- Explore the [Commands Reference](/workstate/reference/overview/) for advanced options like encryption and git hooks.
