# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datetime import datetime, timezone
from typing import List, Tuple

from samps import (
    BaudrateType,
    SerialCommonInterface,
    SerialCommonInterfaceParameters,
)

from .base import (
    BaseDeviceState,
)
from .base_safety import (
    BaseSafetyMonitorDeviceInterface,
    BaseSafetyMonitorDeviceParameters,
    BaseSafetyMonitorDeviceState,
)
from .responses import PATTERN_SAFETY_MONITOR_ALL_RESPONSE
from .status import BoltwoodIIISafetyMonitorDeviceStatus
from .utils import parse_semantic_version
from .version import BOLTWOOD_DRIVER_SEMANTIC_VERSION

# **************************************************************************************


class BoltwoodIIISafetyMonitorDeviceParameters(
    BaseSafetyMonitorDeviceParameters,
):
    name: str
    description: str
    port: str
    baudrate: BaudrateType


# **************************************************************************************


class BoltwoodIIISafetyMonitorDeviceInterface(BaseSafetyMonitorDeviceInterface):
    """ """

    _id: int = 0

    # The
    _port: str = "/dev/ttyUSB0"

    # The baudrate of the safety monitor (in bits per second):
    _baudrate: BaudrateType = 9600

    # When did we last successfully poll the device?
    _last_polling_time: datetime = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    # The state of the device is the safety state of the system (assume we are unsafe
    # until we are told otherwise):
    _safety_state: BaseSafetyMonitorDeviceState = BaseSafetyMonitorDeviceState.UNSAFE

    def __init__(
        self,
        id: int,
        params: BoltwoodIIISafetyMonitorDeviceParameters,
    ) -> None:
        """
        Initialise the base safety monitor interface.

        Args:
            params (BoltwoodIIISafetyMonitorDeviceParameters): A dictionary-like object
                containing device parameters such as vendor ID (vid), product ID (pid),
                or device ID (did).
        """
        super().__init__(id, params)

        # Set the port of the device:
        self._port = params.get("port", "/dev/ttyUSB0")

        # Set the baudrate of the device:
        self._baudrate = params.get("baudrate", 9600)

        # The name of the safety monitor (default: "Boltwood Safety Monitor"):
        self._name = params.get("name", "Boltwood safety monitor")

        # The description of the safety monitor (default: Boltwood Safety Monitor Interface):
        self._description = params.get(
            "description", f"Boltwood Safety Monitor Interface ({self._port})"
        )

    @property
    def id(self) -> int:
        """
        Unique identifier for the device.

        Returns:
            int: The unique device identifier.
        """
        return self._id

    def _read_all_parameters(self) -> BoltwoodIIISafetyMonitorDeviceStatus:
        """
        Send a "G OC all" query and return the result as a list of floats.

        The result is a list of 14 values, where each value corresponds to a specific
        parameter. If a parameter is not available (e.g., "NA"), it will be set to "None":
        """
        if self.state != BaseDeviceState.CONNECTED:
            raise RuntimeError(f"[ID {self.id}]: Device not connected")

        # Construct the command to send to the device:
        command = b"G SM all\n"

        # Write the command to the device:
        self._serial.write(command)

        now = datetime.now(timezone.utc)

        try:
            # Read the response from the device:
            response = self._serial.readline().decode("ascii").strip()
        except Exception as e:
            raise RuntimeError(
                f"[Safety Monitor ID {self.id}]: Error reading from device on port {self._port}: {e}"
            )

        if response == 0:
            raise RuntimeError(
                f"[Safety Monitor ID {self.id}]: No response from device on port {self._port}."
            )

        code, *result = response.split(" ", 1)

        # If the response code is not "0", raise an exception to indicate an error:
        if code != "0":
            msg = result[0] if result else "Unknown error"
            raise RuntimeError(
                f"[Safety Monitor ID {self.id}]: Error reading SM all: {msg}"
            )

        parameters = PATTERN_SAFETY_MONITOR_ALL_RESPONSE.match(response)

        # If the response does not match the expected pattern, raise an exception:
        if not parameters:
            raise RuntimeError(
                f"[Safety Monitor ID {self.id}]: Error reading SM all: {response}"
            )

        data = {
            "utc": now,
            **{
                name: (None if val == "NA" else float(val))
                for name, val in parameters.groupdict().items()
                if name
                in {
                    "is_safe",
                }
            },
        }

        # Attempt to parse the parameters from the response and validate them with
        # the status model:
        return BoltwoodIIISafetyMonitorDeviceStatus.model_validate(data)

    def initialise(self, timeout: float = 5.0, retries: int = 3) -> None:
        """
        Initialise the device.

        This method should handle any necessary setup required before the device can be used.
        """

        # Define the initialisation function to be run in a separate thread:
        def do_initialise() -> None:
            if self.state == BaseDeviceState.CONNECTED:
                return

            # We leave the device state as DISCONNECTED until connect() is called:
            self.state = BaseDeviceState.DISCONNECTED

            # If we have a device ID, attempt to connect:
            self.connect(timeout=timeout, retries=retries)

        # Keep a track of the number of attempts:
        i = 0

        # Try to initialise the safety monitor up to `retries` times, with the given timeout:
        while i < retries:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(do_initialise)
                try:
                    # Block for up to `timeout` seconds to see if init completes
                    future.result(timeout=timeout)
                    return
                except TimeoutError:
                    # If we have a timeout after the retries are exhausted, raise an exception:
                    if i == retries - 1:
                        raise TimeoutError(
                            f"[Safety Monitor ID {self.id}]: Did not initialize within {timeout} seconds "
                            f"after {retries} attempts."
                        )
                except RuntimeError as error:
                    # If we have a runtime error after the retries are exhausted, raise it:
                    if i == retries - 1:
                        raise error

            # Increment the retry counter:
            i += 1

    def reset(self) -> None:
        """
        Reset the device.

        This method should restore the device to its default or initial state.
        """
        # Reset the device state to DISCONNECTED:
        self.disconnect()

        # Re-initialise the device:
        self.initialise()

    def connect(self, timeout: float = 5.0, retries: int = 3) -> None:
        """
        Establish a connection to the device.

        This method should implement the operations required to connect to the device.
        """
        if self.state == BaseDeviceState.CONNECTED:
            return

        serial_params = SerialCommonInterfaceParameters(
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=10,
            xonxoff=False,
            rtscts=False,
        )

        self._serial = SerialCommonInterface(
            port=self._port,
            baudrate=self._baudrate,
            params=serial_params,
        )

        self._serial.open()

        # If the device is not open, raise an exception:
        if not self._serial.is_open():
            raise RuntimeError(
                f"[Safety Monitor ID {self.id}]: Unable to open serial port {self._port}."
            )

        # Set the device state to CONNECTED if the connection is successful and the device is open:
        self.state = BaseDeviceState.CONNECTED

    def disconnect(self) -> None:
        """
        Disconnect from the device.

        This method should handle any cleanup or shutdown procedures necessary to safely
        disconnect from the device.
        """
        if self.state == BaseDeviceState.DISCONNECTED:
            return

        if not self._serial.is_open():
            self.state = BaseDeviceState.DISCONNECTED
            return

        # Close the serial port:
        self._serial.close()

        # Set the device state to DISCONNECTED:
        self.state = BaseDeviceState.DISCONNECTED

    def is_connected(self) -> bool:
        """
        Check if the device is connected.

        Returns:
            bool: True if the device is connected; otherwise, False.
        """
        if self.state == BaseDeviceState.DISCONNECTED:
            return False

        is_open = self._serial.is_open()

        return True if self.state == BaseDeviceState.CONNECTED and is_open else False

    def is_ready(self) -> bool:
        """
        Check if the device is ready for operation.

        Returns:
            bool: True if the device is ready; otherwise, False.
        """
        if self.state == BaseDeviceState.DISCONNECTED:
            return False

        is_open = self._serial.is_open()

        return True if self.state == BaseDeviceState.CONNECTED and is_open else False

    def get_name(self) -> str:
        """
        Get the name of the device.

        Returns:
            str: The device name.
        """
        return self._name

    def get_description(self) -> str:
        """
        Get a description of the device.

        Returns:
            str: A brief description of the device.
        """
        if self.state != BaseDeviceState.CONNECTED:
            return self._description

        # Construct the command to send to the device for the description:
        command = b"G OC sensordescription 0\n"

        # Write the read command to the device:
        self._serial.write(command)

        response = self._serial.readline().decode("ascii").strip()

        # The format of the response is, e.g., "0 <SENSOR_DESCRIPTION>" so we split on
        # the first space:
        code, *result = response.split(" ", 1)

        # If the response code is not "0", return an empty string as we assume
        # the device is not connected or the command failed:
        if code != "0":
            raise RuntimeError(
                f"[Conditions Monitor ID {self.id}]: Error reading description: {result[0]}"
            )

        description = result[0].strip()

        # Return the description from the result, if available, otherwise return the
        # default description:
        return (
            description
            if description and description != "description"
            else self._description
        )

    def get_serial_number(self) -> str:
        """
        Get the serial number of the device.

        Returns:
            str: The serial number of the device.
        """
        if self.state != BaseDeviceState.CONNECTED:
            return ""

        # Construct the command to send to the device for the serial number:
        command = b"G DD serial\n"

        # Write the read command to the device:
        self._serial.write(command)

        response = self._serial.readline().decode("ascii").strip()

        # The format of the response is, e.g., "0 BCS322051101" so we split on
        # the first space:
        code, *result = response.split(" ", 1)

        # If the response code is not "0", return an empty string as we assume
        # the device is not connected or the command failed:
        if code != "0":
            raise RuntimeError(
                f"[Conditions Monitor ID {self.id}]: Error reading serial number: {result[0]}"
            )

        # Return the serial number from the result, if available:
        return result[0]

    def get_driver_version(self) -> Tuple[int, int, int]:
        """
        Get the version of the device driver as a tuple (major, minor, patch).

        Returns:
            Tuple[int, int, int]: The driver version.
        """
        return BOLTWOOD_DRIVER_SEMANTIC_VERSION

    def get_firmware_version(self) -> Tuple[int, int, int]:
        """
        Get the version of the device firmware as a tuple (major, minor, patch).

        Returns:
            Tuple[int, int, int]: The firmware version. Defaults to (-1, -1, -1).
        """
        if self.state != BaseDeviceState.CONNECTED:
            return -1, -1, -1

        # Construct the command to send to the device for the firmware version:
        command = b"G DD fwrev\n"

        # Write the read command to the device:
        self._serial.write(command)

        response = self._serial.readline().decode("ascii").strip()

        # The format of the response is, e.g., "0 BCS322051101" so we split on
        # the first space:
        code, *result = response.split(" ", 1)

        # If the response code is not "0", return an empty string as we assume
        # the device is not connected or the command failed:
        if code != "0":
            raise RuntimeError(
                f"[Conditions Monitor ID {self.id}]: Error reading firmware version: {result[0]}"
            )

        version = result[0].strip()

        try:
            return parse_semantic_version(version)
        except ValueError:
            # If we have a value error, return -1, -1, -1 as the default version:
            return -1, -1, -1

    def get_capabilities(self) -> List[str]:
        """
        Retrieve a list of capabilities supported by the device.

        Returns:
            List[str]: A list of capability names. Defaults to an empty list.
        """
        return []

    def _is_closed(self) -> bool:
        """
        Check if the device is closed.

        Returns:
            bool: True if the device is closed; otherwise, False.
        """
        return not self._serial.is_open()

    def get_status(self) -> BoltwoodIIISafetyMonitorDeviceStatus:
        """
        Retrieve the current status of the device.

        Returns:
            BoltwoodIIISafetyMonitorDeviceStatus: The current status of the device.
        """
        return self._read_all_parameters()

    def is_safe(self) -> bool:
        """
        Check if the device is in a safe state.

        Returns:
            bool: True if device state is SAFE, False otherwise.
        """
        # Read all of the latest safety status from the device, (if available). This will
        # update the internal state of the device interface:
        status = self._read_all_parameters()

        # Update the internal state of the device interface with the latest safety status:
        self._last_polling_time = status.utc

        # Update the safety state of the device based on the latest status:
        self._safety_state = (
            BaseSafetyMonitorDeviceState.SAFE
            if status.is_safe
            else BaseSafetyMonitorDeviceState.UNSAFE
        )

        return self._safety_state == BaseSafetyMonitorDeviceState.SAFE

    def is_unsafe(self) -> bool:
        """
        Check if the device is in an unsafe state.

        Returns:
            bool: True if device state is UNSAFE, False otherwise.
        """
        return not self.is_safe()

    def refresh(self) -> None:
        """
        Refresh the device state.

        This method should implement any necessary operations to refresh the device state.

        Raises:
            RuntimeError: If the device is not connected or if there is an error refreshing
                the device state.
        """
        # If the device is not connected, raise an exception:
        if self.state == BaseDeviceState.DISCONNECTED:
            raise RuntimeError(
                f"[Safety Monitor ID {self.id}]: Device is not connected."
            )

        # Construct the command to send to the device for refreshing:
        command = b"P OC refresh 1\n"

        # Write the refresh command to the device:
        self._serial.write(command)

        # Read the acknowledgment response from the device:
        response = self._serial.readline().decode("ascii").strip()

        at = datetime.now(timezone.utc)

        # The response should be "0" if the refresh was successful:
        if not response.startswith("0"):
            raise RuntimeError(
                f"[Safety Monitor ID {self.id}]: Error refreshing device: {response}"
            )

        # If the refresh was successful, update the last polling time:
        self._last_polling_time = at


# **************************************************************************************
