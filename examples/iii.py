# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import asyncio
from argparse import ArgumentParser
from typing import cast

from samps import BaudrateType

from boltwood import (
    BoltwoodIIIConditionsMonitorDeviceInterface,
    BoltwoodIIIConditionsMonitorDeviceParameters,
)

# **************************************************************************************


async def main(port: str, baudrate: BaudrateType = 9600) -> None:
    params: BoltwoodIIIConditionsMonitorDeviceParameters = (
        BoltwoodIIIConditionsMonitorDeviceParameters(
            name="",
            description="",
            port=port,
            baudrate=baudrate,
            latitude=33.87047,
            longitude=-118.24708,
            elevation=0.0,
            did="0",
            vid="",
            pid="",
        )
    )

    monitor = BoltwoodIIIConditionsMonitorDeviceInterface(id=0, params=params)

    try:
        monitor.initialise()

        status = monitor.get_status()

        print(status)

        print("[Connected]:", monitor.is_connected())

        print("[Serial Number]", monitor.get_serial_number())

        print("[Firmware Version]", monitor.get_firmware_version())

        print("[Description]", monitor.get_description())

        monitor.refresh()

        status = monitor.get_status()

        print(status)

        atmospheric_dew_point = monitor.get_atmospheric_dew_point()

        print("[Atmospheric Dew Point]:", atmospheric_dew_point)

        cloud_coverage = monitor.get_cloud_coverage()

        print("[Cloud Coverage]:", cloud_coverage)

        humidity = monitor.get_humidity()

        print("[Humidity]:", humidity)

        precipitation_rate = monitor.get_precipitation_rate()

        print("[Precipitation Rate]:", precipitation_rate)

        sky_brightness = monitor.get_sky_brightness()

        print("[Sky Brightness]:", sky_brightness)

        sky_quality = monitor.get_sky_quality()

        print("[Sky Quality]:", sky_quality)

        sky_temperature = monitor.get_sky_temperature()

        print("[Sky Temperature]:", sky_temperature)

        temperature = monitor.get_temperature()

        print("[Temperature]:", temperature)

        wind_direction = monitor.get_wind_direction()

        print("[Wind Direction]:", wind_direction)

        wind_gust = monitor.get_wind_gust()

        print("[Wind Gust]:", wind_gust)

        wind_speed = monitor.get_wind_speed()

        print("[Wind Speed]:", wind_speed)
    except asyncio.CancelledError:
        print("Operation was cancelled.")
    except KeyboardInterrupt:
        print("Keyboard interrupt received during execution. Exiting gracefully.")
    finally:
        monitor.disconnect()


# **************************************************************************************

if __name__ == "__main__":
    parser = ArgumentParser(description="Run Boltwood III Conditions Monitor")

    parser.add_argument(
        "--port",
        type=str,
        default="/dev/serial0",
        help='Serial port to use (default: "/dev/serial0")',
    )

    parser.add_argument(
        "--baudrate",
        type=int,
        default=9600,
        help="Baud rate for the serial connection (default: 9600)",
    )

    args = parser.parse_args()

    port = cast(str, args.port)

    baudrate = cast(BaudrateType, args.baudrate)

    try:
        asyncio.run(
            main(
                port=port,
                baudrate=baudrate,
            )
        )
    except KeyboardInterrupt:
        print("Program terminated by user via KeyboardInterrupt.")
    except Exception as e:
        print(f"An unexpected exception occurred: {e}")

# **************************************************************************************
