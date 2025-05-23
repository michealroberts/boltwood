# **************************************************************************************

# @package        boltwood
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import asyncio
from argparse import ArgumentParser
from typing import cast

from samps import BaudrateType

from boltwood import (
    BoltwoodIIISafetyMonitorDeviceInterface,
    BoltwoodIIISafetyMonitorDeviceParameters,
)

# **************************************************************************************


async def main(port: str, baudrate: BaudrateType = 9600) -> None:
    params: BoltwoodIIISafetyMonitorDeviceParameters = (
        BoltwoodIIISafetyMonitorDeviceParameters(
            name="",
            description="",
            port=port,
            baudrate=baudrate,
            did="0",
            vid="",
            pid="",
        )
    )

    safety = BoltwoodIIISafetyMonitorDeviceInterface(id=0, params=params)

    try:
        safety.initialise()

        print("[Connected]:", safety.is_connected())

        print("[Serial Number]", safety.get_serial_number())

        print("[Firmware Version]", safety.get_firmware_version())

        print("[Description]", safety.get_description())

        print("[Is Safe]:", safety.is_safe())
    except asyncio.CancelledError:
        print("Operation was cancelled.")
    except KeyboardInterrupt:
        print("Keyboard interrupt received during execution. Exiting gracefully.")
    finally:
        safety.disconnect()


# **************************************************************************************

if __name__ == "__main__":
    parser = ArgumentParser(description="Run Boltwood III Safety Monitor")

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
