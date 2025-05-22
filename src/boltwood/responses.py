# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from re import compile

# **************************************************************************************

# Regex pattern for "G OC all" response: 1 status + 14 values (NA or number):
PATTERN_OBSERVING_CONDITIONS_ALL_RESPONSE = compile(
    r"^"
    r"(?P<status>[0-2])"  # status code 0,1,2
    r"(?:\s+(?P<average_period>NA|\d+\.?\d*))"
    r"(?:\s+(?P<cloud_coverage>NA|\d+\.?\d*))"
    r"(?:\s+(?P<atmospheric_dew_point>NA|\d+\.?\d*))"
    r"(?:\s+(?P<humidity>NA|\d+\.?\d*))"
    r"(?:\s+(?P<pressure>NA|\d+\.?\d*))"
    r"(?:\s+(?P<precipitation_rate>NA|\d+\.?\d*))"
    r"(?:\s+(?P<sky_brightness>NA|\d+\.?\d*))"
    r"(?:\s+(?P<sky_quality>NA|\d+\.?\d*))"
    r"(?:\s+(?P<sky_temperature>NA|\d+\.?\d*))"
    r"(?:\s+(?P<star_full_width_half_maximum>NA|\d+\.?\d*))"
    r"(?:\s+(?P<temperature>NA|\d+\.?\d*))"
    r"(?:\s+(?P<wind_direction>NA|\d+\.?\d*))"
    r"(?:\s+(?P<wind_gust>NA|\d+\.?\d*))"
    r"(?:\s+(?P<wind_speed>NA|\d+\.?\d*))"
    r"$"
)

# **************************************************************************************

# Regex pattern for "G SM all" response: 1 status + 1 values (NA or boolean):
PATTERN_SAFETY_MONITOR_ALL_RESPONSE = compile(
    r"^"
    r"(?P<status>[0-2])"  # status code 0,1,2
    r"(?:\s+(?P<is_safe>NA|0|1))"
    r"$"
)

# **************************************************************************************
