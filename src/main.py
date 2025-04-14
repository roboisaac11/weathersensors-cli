from argparse import ArgumentParser, Namespace
from sys import platform, stderr, exit
from time import strftime, sleep
from json import dumps, loads
from typing import Any, Callable
from pathlib import Path
from importlib.metadata import version
from BME680 import BME680Reader
from DS18B20 import DS18B20Reader
try:
    import tomllib # type: ignore
except ModuleNotFoundError:
    import tomli as tomllib  # Backport for <3.11

# Map of sensor names to their respective reader functions
SENSOR_MAP: dict[str, Callable[[], dict[str, Any]]] = {
    "bme680": BME680Reader,
    "ds18b20": DS18B20Reader,
}

def setup_sensors() -> None:
    """Initialize and configure the sensors. Populate the SENSOR_MAP dictionary."""

    # Load preferences:
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)
        sensor_conf = config["sensors"]

    # Add the sensors
    for sensor in SENSOR_MAP.keys():
        addr: int = int(sensor_conf[sensor]["address"], 16)
        bus: int = int(sensor_conf[sensor]["bus"])
        sensor_class: object = SENSOR_MAP[sensor]
        
        SENSOR_MAP[sensor] = sensor_class(device_address=addr, bus_number=bus)


def confirm_permissions() -> None:
    """Check if the script has the necessary permissions to run on the current platform."""

    match platform:
        case "linux":
            from os import geteuid
            if geteuid() != 0:
                print("This script must be run as root.", file=stderr)
                exit(1)
        case "win32":
            print("This script is not supported on Windows.", file=stderr)
            exit(1)
        case _:
            print("This script is not supported on this platform.", file=stderr)
            exit(1)

def parse_args() -> Namespace:
    """Parse and return command line arguments."""

    parser = ArgumentParser(description="A CLI tool for reading weather sensors.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version('weathersensors-cli')}")
    parser.add_argument("-l", "--list", action="store_true", help="List available sensors.")
    parser.add_argument(
        "--sensor",
        nargs="+",
        choices=list(SENSOR_MAP.keys()),
        help="Sensor(s) to read from. If omitted, reads all.",
    )
    parser.add_argument("--interval", type=int, help="Interval (in seconds) between reads.")
    parser.add_argument("--count", type=int, help="Number of reads to perform (requires --interval). If omitted, reads indefinitely.")
    parser.add_argument("--json", action="store_true", help="Output in JSON format.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrites data in output file.")
    parser.add_argument("--timestamps", action="store_true", help="Add timestamps to output.")
    parser.add_argument("-o", "--output", help="Output file path.")
    return parser.parse_args()

def read_sensors(sensor_names: list[str]) -> dict[str, dict[str, Any]]:
    """Read data from specified sensors and return as a dictionary."""

    return {
        name: SENSOR_MAP[name]() if name in SENSOR_MAP else {"error": "Unknown sensor"}
        for name in sensor_names
    }

def format_sensor_data(data: dict, timestamps: bool) -> str:
    """Format sensor data as a human-readable string."""

    lines = []
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
    for sensor in data:
        if timestamps:
            lines.append(f"({timestamp}) - {sensor.upper()}:")
        else:
            lines.append(f"{sensor.upper()}:")
        for key, value in data[sensor].items():
            lines.append(f"\t{key}: {value}")
    return "\n".join(lines)

def check_output_file(output_path: str, overwrite: bool) -> None:
    """Check if output file exists and handle according to overwrite flag."""

    path = Path(output_path)
    if path.exists() and path.read_text().strip() != "":
        if overwrite:
            print(f"Overwriting {path.name}")
            path.write_text("")  # Wipe it
        else:
            print("Output file is not empty. Use --overwrite to overwrite.", file=stderr)
            exit(1)

def output_results(data: dict, use_json: bool = False, output_path: str = None, timestamps: bool = False) -> None:
    """Output sensor data either to console or file in specified format."""

    if not output_path:
        print(dumps(data, indent=2) if use_json else format_sensor_data(data, timestamps))
        return
    
    path = Path(output_path)

    if use_json:
        # Handle JSON output format
        try:
            current_data = loads(path.read_text())
        except Exception:
            current_data = {}
        next_index = len(current_data) + 1
        current_data[f"reading_{next_index}"] = data
        if timestamps:
            current_data[f"reading_{next_index}"]["timestamp"] = strftime("%Y-%m-%d %H:%M:%S")
        output_data = current_data

        path.write_text(dumps(output_data, indent=2) + '\n')

    else:
        # Handle plain text output format
        formatted = format_sensor_data(data, timestamps)
        with open(output_path, 'a') as f:
            f.write(formatted + '\n')

def main() -> None:
    """Main function to handle sensor reading and output."""

    confirm_permissions()

    setup_sensors()

    args: Namespace = parse_args()
    sensor_names: list[str] = args.sensor or list(SENSOR_MAP) # If sensor names aren't provided, use all of them

    
    if args.output:
        check_output_file(args.output, args.overwrite)

    if args.list:
        print("Available sensors:")
        for sensor in SENSOR_MAP:
            print(f"- {sensor}")
        exit(0)

    if args.interval:
        # Continuous reading mode with interval
        count = args.count if args.count else float("inf")
        for i in range(int(count)):
            data = read_sensors(sensor_names)
            output_results(data, use_json=args.json, output_path=args.output, timestamps=args.timestamps)
            if i < count - 1:
                sleep(args.interval)
    else:
        # Single reading mode
        data = read_sensors(sensor_names)
        output_results(data, use_json=args.json, output_path=args.output, timestamps=args.timestamps)

if __name__ == "__main__":
    main()