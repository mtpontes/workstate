---
title: Commands Overview
description: A complete table of all available Workstate commands.
---

Workstate provides a powerful CLI to manage your environment states. Here is a summary of all commands.

| Command | Description |
| :--- | :--- |
| `configure` | Setup AWS credentials and S3 bucket. |
| `init` | Initialize Workstate tracking in the current directory. |
| `status` | Show differences between local state and S3. |
| `save` | Capture and upload the current environment state. |
| `list` | List available backups on S3. |
| `download` | Restore a state from S3 to your machine. |
| `sync` | Automatically sync with the latest backup. |
| `compare` | Compare local state against a specific backup. |
| `inspect` | View detailed metadata of a specific backup. |
| `protect` | Lock a backup to prevent accidental deletion. |
| `delete` | Remove backups from S3. |
| `git-hook` | Install or remove Git integration hooks. |
| `doctor` | Check health and connectivity of your setup. |
| `update` | Update Workstate to the latest version. |

## Documentation per Command

Each command has a dedicated page with detailed options and examples. Explore them in the **Commands** section of the sidebar.
