---
title: Development from Source
description: Instructions for building and developing Workstate locally.
---

If you want to contribute to Workstate or build it from scratch, follow this guide.

## Building Locally

Workstate uses [Hatch](https://hatch.pypa.io/) as its build system and environment manager.

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/mtpontes/workstate.git
    cd workstate
    ```

2.  **Install via Hatch**:
    ```bash
    hatch run build-local
    ```
    This command will build the wheel and install it in your environment using `pip install -e .`.

## Documentation Development

The documentation site is built with Astro/Starlight.

1.  **Dependencies**: You need Node.js v22.
2.  **Dev Server**:
    ```bash
    hatch run docs-serve
    ```
    This will start the local server at `http://localhost:4321/workstate/`.

## Coding Standards

- **Language**: Core logic is in Python.
- **Style**: We follow PEP8 conventions.
- **Testing**: Run tests using `hatch run test:unit`.
