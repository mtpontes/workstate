---
title: What is Captured
description: Learn which files and settings Workstate tracks and backs up.
---

Workstate is designed to capture the "intelligence" of your environment without bloating your backups with binaries or temporary files.

## Tracked Files

By default, Workstate looks for:

- **Environment Variables**: `.env`, `.env.local`, `.env.development`.
- **Shell Configs**: `.zshrc`, `.bashrc`, `.profile` (partially or via specific exports).
- **Tool Configs**: `.nvmrc`, `package.json` (for version tracking), `pyproject.toml`, `.python-version`.
- **Infrastructure**: `Dockerfile`, `docker-compose.yml`, Terraform files (`.tf`).

## What is NOT Captured

To keep backups lean and secure, we exclude:

- `node_modules/`
- `.git/` (we track the state, not the whole history)
- `__pycache__/`
- Large binary files (> 50MB by default)
- OS-specific temp files (`.DS_Store`, `Thumbs.db`)

## Customization

You can customize what is captured using the `.workstateignore` file in your root directory, which follows the same syntax as `.gitignore`.
