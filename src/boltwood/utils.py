# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

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
