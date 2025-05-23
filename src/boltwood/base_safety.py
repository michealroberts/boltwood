# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from abc import abstractmethod
from enum import Enum
from typing import Any

from .base import BaseDeviceInterface, BaseDeviceParameters

# **************************************************************************************


class BaseSafetyMonitorDeviceState(Enum):
    """
    Enumeration of possible safety states for a device.
    """

    SAFE = 0
    UNSAFE = 1


# **************************************************************************************


class BaseSafetyMonitorDeviceParameters(BaseDeviceParameters):
    pass


# **************************************************************************************


class BaseSafetyMonitorDeviceInterface(BaseDeviceInterface):
    """
    Abstract class representing a generic safety monitor device.

    Extends BaseDeviceInterface by adding safety monitor-specific methods and properties,
    such as the current safety state of the system.

    N.B. The system must be in a safe state to operate nominally. Any unsafe state here
    will be considered a failure of the system. Intermittent failures are not considered
    unsafe states, but rather a failure of the system to operate nominally.
    """

    _id: int = 0

    # The state of the device is the safety state of the system:
    _safety_state: BaseSafetyMonitorDeviceState = BaseSafetyMonitorDeviceState.UNSAFE

    def __init__(
        self,
        id: int,
        parameters: BaseSafetyMonitorDeviceParameters,
        **extras: Any,
    ) -> None:
        """
        Initialize the device with parameters.

        Args:
            parameters (BaseSafetyMonitorDeviceParameters): Device parameters.
        """
        # Set the identifier for the device:
        self._id = id

        self._safety_state = BaseSafetyMonitorDeviceState.UNSAFE

    def is_safe(self) -> bool:
        """
        Check if the device is in a safe state.

        Returns:
            bool: True if device state is SAFE, False otherwise.
        """
        return self._safety_state == BaseSafetyMonitorDeviceState.SAFE

    def is_unsafe(self) -> bool:
        """
        Check if the device is in an unsafe state.

        Returns:
            bool: True if device state is UNSAFE, False otherwise.
        """
        return self._safety_state == BaseSafetyMonitorDeviceState.UNSAFE

    @abstractmethod
    def refresh(self) -> None:
        """
        Refresh the device state.

        This method should implement any necessary operations to refresh the device state.
        """
        raise NotImplementedError("refresh() method must be implemented.")


# **************************************************************************************
