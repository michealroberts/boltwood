# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from re import VERBOSE, compile
from typing import Optional

# **************************************************************************************


def is_hexadecimal(value: Optional[str]) -> bool:
    """
    Check if the given string represents a valid hexadecimal number.

    Args:
        value (Optional[str]): The string to check. Can be None or a string.

    Returns:
        bool: True if the string is a valid hexadecimal False otherwise.
    """
    if not value:
        return False

    # Disallow leading or trailing whitespace:
    if value.strip() != value:
        return False

    # Disallow leading '+' or '-' signs:
    if value[0] in ("+", "-"):
        return False

    try:
        int(value, 16)
        return True
    except ValueError:
        return False


# **************************************************************************************


_SEMANTIC_VERSION_PATTERN = compile(
    r"""
            ^v?                                  
            (?P<major>0|[1-9]\d*)
            (?:\.(?P<minor>0|[1-9]\d*))?
            (?:\.(?P<patch>0|[1-9]\d*))?
            (?:-[\da-zA-Z-]+(?:\.[\da-zA-Z-]+)*)?
            (?:\+[\da-zA-Z-]+(?:\.[\da-zA-Z-]+)*)?
            $
        """,
    VERBOSE,
)

# **************************************************************************************


def parse_semantic_version(value: str) -> tuple[int, int, int]:
    """
    Parse a semantic version string into its components.

    Args:
        value (str): The semantic version string to parse.

    Returns:
        tuple[int, int, int]: A tuple containing the major, minor, and patch version numbers.
    """
    # Check if the value matches with the semantic version pattern regex:
    m = _SEMANTIC_VERSION_PATTERN.match(value)

    # If the value does not match the pattern, raise a ValueError:
    if not m:
        raise ValueError(f"Invalid semantic version: {value!r}")

    # Extract the named groups from the match object:
    version = m.groupdict()

    # Convert the named groups to integers:
    major = int(version["major"])
    minor = int(version["minor"]) if version.get("minor") is not None else 0
    patch = int(version["patch"]) if version.get("patch") is not None else 0

    # Return the major, minor, and patch version numbers as a tuple:
    return major, minor, patch


# **************************************************************************************
