# /// script
# dependencies = [
#   "bme680",
#   "smbus2"
# ]
# ///

import bme680 # type: ignore

class BME680Reader:
    """A class to handle reading data from a BME680 environmental sensor.

    This class initializes and manages a BME680 sensor, configuring it for optimal
    readings of temperature, pressure, humidity, and gas resistance. It provides
    methods to initialize the sensor with appropriate settings and read data from it.

    Attributes:
        sensor: The BME680 sensor instance used for measurements.

    Args:
        bus_number (int): The I2C bus number to use (default: 2).
        device_address (int): The I2C device address of the BME680 (default: 0x77).
        _debug_sensor: Optional mock sensor for testing (default: None).
    """

    def __init__(self, bus_number: int = 2, device_address: int = 0x77, _debug_sensor=None) -> None:
        """Initialize the BME680Reader with specified bus and address.

        Sets up the BME680 sensor on the specified I2C bus and address, or uses a
        provided debug sensor for testing purposes.

        Args:
            bus_number (int): The I2C bus number to use.
            device_address (int): The I2C device address of the BME680.
            _debug_sensor (int): Optional mock sensor for testing.
        """
        
        if _debug_sensor is None:
            from smbus2 import SMBus
            self.sensor = bme680.BME680(device_address, SMBus(bus_number))
        else:
            self.sensor = _debug_sensor

        self._initialize_bme680()

    def _initialize_bme680(self) -> None:
        """Initialize the BME680 sensor with appropriate settings.

        Configures the sensor's oversampling rates for humidity, pressure, and
        temperature measurements. Also sets up the gas sensor with appropriate
        temperature and duration settings, and enables gas measurements.
        """

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)
    
    def get_readings(self) -> dict | None:
        """Read current sensor data from the BME680.

        Attempts to read the current sensor data and returns it as a dictionary
        containing temperature, pressure, humidity, and gas resistance values.

        Returns:
            dict: A dictionary containing the following keys:
                - temperature: Current temperature in degrees Celsius
                - pressure: Current pressure in hPa
                - humidity: Current relative humidity in %
                - gas_resistance: Current gas resistance in Ohms (None if heat unstable)
            None: If sensor data could not be read
        """

        if not self.sensor.get_sensor_data():
            return None
        
        return {
            "temperature": self.sensor.data.temperature,
            "pressure": self.sensor.data.pressure,
            "humidity": self.sensor.data.humidity,
            "gas_resistance": self.sensor.data.gas_resistance if self.sensor.data.heat_stable else None
        }