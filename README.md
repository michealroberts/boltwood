![pypi](https://img.shields.io/pypi/v/boltwood.svg)
![versions](https://img.shields.io/pypi/pyversions/boltwood.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![boltwood/test](https://github.com/michealroberts/boltwood/actions/workflows/test.yml/badge.svg)](https://github.com/michealroberts/boltwood/actions/workflows/test.yml)

# Boltwood

Modern, type-safe, zero-dependency python library for controlling the Boltwood III observing conditions sensor.

## Installation

```bash
uv add boltwood
```

or

using your preferred environment / package manager of choice, e.g., `poetry`, `conda` or `pip`:

```bash
pip install boltwood
```

```bash
poetry add boltwood
```

```bash
conda install boltwood
```

## Usage

To use the conditions monitor, you need to create an instance of the `BoltwoodIIIConditionsMonitorDeviceInterface` class with the appropriate parameters. 

Below is a simple example of how to set up and use the Boltwood III Conditions Monitor:

```python
from boltwood import (
    BoltwoodIIIConditionsMonitorDeviceInterface,
    BoltwoodIIIConditionsMonitorDeviceParameters,
)

# Define the parameters for the BoltwoodIII monitor device:
params: BoltwoodIIIConditionsMonitorDeviceParameters = BoltwoodIIIConditionsMonitorDeviceParameters(
    name="Boltwood III Conditions Monitor",
    description="Boltwood III Conditions Monitor",
    port="/dev/ttyUSB0",  # Replace with your actual port
    baudrate=9600,
    latitude=33.87047,
    longitude=-118.24708,
    elevation=0.0,
    did="0", # Device ID
    vid="067b",  # Vendor ID
    pid="23a3",  # Product ID
)

# Create a new Boltwood III Conditions Monitor device interface:
monitor = BoltwoodIIIConditionsMonitorDeviceInterface(
    id=0,
    params=params,
)

# Initialise the monitor:
monitor.initialise()

# Get the current status of the monitor:
status = monitor.get_status()

...
```

To use the safety monitor, you can create an instance of the `BoltwoodIIISafetyMonitorDeviceInterface` class in a similar way:

```python
from boltwood import (
    BoltwoodIIISafetyMonitorDeviceInterface,
    BoltwoodIIISafetyMonitorDeviceParameters,
)

# Define the parameters for the BoltwoodIII safety monitor device:
params: BoltwoodIIISafetyMonitorDeviceParameters = BoltwoodIIISafetyMonitorDeviceParameters(
    name="Boltwood III Safety Monitor",
    description="Boltwood III Safety Monitor",
    port="/dev/ttyUSB0",  # Replace with your actual port
    baudrate=9600,
    did="0", # Device ID
    vid="067b",  # Vendor ID
    pid="23a3",  # Product ID
)

# Create a new Boltwood III Safety Monitor device interface:
safety_monitor = BoltwoodIIISafetyMonitorDeviceInterface(
    id=0,
    params=params,
)

# Initialise the safety monitor:
safety_monitor.initialise()

# Get the current status of the safety monitor:
status = safety_monitor.get_status()

...
```

As the boltwood instance is fully typed, you can use your IDE's autocompletion to see all the available methods and properties.

We have also provided further usage examples in the [examples](./examples) directory.

## Milestones

- [X] Type-safe modern 3.6+ Python
- [X] Fully unit tested
- [X] Simpler API (modelled around the ASCOM Alpaca API)
- [X] Integration testing with HIL testing (hardware-in-the-loop)
- [X] Zero-external dependencies (no numpy, astropy etc for portability)
- [X] Example API usage
- [X] Fully supported Observing Conditions Sensor operations
- [X] Fully supported Safety Monitor operations
- [ ] Fully supported Alert Threshold operations
- [ ] ASCOM Alpaca APIs w/Fast API

---

### Disclaimer

This project is not affiliated with Diffraction Limited in any way. It is a community-driven project. All trademarks and logos are the property of their respective owners.

### License

This project is licensed under the terms of the MIT license.
