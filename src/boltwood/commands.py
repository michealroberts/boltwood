# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

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
