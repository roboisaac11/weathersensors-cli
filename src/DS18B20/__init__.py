import glob
from . import constants

class DS18B20Reader:
    """Class for reading temperature from DS18B20 sensors via DS2482 bridge.

    This class handles the initialization of the DS2482 I2C-to-1-Wire bridge
    and reading temperature values from connected DS18B20 sensors.

    Attributes:
        bus_number (int): The I2C bus number where the DS2482 is connected.
        device_address (int): The I2C address of the DS2482 device.
        output_path (str): Path to the temperature sensor's output file.

    Args:
        bus_number (int, optional): I2C bus number. Defaults to 2.
        device_address (int, optional): DS2482 I2C address. Defaults to 0x18.
        init (bool, optional): Whether to initialize the DS2482 on creation. Defaults to True.

    Raises:
        FileNotFoundError: If no DS18B20 devices are found after initialization.
    """

    def __init__(self, bus_number: int = 2, device_address: int = 0x18) -> None:
        self.bus_number: int = bus_number
        self.device_address: int = device_address
        self.output_path: str = glob.glob(constants.OUTPUT_PATH)

        self._initialize_ds2482()
        
    
    def _initialize_ds2482(self) -> None:
        """Initialize the DS2482 I2C-to-1-Wire bridge.

        This method writes the device address to the I2C bus to initialize
        the DS2482 bridge. It then verifies that a DS18B20 device is present.

        Raises:
            FileNotFoundError: If no DS18B20 devices are found after initialization.
        """

        file_path: str = constants.I2C_NEW_DEVICE_PATH.format(self.bus_number)

        try:
            with open(file_path, 'w') as f:
                f.write(f"ds2482 {hex(self.device_address)}\n")
        except Exception as e:
            print(f"Error: {e}")

        if not self.output_path:
            raise FileNotFoundError(f"No DS18B20 devices found. Could not find file at {constants.OUTPUT_PATH}")

    def read_temperature(self) -> float:
        """Read the current temperature from the DS18B20 sensor.

        Reads the raw temperature value from the sensor's output file
        and converts it to degrees Celsius.

        Returns:
            float: Temperature in degrees Celsius.

        Note:
            The raw temperature value is divided by 1000 to convert
            from millidegrees to degrees Celsius.
        """

        with open(self.output_path[0], 'r') as f:
            content: str = f.read()
            temp: str = content.split("t=")[1]
            return float(temp) / 1000