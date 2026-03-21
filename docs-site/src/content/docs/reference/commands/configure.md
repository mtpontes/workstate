---
title: configure
description: Setup AWS credentials and S3 bucket for Workstate.
---

The `configure` command is the first step to using Workstate. It links your local environment to your AWS account.

## Usage

```bash
workstate configure [OPTIONS]
```

## Options

- `--profile TEXT`: Use a specific AWS profile from your `~/.aws/credentials`.
- `--bucket TEXT`: Specify a custom S3 bucket name.
- `--region TEXT`: Specify the AWS region (e.g., `us-east-1`).

## Examples

```bash
# Interactive setup (Recommended)
workstate configure

# Setup with specific profile and bucket
workstate configure --profile dev-user --bucket my-work-backups
```

:::tip[Tip]
If the bucket doesn't exist, Workstate will offer to create it for you automatically with the correct security settings.
:::
