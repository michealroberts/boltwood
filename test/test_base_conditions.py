# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone
from typing import List, Tuple

from boltwood.base_conditions import (
    BaseConditionsMonitorDeviceInterface,
    BaseConditionsMonitorDeviceParameters,
)

# **************************************************************************************


class DummyConditionsMonitorDeviceInterface(BaseConditionsMonitorDeviceInterface):
    """
    Dummy implementation of BaseConditionsMonitorDeviceInterface for testing.

    It provides fixed return values for each of the abstract methods and properties.
    """

    def __init__(self, id: int, params: BaseConditionsMonitorDeviceParameters) -> None:
        super().__init__(id, params)
        # Initialize some attributes to verify that methods have been called.
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
        return "Dummy Device"

    def get_description(self) -> str:
        return "Dummy description"

    def get_driver_version(self) -> Tuple[int, int, int]:
        return (1, 0, 0)

    def get_firmware_version(self) -> Tuple[int, int, int]:
        return (1, 0, 1)

    def connect(self, timeout: float = 5.0, retries: int = 3) -> None:
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False

    def get_capabilities(self) -> List[str]:
        return ["capability 1", "capability 2"]

    def get_atmospheric_dew_point(self) -> float:
        return 1.1

    def get_cloud_coverage(self) -> float:
        return 22.2

    def get_humidity(self) -> float:
        return 33.3

    def get_full_width_half_maximum(self) -> list[float]:
        return [1.0, 2.0]

    def get_half_flux_diameter(self) -> list[float]:
        # Explicitly compute the half flux diameter as 2×FWHM
        return [2 * fwhm for fwhm in self.get_full_width_half_maximum()]

    def get_precipitation_rate(self) -> float:
        return 4.4

    def get_pressure(self) -> float:
        return 101300.0

    def get_sky_brightness(self) -> float:
        return 55.5

    def get_sky_temperature(self) -> float:
        return -5.5

    def get_sky_quality(self):
        return 0.8

    def get_temperature(self) -> float:
        return 12.3

    def get_wind_direction(self) -> float:
        return 180.0

    def get_wind_speed(self) -> float:
        return 6.6

    def get_wind_gust(self) -> float:
        return 7.7

    def get_last_polling_time(self) -> datetime:
        return datetime(2025, 1, 2, 3, 4, 5, tzinfo=timezone.utc)

    def refresh(self) -> None:
        # no-op
        pass


# **************************************************************************************


class TestBaseConditionsMonitorDeviceInterface(unittest.TestCase):
    def setUp(self) -> None:
        params: BaseConditionsMonitorDeviceParameters = (
            BaseConditionsMonitorDeviceParameters(
                {
                    "did": "ddid",
                    "vid": "dvid",
                    "pid": "dpid",
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "elevation": 0.0,
                }
            )
        )

        self.device = DummyConditionsMonitorDeviceInterface(id=0, params=params)

    def test_is_night_method_exists_and_returns_bool(self) -> None:
        """Test that is_night method exists and returns a boolean."""
        self.assertTrue(hasattr(self.device, "is_night"), "Missing is_night method")
        result = self.device.is_night()
        self.assertIsInstance(result, bool)

    def test_get_atmospheric_dew_point(self) -> None:
        """Test that get_atmospheric_dew_point exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_atmospheric_dew_point"),
            "Missing get_atmospheric_dew_point method",
        )
        self.assertEqual(self.device.get_atmospheric_dew_point(), 1.1)

    def test_get_cloud_coverage(self) -> None:
        """Test that get_cloud_coverage exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_cloud_coverage"),
            "Missing get_cloud_coverage method",
        )
        self.assertEqual(self.device.get_cloud_coverage(), 22.2)

    def test_get_humidity(self) -> None:
        """Test that get_humidity exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_humidity"), "Missing get_humidity method"
        )
        self.assertEqual(self.device.get_humidity(), 33.3)

    def test_get_full_width_half_maximum(self) -> None:
        """Test that get_full_width_half_maximum exists and returns correct list."""
        self.assertTrue(
            hasattr(self.device, "get_full_width_half_maximum"),
            "Missing get_full_width_half_maximum method",
        )
        self.assertEqual(self.device.get_full_width_half_maximum(), [1.0, 2.0])

    def test_get_half_flux_diameter(self) -> None:
        """Test that get_half_flux_diameter exists and doubles the FWHM values."""
        self.assertTrue(
            hasattr(self.device, "get_half_flux_diameter"),
            "Missing get_half_flux_diameter method",
        )
        fwhm = self.device.get_full_width_half_maximum()
        self.assertEqual(
            self.device.get_half_flux_diameter(),
            [2 * fwhm[0], 2 * fwhm[1]],
        )

    def test_get_precipitation_rate(self) -> None:
        """Test that get_precipitation_rate exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_precipitation_rate"),
            "Missing get_precipitation_rate method",
        )
        self.assertEqual(self.device.get_precipitation_rate(), 4.4)

    def test_get_pressure(self) -> None:
        """Test that get_pressure exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_pressure"), "Missing get_pressure method"
        )
        self.assertEqual(self.device.get_pressure(), 101300.0)

    def test_get_sky_brightness(self) -> None:
        """Test that get_sky_brightness exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_sky_brightness"),
            "Missing get_sky_brightness method",
        )
        self.assertEqual(self.device.get_sky_brightness(), 55.5)

    def test_get_sky_temperature(self) -> None:
        """Test that get_sky_temperature exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_sky_temperature"),
            "Missing get_sky_temperature method",
        )
        self.assertEqual(self.device.get_sky_temperature(), -5.5)

    def test_get_sky_quality(self) -> None:
        """Test that get_sky_quality exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_sky_quality"),
            "Missing get_sky_quality method",
        )
        self.assertEqual(self.device.get_sky_quality(), 0.8)

    def test_get_temperature(self) -> None:
        """Test that get_temperature exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_temperature"), "Missing get_temperature method"
        )
        self.assertEqual(self.device.get_temperature(), 12.3)

    def test_get_wind_direction(self) -> None:
        """Test that get_wind_direction exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_wind_direction"),
            "Missing get_wind_direction method",
        )
        self.assertEqual(self.device.get_wind_direction(), 180.0)

    def test_get_wind_speed(self) -> None:
        """Test that get_wind_speed exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_wind_speed"), "Missing get_wind_speed method"
        )
        self.assertEqual(self.device.get_wind_speed(), 6.6)

    def test_get_wind_gust(self) -> None:
        """Test that get_wind_gust exists and returns correct value."""
        self.assertTrue(
            hasattr(self.device, "get_wind_gust"), "Missing get_wind_gust method"
        )
        self.assertEqual(self.device.get_wind_gust(), 7.7)

    def test_get_last_polling_time(self) -> None:
        """Test that get_last_polling_time exists and returns correct datetime."""
        self.assertTrue(
            hasattr(self.device, "get_last_polling_time"),
            "Missing get_last_polling_time method",
        )
        expected = datetime(2025, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        self.assertEqual(self.device.get_last_polling_time(), expected)

    def test_refresh_method_exists_and_no_error(self) -> None:
        """Test that refresh exists and does not raise."""
        self.assertTrue(hasattr(self.device, "refresh"), "Missing refresh method")
        try:
            self.device.refresh()
        except Exception as e:
            self.fail(f"refresh() raised an exception: {e}")


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
