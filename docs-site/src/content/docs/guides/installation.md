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

After installing, run the following command to verify:

```bash
workstate --version
```

If you see the version number, you are ready to go!
