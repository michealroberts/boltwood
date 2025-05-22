# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from boltwood.responses import (
    PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE,
    PATTERN_SAFETY_MONITOR_ALL_RESPONSE,
)

# **************************************************************************************


class TestPatternObservingConditionsAllResponse(unittest.TestCase):
    def test_full_numeric(self):
        raw = "0 5 50 10.5 55.5 1013.2 0.1 100 5.0 15.2 2.3 20.0 180 4.5 3.2"
        m = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match a fully numeric response")
        gd = m.groupdict()

        expected = {
            "status": "0",
            "average_period": "5",
            "cloud_coverage": "50",
            "atmospheric_dew_point": "10.5",
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

        for key, expected in expected.items():
            self.assertEqual(
                gd[key],
                expected,
                msg=f"Group '{key}' expected {expected} but got {gd[key]}",
            )

    def test_numeric_with_not_any(self):
        raw = "0 NA 0 NA 42.21 NA 0 NA NA 27.37 NA 27.77 NA 0 0"
        m = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match response containing 'NA'")

        self.assertEqual(m.group("average_period"), "NA")
        self.assertEqual(m.group("cloud_coverage"), "0")
        self.assertEqual(m.group("atmospheric_dew_point"), "NA")
        self.assertEqual(m.group("humidity"), "42.21")
        self.assertEqual(m.group("sky_quality"), "NA")
        self.assertEqual(m.group("star_full_width_half_maximum"), "NA")
        self.assertEqual(m.group("wind_speed"), "0")

    def test_status_client_error(self):
        # Pattern should match but capture status '1' when device returns an error code:
        raw = "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
        m = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match a response with status 1")
        self.assertEqual(
            m.group("status"),
            "1",
            msg=f"Expected status '1' but got '{m.group('status')}'",
        )

    def test_status_server_error(self):
        # Pattern should match but capture status '2' when device returns an error code:
        raw = "2 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
        m = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match a response with status 2")
        self.assertEqual(
            m.group("status"),
            "2",
            msg=f"Expected status '2' but got '{m.group('status')}'",
        )

    def test_invalid_format(self):
        raw = "I 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
        m = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(raw)
        self.assertIsNone(m, msg="Pattern should not match an invalid response")

    def test_negative_values(self):
        # Negative numbers are not supported by the regex, so this should not match:
        raw = "0 -5 50 10 50 1000 1 100 5 15 2 20 180 4 3"
        m = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(raw)
        self.assertIsNone(m, msg="Pattern should not match negative numeric values")

    def test_excess_tokens(self):
        # Too many fields (16 instead of 15) should fail to match:
        raw = "0 5 50 10.5 55.5 1013.2 0.1 100 5.0 15.2 2.3 20.0 180 4.5 3.2 99"
        m = PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE.match(raw)
        self.assertIsNone(m, msg="Pattern should not match when there are extra tokens")


# **************************************************************************************


class TestPatternSafetyMonitorAllResponse(unittest.TestCase):
    def test_full_boolean_safe(self):
        raw = "0 1"
        m = PATTERN_SAFETY_MONITOR_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match a fully numeric response")
        gd = m.groupdict()

        expected = {"status": "0", "is_safe": "1"}

        for key, expected in expected.items():
            self.assertEqual(
                gd[key],
                expected,
                msg=f"Group '{key}' expected {expected} but got {gd[key]}",
            )

    def test_full_boolean_unsafe(self):
        raw = "0 0"
        m = PATTERN_SAFETY_MONITOR_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match a fully numeric response")
        gd = m.groupdict()

        expected = {"status": "0", "is_safe": "0"}

        for key, expected in expected.items():
            self.assertEqual(
                gd[key],
                expected,
                msg=f"Group '{key}' expected {expected} but got {gd[key]}",
            )

    def test_status_client_error(self):
        # Pattern should match but capture status '1' when device returns an error code:
        raw = "1 0"
        m = PATTERN_SAFETY_MONITOR_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match a response with status 1")
        self.assertEqual(
            m.group("status"),
            "1",
            msg=f"Expected status '1' but got '{m.group('status')}'",
        )

    def test_status_server_error(self):
        # Pattern should match but capture status '2' when device returns an error code:
        raw = "2 0"
        m = PATTERN_SAFETY_MONITOR_ALL_RESPONSE.match(raw)
        self.assertIsNotNone(m, msg="Pattern did not match a response with status 2")
        self.assertEqual(
            m.group("status"),
            "2",
            msg=f"Expected status '2' but got '{m.group('status')}'",
        )

    def test_invalid_format(self):
        raw = "I 0"
        m = PATTERN_SAFETY_MONITOR_ALL_RESPONSE.match(raw)
        self.assertIsNone(m, msg="Pattern should not match an invalid response")

    def test_excess_tokens(self):
        # Too many fields (3 instead of 2) should fail to match:
        raw = "0 1 99"
        m = PATTERN_SAFETY_MONITOR_ALL_RESPONSE.match(raw)
        self.assertIsNone(m, msg="Pattern should not match when there are extra tokens")


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
