# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from enum import Enum

# **************************************************************************************

# Represents a request for a poll response in the Boltwood protocol:
REQUEST_FOR_POLL_RESPONSE: bytes = b"\x01"

# **************************************************************************************

# Marks the beginning of a framed protocol message in the Boltwood protocol:
FRAME_START: bytes = b"\x02"

# **************************************************************************************

# # Marks the end of a framed protocol message in the Boltwood protocol:
FRAME_END: bytes = b"\n"

# **************************************************************************************


class CommandOperation(Enum):
    """
    Represents the set of operations in the Boltwood protocol.
    """

    # Request a poll response from the device:
    POLL = b"P"

    # Acknowledge receipt of a message from the device:
    ACK = b"A"

    # Indicate a negative acknowledgment (e.g., an error or invalid message)
    # from the device:
    NACK = b"N"

    # Send a message to the device:
    MSG = b"M"


# **************************************************************************************
