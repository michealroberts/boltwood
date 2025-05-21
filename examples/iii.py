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
            id=0,
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

    monitor = BoltwoodIIIConditionsMonitorDeviceInterface(params)

    try:
        monitor.initialise()

        status = monitor.get_status()

        print(status)

        print("[Connected]:", monitor.is_connected())
    except asyncio.CancelledError:
        print("Operation was cancelled.")
    except KeyboardInterrupt:
        print("Keyboard interrupt received during execution. Exiting gracefully.")
    finally:
        monitor.disconnect()


# **************************************************************************************

if __name__ == "__main__":
    parser = ArgumentParser(description="Run GNSSRTC GPS")

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
