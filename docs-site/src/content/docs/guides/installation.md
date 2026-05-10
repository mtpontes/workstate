---
title: Installation
description: How to install Workstate on your machine.
---

Workstate is a CLI tool built with Python. You can install it using `pip` or by downloading the standalone binary.

## Prerequisites

- **Python**: Version 3.10 or higher.
- **AWS CLI**: Configured with valid credentials.

## Installation Methods

### Via Pip (Recommended)

```bash
pip install workstate
```

### From Source

If you want the latest development version:

```bash
git clone https://github.com/mtpontes/workstate.git
cd workstate
pip install -e .
```

## Verifying Installation

After installing, run the following command to verify the version:

```bash
workstate --version
```

### Validating Setup (The Doctor Command)

To ensure everything is correctly configured—including your AWS credentials and S3 permissions—use the **doctor** command:

```bash
workstate doctor
```

This command will:
1. Check if the configuration file exists.
2. Validate your AWS Access Keys.
3. Test connectivity and permissions to the configured S3 bucket.

If everything is green, you are ready to go!
