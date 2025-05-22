# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone

from pydantic import ValidationError

from boltwood.status import (
    BoltwoodIIIConditionsMonitorDeviceStatus,
    BoltwoodIIISafetyMonitorDeviceStatus,
)

# **************************************************************************************


class TestBoltwoodIIIConditionsMonitorDeviceStatus(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(tz=timezone.utc)

    def test_all_numeric_strings(self):
        data = {
            "utc": self.now,
            "atmospheric_dew_point": "10.5",
            "cloud_coverage": "50",
            "humidity": "55.5",
            "pressure": "1013.2",
            "precipitation_rate": "0.1",
            "sky_brightness": "100",
            "sky_quality": "5.0",
            "sky_temperature": "15.2",
            "star_full_width_half_maximum": "2.3",
            "temperature": "20.0",
            "wind_direction": "180",
            "wind_gust": "4.5",
            "wind_speed": "3.2",
        }
        status = BoltwoodIIIConditionsMonitorDeviceStatus(**data)
        self.assertEqual(status.atmospheric_dew_point, 10.5)
        self.assertEqual(status.cloud_coverage, 50.0)
        self.assertEqual(status.humidity, 55.5)
        self.assertEqual(status.pressure, 1013.2)
        self.assertEqual(status.precipitation_rate, 0.1)
        self.assertEqual(status.sky_brightness, 100.0)
        self.assertEqual(status.sky_quality, 5.0)
        self.assertEqual(status.sky_temperature, 15.2)
        self.assertEqual(status.star_full_width_half_maximum, 2.3)
        self.assertEqual(status.temperature, 20.0)
        self.assertEqual(status.wind_direction, 180.0)
        self.assertEqual(status.wind_gust, 4.5)
        self.assertEqual(status.wind_speed, 3.2)

    def test_na_strings_become_none(self):
        data = {
            field: "NA"
            for field in [
                "atmospheric_dew_point",
                "cloud_coverage",
                "humidity",
                "pressure",
                "precipitation_rate",
                "sky_brightness",
                "sky_quality",
                "sky_temperature",
                "star_full_width_half_maximum",
                "temperature",
                "wind_direction",
                "wind_gust",
                "wind_speed",
            ]
        }
        data["utc"] = self.now
        status = BoltwoodIIIConditionsMonitorDeviceStatus(**data)
        for field in data:
            if field == "utc":
                continue
            self.assertIsNone(getattr(status, field), f"{field} should be None")

    def test_invalid_string_raises(self):
        data = {
            "utc": self.now,
            "atmospheric_dew_point": "not_a_number",
            "cloud_coverage": "50",
            "humidity": "55",
            "pressure": "1013",
            "precipitation_rate": "0.1",
            "sky_brightness": "100",
            "sky_quality": "5",
            "sky_temperature": "15",
            "star_full_width_half_maximum": "2.3",
            "temperature": "20",
            "wind_direction": "180",
            "wind_gust": "4.5",
            "wind_speed": "3.2",
        }
        with self.assertRaises(ValidationError):
            BoltwoodIIIConditionsMonitorDeviceStatus(**data)


# **************************************************************************************


class TestBoltwoodIIISafetyMonitorDeviceStatus(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(tz=timezone.utc)

    def test_boolean_values(self):
        for value in (True, False):
            data = {
                "utc": self.now,
                "is_safe": value,
            }
            status = BoltwoodIIISafetyMonitorDeviceStatus(**data)
            self.assertIs(status.is_safe, value)

    def test_string_truthy_boolean(self):
        data = {
            "utc": self.now,
            "is_safe": "1",
        }
        status = BoltwoodIIISafetyMonitorDeviceStatus(**data)
        self.assertTrue(status.is_safe)

    def test_string_falsy_boolean(self):
        data = {
            "utc": self.now,
            "is_safe": "0",
        }
        status = BoltwoodIIISafetyMonitorDeviceStatus(**data)
        self.assertFalse(status.is_safe)

    def test_string_other_boolean(self):
        data = {
            "utc": self.now,
            "is_safe": "TRUE",
        }
        status = BoltwoodIIISafetyMonitorDeviceStatus(**data)
        self.assertFalse(status.is_safe)

    def test_invalid_string_is_always_false(self):
        data = {
            "utc": self.now,
            "is_safe": "not_a_bool",
        }
        status = BoltwoodIIISafetyMonitorDeviceStatus(**data)
        self.assertFalse(status.is_safe)

    def test_na_string_becomes_none(self):
        data = {
            "utc": self.now,
            "is_safe": "NA",
        }
        status = BoltwoodIIISafetyMonitorDeviceStatus(**data)
        self.assertIsNone(status.is_safe)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
