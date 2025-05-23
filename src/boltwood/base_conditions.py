# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from abc import abstractmethod
from datetime import datetime, timezone
from typing import List

from celerity.coordinates import GeographicCoordinate
from celerity.night import is_night

from .base import BaseDeviceInterface, BaseDeviceParameters

# **************************************************************************************


class BaseConditionsMonitorDeviceParameters(BaseDeviceParameters):
    # The latitude of the conditions monitor (in degrees):
    latitude: float
    # The longitude of the conditions monitor (in degrees):
    longitude: float
    # The elevation of the conditions monitor (in meters):
    elevation: float


# **************************************************************************************


class BaseConditionsMonitorDeviceInterface(BaseDeviceInterface):
    """
    Abstract class representing a generic conditions monitor device interface.

    This class extends the BaseDeviceInterface by adding methods and properties
    specific to conditions monitors, such as atmospheric readings, cloud coverage, etc.

    Subclasses should override these methods with the appropriate hardware-specific logic.
    """

    _id: int = 0

    # The latitude of the conditions monitor (in degrees):
    _latitude: float = 0.0

    # The longitude of the conditions monitor (in degrees):
    _longitude: float = 0.0

    # The elevation of the conditions monitor (in meters):
    _elevation: float = 0.0

    def __init__(
        self,
        id: int,
        params: BaseConditionsMonitorDeviceParameters,
    ) -> None:
        """
        Initialize the conditions monitor device with the given parameters.

        Args:
            params (BaseConditionsMonitorDeviceParameters): The parameters for the device.
        """
        # Set the identifier for the device:
        self._id = id

        # Set the site geographic coordinates (latitude, longitude, elevation) of the conditions monitor:
        self._latitude = params.get("latitude", 0.0)
        self._longitude = params.get("longitude", 0.0)
        self._elevation = params.get("elevation", 0.0)

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

    @abstractmethod
    def get_atmospheric_dew_point(self) -> float:
        """
        Retrieve the current atmospheric dew point reading from the device, if available.

        Returns:
            float: The current atmospheric dew point reading (in degrees Celsius).
        """
        raise NotImplementedError(
            "get_atmospheric_dew_point() method must be implemented."
        )

    @abstractmethod
    def get_cloud_coverage(self) -> float:
        """
        Retrieve the current cloud coverage reading from the device, if available.

        Higher values indicate more cloud cover, while lower values indicate clearer skies.

        Values are typically expressed as a percentage, where 0% indicates no clouds and 100%
        indicates completely overcast conditions.

        Returns:
            float: The current cloud coverage reading (as a percentage).
        """
        raise NotImplementedError("get_cloud_coverage() method must be implemented.")

    @abstractmethod
    def get_humidity(self) -> float:
        """
        Retrieve the current humidity reading from the device.

        Returns:
            float: The current humidity reading (as a percentage).
        """
        raise NotImplementedError("get_humidity() method must be implemented.")

    @abstractmethod
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

    @abstractmethod
    def get_precipitation_rate(self) -> float:
        """
        Retrieve the current precipitation rate reading from the device, if available.

        Returns:
            float: The current precipitation rate reading (in millimeters per hour).
        """
        raise NotImplementedError(
            "get_precipitation_rate() method must be implemented."
        )

    @abstractmethod
    def get_pressure(self) -> float:
        """
        Retrieve the current atmospheric pressure reading from the device, if available.

        Returns:
            float: The current atmospheric pressure reading (in Pa).
        """
        raise NotImplementedError("get_pressure() method must be implemented.")

    @abstractmethod
    def get_sky_brightness(self) -> float:
        """
        Retrieve the current sky brightness reading from the device, if available.

        Returns:
            float: The current sky brightness reading (in lux, e.g., luminous flux per unit area).
        """
        raise NotImplementedError("get_sky_brightness() method must be implemented.")

    @abstractmethod
    def get_sky_temperature(self) -> float:
        """
        Retrieve the current sky temperature reading from the device, if available.

        Returns:
            float: The current sky temperature reading (in degrees Celsius).
        """
        raise NotImplementedError("get_sky_temperature() method must be implemented.")

    @abstractmethod
    def get_sky_quality(self) -> float:
        """
        Retrieve the current sky quality reading from the device, if available.

        Returns:
            float: The current sky quality reading (dimensionless).
        """
        raise NotImplementedError("get_sky_quality() method must be implemented.")

    @abstractmethod
    def get_temperature(self) -> float:
        """
        Retrieve the current temperature reading from the device.

        Returns:
            float: The current temperature reading (in degrees Celsius).
        """
        raise NotImplementedError("get_temperature() method must be implemented.")

    @abstractmethod
    def get_wind_direction(self) -> float:
        """
        Retrieve the current wind direction reading from the device.

        Returns:
            float: The current wind direction reading (in degrees), where 0° indicates
            a wind blowing from the North, 90° indicates a wind blowing from the East,
            and so on.
        """
        raise NotImplementedError("get_wind_direction() method must be implemented.")

    @abstractmethod
    def get_wind_speed(self) -> float:
        """
        Retrieve the current wind speed reading from the device.

        Returns:
            float: The current wind speed reading (in meters per second).
        """
        raise NotImplementedError("get_wind_speed() method must be implemented.")

    @abstractmethod
    def get_wind_gust(self) -> float:
        """
        Retrieve the current wind gust reading from the device.

        Returns:
            float: The current wind gust reading (in meters per second).
        """
        raise NotImplementedError("get_wind_gust() method must be implemented.")

    @abstractmethod
    def get_last_polling_time(self) -> datetime:
        """
        Retrieve the last time the device was polled for data.

        Returns:
            datetime: The last polling time.
        """
        # In a true implementation, this method would return the actual last polling time
        # from the device itself:
        raise NotImplementedError("get_last_polling_time() method must be implemented.")

    @abstractmethod
    def refresh(self) -> None:
        """
        Refresh the device state.

        This method should implement any necessary operations to refresh the device state.
        """
        raise NotImplementedError("refresh() method must be implemented.")


# **************************************************************************************
