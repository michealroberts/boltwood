# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datetime import datetime, timezone
from logging import warning
from math import inf
from typing import List, Tuple

from celerity.coordinates import GeographicCoordinate
from celerity.night import is_night
from samps import (
    BaudrateType,
    SerialCommonInterface,
    SerialCommonInterfaceParameters,
)

from .base import (
    BaseDeviceState,
)
from .base_conditions import (
    BaseConditionsMonitorDeviceInterface,
    BaseConditionsMonitorDeviceParameters,
)
from .responses import PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE
from .status import BoltwoodIIIConditionsMonitorDeviceStatus
from .utils import parse_semantic_version
from .version import BOLTWOOD_DRIVER_SEMANTIC_VERSION

# **************************************************************************************


class BoltwoodIIIConditionsMonitorDeviceParameters(
    BaseConditionsMonitorDeviceParameters,
):
    name: str
    description: str
    port: str
    baudrate: BaudrateType


# **************************************************************************************


class BoltwoodIIIConditionsMonitorDeviceInterface(BaseConditionsMonitorDeviceInterface):
    """ """

    _id: int = 0

    # The latitude of the conditions monitor (in degrees):
    _latitude: float = 0.0

    # The longitude of the conditions monitor (in degrees):
    _longitude: float = 0.0

    # The elevation of the conditions monitor (in meters):
    _elevation: float = 0.0

    # The
    _port: str = "/dev/ttyUSB0"

    # The baudrate of the conditions monitor (in bits per second):
    _baudrate: BaudrateType = 9600

    # The raw data received from the device:
    _raw_data: bytes = b""

    # When did we last successfully poll the device?
    _last_polling_time: datetime = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    _atmospheric_dew_point: float = inf

    _cloud_coverage: float = inf

    _humidity: float = inf

    _precipitation_rate: float = inf

    _pressure: float = inf

    _sky_brightness: float = inf

    _sky_temperature: float = inf

    _sky_quality: float = inf

    _star_full_width_half_maximum: float = inf

    _temperature: float = inf

    _wind_direction: float = inf

    _wind_gust: float = inf

    _wind_speed: float = inf

    def __init__(
        self,
        id: int,
        params: BoltwoodIIIConditionsMonitorDeviceParameters,
    ) -> None:
        """
        Initialise the base conditions monitor interface.

        Args:
            params (BoltwoodIIIConditionsMonitorDeviceParameters): A dictionary-like object
                containing device parameters such as vendor ID (vid), product ID (pid),
                or device ID (did).
        """
        super().__init__(id, params)

        # Set the port of the device:
        self._port = params.get("port", "/dev/ttyUSB0")

        # Set the baudrate of the device:
        self._baudrate = params.get("baudrate", 9600)

        # The name of the conditions monitor (default: "Boltwood Conditions Monitor"):
        self._name = params.get("name", "Boltwood Conditions Monitor")

        # The description of the conditions monitor (default: Boltwood Conditions Monitor Interface):
        self._description = params.get(
            "description", f"Boltwood Conditions Monitor Interface ({self._port})"
        )

        # Set the site geographic coordinates (latitude, longitude, elevation) of the conditions monitor:
        self._latitude = params.get("latitude", 0.0)
        self._longitude = params.get("longitude", 0.0)
        self._elevation = params.get("elevation", 0.0)

    @property
    def id(self) -> int:
        """
        Unique identifier for the device.

        Returns:
            int: The unique device identifier.
        """
        return self._id

    def _read_all_parameters(self) -> BoltwoodIIIConditionsMonitorDeviceStatus:
        """
        Send a "G OC all" query and return the result as a list of floats.

        The result is a list of 14 values, where each value corresponds to a specific
        parameter. If a parameter is not available (e.g., "NA"), it will be set to "None":
        """
        if self.state != BaseDeviceState.CONNECTED:
            raise RuntimeError(f"[ID {self.id}]: Device not connected")

        # Construct the command to send to the device:
        command = b"G OC all\n"

        # Write the command to the device:
        self._serial.write(command)

        now = datetime.now(timezone.utc)

        # Read the response from the device:
        response = self._serial.readline().decode("ascii").strip()

        code, *result = response.split(" ", 1)

        # If the response code is not "0", raise an exception to indicate an error:
        if code != "0":
            msg = result[0] if result else "Unknown error"
            raise RuntimeError(
                f"[Conditions Monitor ID {self.id}]: Error reading OC all: {msg}"
            )

        parameters = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(response)

        # If the response does not match the expected pattern, raise an exception:
        if not parameters:
            raise RuntimeError(
                f"[Conditions Monitor ID {self.id}]: Error reading OC all: {response}"
            )

        data = {
            "utc": now,
            **{
                name: (None if val == "NA" else float(val))
                for name, val in parameters.groupdict().items()
                if name
                in {
                    "atmospheric_dew_point",
                    "cloud_coverage",
                    "humidity",
                    "precipitation_rate",
                    "sky_temperature",
                    "temperature",
                    "wind_direction",
                    "wind_speed",
                    "wind_gust",
                }
            },
        }

        # Attempt to parse the parameters from the response and validate them with
        # the status model:
        return BoltwoodIIIConditionsMonitorDeviceStatus.model_validate(data)

    def _read_float_parameter(self, subsystem: str, parameter: str) -> float:
        """
        Send a "G <subsystem> <param>" query and return the float result or inf on parse error.

        Args:
            subsystem (str): The subsystem to query.
            parameter (str): The parameter to query.

        Returns:
            float: The value of the parameter, or inf if the parameter is not available.

        Raises:
            RuntimeError: If the device is not connected or if there is an error reading the parameter.
        """
        # If we are not connected, raise an exception to indicate the device is not connected:
        if self.state != BaseDeviceState.CONNECTED:
            raise RuntimeError(
                f"[Conditions Monitor ID {self.id}]: Device not connected"
            )

        # Construct the command to send to the device:
        command = f"G {subsystem} {parameter}\n".encode("ascii")

        # Write the command to the device:
        self._serial.write(command)

        response = self._serial.readline().decode("ascii").strip()

        code, *result = response.split(" ", 1)

        # If the response code is not "0", raise an exception to indicate an error:
        if code != "0":
            msg = result[0] if result else "Unknown error"

            print(msg)

            raise RuntimeError(
                f"[Conditions Monitor ID {self.id}]: Error reading {subsystem} {parameter}: {msg}"
            )

        # If the result is "NA", it means the parameter is not available, and we shoudl raise
        # a not implemented error:
        if result[0] == "NA":
            raise NotImplementedError(
                f"[Conditions Monitor ID {self.id}]: {subsystem} {parameter} not available for this device."
            )

        # If we have a result, try to convert it to a float and return it:
        try:
            return float(result[0])
        except (IndexError, ValueError):
            # If we have an index error or value error, return inf as the default
            # value as it is physically impossible:
            return inf

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

        # Try to initialise the conditions monitor up to `retries` times, with the given timeout:
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
                            f"[Conditions Monitor ID {self.id}]: Did not initialize within {timeout} seconds "
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
                f"[Conditions Monitor ID {self.id}]: Unable to open serial port {self._port}."
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
        return [
            "atmospheric_dew_point",
            "cloud_coverage",
            "humidity",
            "precipitation_rate",
            "sky_brightness",
            "sky_temperature",
            "temperature",
            "wind_gust",
            "wind_speed",
        ]

    def _is_closed(self) -> bool:
        """
        Check if the device is closed.

        Returns:
            bool: True if the device is closed; otherwise, False.
        """
        return not self._serial.is_open()

    def is_night(self) -> bool:
        """
        Determine if it is currently night at the device's location.

        Returns:
            bool: True if it is night, False otherwise.
        """
        # It is considered night if the Sun is more than 6 degrees below the horizon:
        return is_night(
            date=datetime.now(timezone.utc),
            observer=GeographicCoordinate(lat=self._latitude, lon=self._longitude),
            horizon=-6,
        )

    def get_status(self) -> BoltwoodIIIConditionsMonitorDeviceStatus:
        """
        Retrieve the current status of the device.

        Returns:
            BoltwoodIIIConditionsMonitorDeviceStatus: The current status of the device.
        """
        return self._read_all_parameters()

    def get_atmospheric_dew_point(self) -> float:
        """
        Retrieve the current atmospheric dew point reading from the device, if available.

        Returns:
            float: The current atmospheric dew point reading (in degrees Celsius).
        """
        return self._read_float_parameter("OC", "dewpoint")

    def get_cloud_coverage(self) -> float:
        """
        Retrieve the current cloud coverage reading from the device, if available.

        Higher values indicate more cloud cover, while lower values indicate clearer skies.

        Values are typically expressed as a percentage, where 0% indicates no clouds and 100%
        indicates completely overcast conditions.

        Returns:
            float: The current cloud coverage reading (as a percentage).
        """
        return self._read_float_parameter("OC", "cloudcover")

    def get_full_width_half_maximum(self) -> List[float]:
        """
        Retrieve the current full width at half maximum (FWHM) reading from the device, if available.

        Returns:
            List[float]: The current FWHM reading (in arcseconds) for each axis.
        """
        raise NotImplementedError(
            "get_full_width_half_maximum() method must be implemented."
        )

    def get_half_flux_diameter(self) -> List[float]:
        """
        Retrieve the current half flux diameter (HFD) reading from the device, if available.

        Returns:
            List[float]: The current HFD reading (in arcseconds) for each axis.
        """
        fwhm = self.get_full_width_half_maximum()

        # Return the approximated HFD value (HFD ≈ 2 * FWHM) for each axis, assuming
        # ideal seeing conditions (e.g., a purely Gaussian profile for each star is an
        # accurate model):
        return [2 * fwhm[0], 2 * fwhm[1]]

    def get_humidity(self) -> float:
        """
        Retrieve the current humidity reading from the device.

        Returns:
            float: The current humidity reading (as a percentage).
        """
        return self._read_float_parameter("OC", "humidity")

    def get_precipitation_rate(self) -> float:
        """
        Retrieve the current precipitation rate reading from the device, if available.

        Returns:
            float: The current precipitation rate reading (in millimeters per hour).
        """
        return self._read_float_parameter("OC", "rainrate")

    def get_pressure(self) -> float:
        """
        Retrieve the current atmospheric pressure reading from the device, if available.

        Returns:
            float: The current atmospheric pressure reading (in Pa).
        """
        return self._read_float_parameter("OC", "pressure") * 100.0

    def get_sky_brightness(self) -> float:
        """
        Retrieve the current sky brightness reading from the device, if available.

        Returns:
            float: The current sky brightness reading (in lux, e.g., luminous flux per unit area).
        """
        return self._read_float_parameter("OC", "skybrightness")

    def get_sky_temperature(self) -> float:
        """
        Retrieve the current sky temperature reading from the device, if available.

        Returns:
            float: The current sky temperature reading (in degrees Celsius).
        """
        return self._read_float_parameter("OC", "skytemperature")

    def get_sky_quality(self) -> float:
        """
        Retrieve the current sky quality reading from the device, if available.

        Returns:
            float: The current sky quality reading (as a percentage).
        """
        try:
            return self._read_float_parameter("OC", "skyquality")
        except Exception as e:
            warning(e)
            # If the sky quality is not available, return -inf:
            return -inf

    def get_temperature(self) -> float:
        """
        Retrieve the current temperature reading from the device.

        Returns:
            float: The current temperature reading (in degrees Celsius).
        """
        return self._read_float_parameter("OC", "temperature")

    def get_wind_direction(self) -> float:
        """
        Retrieve the current wind direction reading from the device.

        Returns:
            float: The current wind direction reading (in degrees), where 0° indicates
            a wind blowing from the North, 90° indicates a wind blowing from the East,
            and so on.
        """
        try:
            return self._read_float_parameter("OC", "winddirection")
        except Exception as e:
            warning(e)
            # If the wind direction is not available, return -inf:
            return -inf

    def get_wind_gust(self) -> float:
        """
        Retrieve the current wind gust reading from the device.

        Returns:
            float: The current wind gust reading (in meters per second).
        """
        try:
            return self._read_float_parameter("OC", "windgust")
        except Exception as e:
            warning(e)
            # If the wind gust is not available, return -inf:
            return -inf

    def get_wind_speed(self) -> float:
        """
        Retrieve the current wind speed reading from the device.

        Returns:
            float: The current wind speed reading (in meters per second).
        """
        return self._read_float_parameter("OC", "windspeed")

    def get_last_polling_time(self) -> datetime:
        """
        Retrieve the last time the device was polled for data.

        Returns:
            Optional[datetime]: The last polling time (in UTC).

        Notes:
            Defaults to the date at the UNIX epoch.
        """
        last_polling_timestamp = self._read_float_parameter("OC", "timesincelastupdate")

        # If we have a valid timestamp, return it:
        if last_polling_timestamp != inf:
            return datetime.fromtimestamp(last_polling_timestamp, tz=timezone.utc)

        # Otherwise, return the last polling time:
        return self._last_polling_time

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
                f"[Conditions Monitor ID {self.id}]: Device is not connected."
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
                f"[Conditions Monitor ID {self.id}]: Error refreshing device: {response}"
            )

        # If the refresh was successful, update the last polling time:
        self._last_polling_time = at


# **************************************************************************************
