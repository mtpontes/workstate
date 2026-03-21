---
title: Hooks and Automation
description: Integrate Workstate with your Git workflow and automation scripts.
---

Automation is at the heart of Workstate. You can use hooks to ensure your environment is always in sync.

## Native Git Hooks

Workstate can automatically install hooks in your repository to remind you to sync or save.

- **Post-Checkout**: Reminds you to run `workstate sync` when you switch branches.
- **Pre-Push**: Suggests a `workstate save` before you push your code.

To install them, run:
```bash
workstate git-hook install
```

## Post-Download Scripts

You can define custom shell scripts to run immediately after a `download` or `sync`. This is perfect for:
- Re-installing dependencies (`npm install`).
- Restarting local services.
- Sourcing environment variables.

Create a script named `.workstate/post-sync.sh` in your project root, and Workstate will execute it automatically.

## CI/CD Integration

Since Workstate is a standard CLI tool, you can easily use it in GitHub Actions, GitLab CI, or Jenkins.

```yaml
- name: Restore Development Environment
  run: workstate sync
```
