# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator

# **************************************************************************************


class BoltwoodIIIConditionsMonitorDeviceStatus(BaseModel):
    """
    Represents the status of a Boltwood II conditions monitor device.
    """

    # The last current date and time received from the device (in UTC):
    utc: datetime = Field(..., description="The current date and time.")

    # Atmospheric dew point in degrees Celsius, or None if not supported:
    atmospheric_dew_point: Optional[float] = Field(
        None, description="Atmospheric dew point (°C)"
    )

    # Cloud cover percentage (0–100), or None if not supported:
    cloud_coverage: Optional[float] = Field(None, description="Cloud cover percentage")

    # Relative humidity as a percentage, or None if not supported:
    humidity: Optional[float] = Field(None, description="Relative humidity (%)")

    # Atmospheric pressure in hectopascals (hPa), or None if not supported:
    pressure: Optional[float] = Field(None, description="Atmospheric pressure (hPa)")

    # Rain rate in millimeters per hour, or None if not supported:
    precipitation_rate: Optional[float] = Field(None, description="Rain rate (mm/hr)")

    # Sky brightness in lux, or None if not supported:
    sky_brightness: Optional[float] = Field(None, description="Sky brightness (lux)")

    # Sky quality index, or None if not supported:
    sky_quality: Optional[float] = Field(None, description="Sky quality index")

    # Sky temperature in degrees Celsius, or None if not supported:
    sky_temperature: Optional[float] = Field(None, description="Sky temperature (°C)")

    # Star full width at half maximum in arcseconds, or None if not supported:
    star_full_width_half_maximum: Optional[float] = Field(
        None, description="Star FWHM (in arcsec)"
    )

    # Ambient temperature in degrees Celsius, or None if not supported:
    temperature: Optional[float] = Field(None, description="Ambient temperature (°C)")

    # Wind direction in degrees (0° = north), or None if not supported:
    wind_direction: Optional[float] = Field(None, description="Wind direction (°)")

    # Peak wind gust in meters per second, or None if not supported:
    wind_gust: Optional[float] = Field(None, description="Peak wind gust (m/s)")

    # Current wind speed in meters per second, or None if not supported:
    wind_speed: Optional[float] = Field(None, description="Wind speed (m/s)")

    @model_validator(mode="before")
    def _coerce_na_and_str_numbers(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        For every field except 'utc', if the incoming value is the string "NA" set it to None;
        otherwise if it's a string, try to convert it to float.
        """
        for key, val in list(values.items()):
            if key == "utc" or val is None:
                continue

            # Coerce literal "NA" to None
            if isinstance(val, str) and val.strip().upper() == "NA":
                values[key] = None
                continue

            # Coerce numeric strings to float
            if isinstance(val, str):
                try:
                    values[key] = float(val)
                except ValueError:
                    # leave it to pydantic to catch invalid types
                    pass

        return values


# **************************************************************************************


class BoltwoodIIISafetyMonitorDeviceStatus(BaseModel):
    """
    Represents the status of a Boltwood III safety monitor device.
    """

    # The last current date and time received from the device (in UTC):
    utc: datetime = Field(..., description="The current date and time.")

    # The current safety state of the system:
    is_safe: Optional[bool] = Field(None, description="Safety state of the system.")

    @model_validator(mode="before")
    def _coerce_na_and_str_numbers(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        For every field except 'utc', if the incoming value is the string "NA" set it
        to None.

        If the value is a numeric-like string ("1"/"0"), convert it to a boolean.
        """
        for key, val in list(values.items()):
            if key == "utc" or val is None:
                continue

            # Coerce literal "NA" to None
            if isinstance(val, str) and val.strip().upper() == "NA":
                values[key] = None
                continue

            # Coerce boolean strings to boolean
            if isinstance(val, str):
                values[key] = val.strip().lower() == "1"

        return values


# **************************************************************************************
