"""
Module responsible for defining the code tools supported by the Workstate application.

The `CodeTool` enumeration represents languages and frameworks that support `.workstateignore` templates.

Main functions:
    - Allows the use of standardized names for supported tools.
    - Provides a list of valid values as a string for display.

Class:
    - CodeTool(Enum): Enum with the supported code tools.
"""

from enum import Enum
from pathlib import Path
from typing import List


class CodeTool(Enum):
    """
    Enum representing the supported code tools for generating `.workstateignore` templates.

    Possible values:
        - NODE
        - REACT
        - ANGULAR
        - JAVA
        - C
        - CPP
        - CSHARP
        - PHP
        - PYTHON
        - DEFAULT
    """

    NODE = "node"
    REACT = "react"
    ANGULAR = "angular"
    JAVA = "java"
    C = "c"
    CPP = "c++"
    CSHARP = "c#"
    PHP = "php"
    PYTHON = "python"
    DEFAULT = "default"

    @classmethod
    def get_valid_values(cls) -> str:
        return ", ".join([this.value for this in cls])

    @classmethod
    def detect_tools(cls) -> List["CodeTool"]:
        """
        Detects project stacks based on files present in the current directory.

        Returns:
            List[CodeTool]: List of detected tools.
        """
        detected: List[CodeTool] = []
        root = Path.cwd()

        # Mapping of files to CodeTool
        mapping = {
            "package.json": cls.NODE,
            "requirements.txt": cls.PYTHON,
            "Pipfile": cls.PYTHON,
            "pyproject.toml": cls.PYTHON,
            "pom.xml": cls.JAVA,
            "build.gradle": cls.JAVA,
            "build.gradle.kts": cls.JAVA,
            "composer.json": cls.PHP,
            "Makefile": cls.C,
            "CMakeLists.txt": cls.CPP,
        }

        for filename, tool in mapping.items():
            if (root / filename).exists():
                if tool not in detected:
                    detected.append(tool)

        # Check for C# projects
        if list(root.glob("*.csproj")) or list(root.glob("*.sln")):
            if cls.CSHARP not in detected:
                detected.append(cls.CSHARP)

        return detected
