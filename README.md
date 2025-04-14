# WeatherSensors CLI
## Table of Contents
1. [Introduction](#Introduction)
2. [Getting Started](#Getting%20Started)
3. [Installation](#Installation)
    - [Installing the Wheel](#Installing%20the%20Wheel)
    - [Installing from a Cloned Repository](Installing%20from%20a%20Cloned%20Repository)
4. [Usage](#Usage)
    - [Command-Line Options](Command-Line%20Options)
5. [Setup with uv](Setup%20with%20uv)
6. [Testing](#Testing)

## Introduction
WeatherSensors CLI is a command-line tool for reading weather data from sensors on an Orange Pi. It is used for a DIY weather station, but you can modify it to work with your own. Everything should be connected via I2C, and for this project on bus 2. The sensors it currently supports are:
- BME680
- OneWire DS18B20 temperature sensor (connected through a DS2482)
- ADS7830
### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Getting Started
### 1. Install the Package
Start by following the [Installation](#Installation) section to get the tool installed on your system.

### 2. Running the Tool
Once installed, you can run the tool via the command line with:

```bash
weathersensors
```
Head to the [Usage](#Usage) section for more information on how to use the tool.

## Installation
### Installing the Wheel
If you just want to install this project as it is, the best way is through one of the build files.

First download a `.whl` file or a `.tar.gz` file from the [releases](https://github.com/roboisaac11/weathersensors-cli/releases) page, then install using `pip install`. For example:
```bash
pip install weathersensors-cli.whl
```
### Installing from a Cloned Repository
If you want to customise this project or contribute, you should clone the repo. Once you have done so, you can install with `pip install .` at the root of the project. For example:
```bash
git clone https://github.com/roboisaac11/weathersensors-cli.git
cd weathersensors-cli
pip install .
```
> [!NOTE]
> If you wish to modify the code or contribute, install in editable mode with `pip install `**`-e`**` .`
> This enables you to not have to re-install every time you make a change.

## Usage
Running the Tool
Once installed, you can simply run the command to get a reading from all the sensors:

```bash
weathersensors
```
Example output:
```bash
BME680:
        temperature: 22.3
        humidity: 50
        pressure: 1013
DS18B20:
        temperature: 21.5
```
### Command-Line Options

You can specify different options when running the tool. Options available:
- `-v`, `--version` : Output the version of the installed tool.
- `-l`, `--list` : Lists the available sensors.
- `--sensor` : Specify the sensor to use (e.g., bme680). You can specify more than one. If omitted, all sensors will be read.
- `--interval` : Set the polling interval for sensor data (in seconds).
- `--count` : Used with `--interval`. Sets the amount of times to read the sensors.
- `--json` : Outputs in JSON format.
- `-o`, `--output` : Specify the output path. If omitted, outputs to console. Will fail if the file isn't empty or `--overwrite` is not passed.
- `--overwrite` : Used with `-output` and `--interval`. Overwrites data in the output file.
- `--timestamps` : Adds timestamps to output.
- `--help` : Display help for the available commands.

#### Examples:

```bash
weathersensors --sensor bme680 --interval 60
```
This will fetch data from the BME680 sensor every 60 seconds indefinitely.
<br>
<br>

```bash
weathersensors --json
```
This will get data from all the sensors output it to the console in JSON format.
<br>
<br>

```bash
weathersensors --interval 5 --count 3 --json --timestamp
```
This will poll the sensors three times with five seconds between and save it in JSON format to `data.json` with timestamps.

## Setup with uv
This project is managed with the [uv project manager](https://docs.astral.sh/uv/). You only need to install uv if you’re cloning the repo. If you're using a release package, just use pip.
### Installing uv
To install uv, run:
#### Windows

```pwsh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Linux or MacOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or you can use pip:

```bash
pip install uv
```
See the [documentation](https://docs.astral.sh/uv/getting-started/installation/) for more information.

#### Configuring I2C devices:
You can specify the I2C bus and device address at the bottom of the  `pyproject.toml` file. This is located in the root of the project.

An example configuration could be:
```toml

...

[sensors.bme680]
bus = 2
address = "0x76"

[sensors.ads7830]
bus = 2
address = "0x48"

[sensors.ds2482]
bus = 2
address = "0x18"
```

### Running the Project:

To run the project with uv (which will automatically install any dependencies):
```bash
uv run src/main.py
```
or if you arn't using uv:
```bash
python src/main.py
```
## Testing
This project uses [pytest](https://docs.pytest.org/) to manage testing.
### Setup
Before you run the tests, make sure you are in the virtual environment created by uv. If none exists yet, run `uv venv` to generate it.

To activate the virtual environment, run:
#### Windows
```bash
.venv\Scripts\activate
```
#### Linux and MacOS
```bash
source .venv/bin/activate
```

Also make sure that `pytest` is installed.

### Running Tests
To run tests, simply use:
```bash
pytest
```
This will only run tests in a simulated environment - it won't test any pysical hardware. To test the sensors, use:
```bash
pytest -m hardware
```