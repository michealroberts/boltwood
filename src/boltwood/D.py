# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import Literal, TypedDict

# **************************************************************************************


class BoltwoodSensorReportSentence(TypedDict):
    # Code indicating humidity and ambient temperature sensor status:
    humidity_and_ambient_temperature_code: Literal[0, 1, 2, 3, 4, 5, 6]

    # Cloud coverage condition:
    cloud_condition: Literal["Unknown", "Clear", "Cloudy", "Very Cloudy"]

    # Wind condition:
    wind_condition: Literal["Unknown", "Calm", "Windy", "Very Windy"]

    # Precipitation condition:
    precipitation_condition: Literal[
        "Unknown", "Not Raining", "Recently Raining", "Raining"
    ]

    # Sky coverage condition:
    sky_condition: Literal["Unknown", "Clear", "Cloudy", "Very Cloudy", "Wet"]

    # Flag indicating a roof close request this cycle (0 or 1 as boolean):
    roof_close_requested: bool

    # Difference between sky target and ambient temperature (in °C):
    sky_minus_ambient_temperature: float

    # Ambient air temperature (in °C):
    ambient_temperature: float

    # Wind speed (in m/s):
    wind_speed: float

    # Wet sensor status:
    wet_sensor_status: Literal["Dry", "Wet", "Recently Wet"]

    # Rain sensor status:
    rain_sensor_status: Literal["Not Raining", "Raining", "Was Raining"]

    # Relative humidity percentage (0–100):
    relative_humidity_percentage: int

    # Atmospheric dew point temperature (in °C):
    dew_point_temperature: float

    # Thermopile case temperature (in °C):
    case_temperature: float

    # Rain heater duty cycle as a percentage (0–100%):
    rain_heater_percentage: int

    # Calibration blackbody reference temperature (in °C):
    blackbody_temperature: float

    # Rain heater operational state code (0–7):
    rain_heater_state: Literal[0, 1, 2, 3, 4, 5, 6, 7]

    # Supply voltage at the sensor head (in V) (e.g., typically 24V):
    power_voltage: float

    # Temperature difference at anemometer tip (in °C):
    anemometer_temperature_difference: float

    # Maximum drop in wetness oscillator counts this cycle:
    wetness_drop: int

    # Average difference of wetness oscillator counts from dry baseline:
    wetness_average_difference: int

    # Dry difference of wetness oscillator counts from baseline:
    wetness_dry_difference: int

    # Rain heater PWM register value:
    rain_heater_pwm: int

    # Anemometer heater PWM register value:
    anemometer_heater_pwm: int

    # Raw thermopile ADC digital reading:
    thermopile_adc: int

    # Raw thermistor ADC digital reading:
    thermistor_adc: int

    # Raw main power ADC digital reading:
    power_adc: int

    # Raw calibration block ADC digital reading:
    block_adc: int

    # Raw anemometer tip thermistor ADC reading:
    anemometer_thermistor_adc: int

    # Raw Davis vane ADC digital reading:
    davis_vane_adc: int

    # External anemometer speed in sensor-specific units:
    external_anemometer_speed: float

    # External anemometer direction in ° (0–359):
    external_anemometer_direction: int

    # Raw wetness oscillator count for this cycle:
    raw_wetness_oscillator_counts: int

    # Day conditions status
    day_conditions: Literal["Unknown", "Night", "Twilight", "Day"]

    # Daylight photodiode ADC digital reading, in range 0–1023:
    daylight_adc: int


# **************************************************************************************
