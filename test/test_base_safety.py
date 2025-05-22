# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from typing import Any, List, Tuple

from boltwood.base_safety import (
    BaseSafetyMonitorDeviceInterface,
    BaseSafetyMonitorDeviceParameters,
    BaseSafetyMonitorDeviceState,
)

# **************************************************************************************


class DummySafetyMonitorDeviceInterface(BaseSafetyMonitorDeviceInterface):
    """
    Dummy implementation of BaseSafetyMonitorDeviceInterface for testing.

    It provides fixed behaviors for the abstract methods.
    """

    def __init__(
        self, parameters: BaseSafetyMonitorDeviceParameters, **extras: Any
    ) -> None:
        super().__init__(parameters, **extras)
        self.initialised = False
        self.reset_called = False
        self.connected = False

    def initialise(self, timeout: float = 5.0, retries: int = 3) -> None:
        self.initialised = True

    def reset(self) -> None:
        self.reset_called = True

    def is_connected(self) -> bool:
        return True

    def is_ready(self) -> bool:
        return True

    def get_name(self) -> str:
        return "Dummy Safety Device"

    def get_description(self) -> str:
        return "Dummy safety monitor"

    def get_driver_version(self) -> Tuple[int, int, int]:
        return (0, 1, 0)

    def get_firmware_version(self) -> Tuple[int, int, int]:
        return (0, 1, 1)

    def connect(self, timeout: float = 5.0, retries: int = 3) -> None:
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False

    def get_capabilities(self) -> List[str]:
        return ["safety_check"]

    def refresh(self) -> None:
        # Flip to unsafe to simulate a safety event:
        self._safety_state = BaseSafetyMonitorDeviceState.UNSAFE


# **************************************************************************************


class TestBaseSafetyMonitorDeviceInterface(unittest.TestCase):
    def setUp(self) -> None:
        params = BaseSafetyMonitorDeviceParameters(
            {
                "id": 1,
                "did": "ddid",
                "vid": "dvid",
                "pid": "dpid",
            }
        )
        self.device = DummySafetyMonitorDeviceInterface(params)

    def test_initial_state_safe(self) -> None:
        """Device should start in SAFE state."""
        self.assertTrue(hasattr(self.device, "is_safe"), "Missing is_safe method")
        self.assertTrue(self.device.is_safe())
        self.assertFalse(self.device.is_unsafe())

    def test_refresh_changes_to_unsafe(self) -> None:
        """Calling refresh() should transition the device to UNSAFE."""
        self.device.refresh()
        self.assertFalse(self.device.is_safe())
        self.assertTrue(self.device.is_unsafe())

    def test_refresh_method_exists_and_no_error(self) -> None:
        """Test that refresh exists and does not raise unexpected errors."""
        self.assertTrue(hasattr(self.device, "refresh"), "Missing refresh method")
        try:
            self.device.refresh()
        except Exception as e:
            self.fail(f"refresh() raised an exception: {e}")


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
