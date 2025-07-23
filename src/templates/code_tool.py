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
        return ", ".join([tool_code.value for tool_code in cls])
