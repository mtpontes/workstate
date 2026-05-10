---
title: Quickstart
description: Get up and running with Workstate in less than 5 minutes.
---

Workstate helps you capture and restore your development environment. This guide covers the essential workflow: Setup, Initialize, Verify, and Save.

## 1. Configure AWS
Before anything else, you need to tell Workstate where to store your snapshots:

```bash
workstate configure
```
*You will be prompted for your AWS Access Key, Secret Key, Region, and S3 Bucket name.*

## 2. Initialize your Project
Go to your project's root directory and initialize it:

```bash
workstate init
```

This creates a `.workstateinclude` file with minimalist defaults. Unlike a blacklist, **only files listed here will be captured.**

## 3. Verify what's captured
Since we use a whitelist approach, it's a good idea to check what Workstate "sees":

```bash
workstate status
```
*This command lists all files that will be included in the next snapshot.*

## 4. Save your State
Capture your current environment and upload it to S3:

```bash
workstate save "my-feature-setup"
```

## 5. List and Restore
To see your stored states and bring one back:

```bash
workstate list
workstate download
```

## Next Steps
- Learn more about [What is Captured](/workstate/foundations/what-is-captured/) (Whitelist vs Blacklist).
- Explore [Command Reference](/workstate/reference/commands/save/) for advanced flags like `--include` and `--encrypt`.
