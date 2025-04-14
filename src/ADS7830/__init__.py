from smbus2 import SMBus # type: ignore
from . import constants

class ADS7830Reader:
    """ADS7830 Analog-to-Digital Converter (ADC) Reader.

    This class provides an interface to read analog values from the ADS7830 ADC chip
    over I2C communication.

    Attributes:
        i2c_addr (int): The I2C address of the ADS7830 device
        bus (SMBus): SMBus object for I2C communication

    Args:
        i2c_addr (int): I2C address of the device (default: constants.ADS7830_I2C_ADDR)
        bus_num (int): I2C bus number to use (default: 2)
    """

    def __init__(self, bus_number: int = 2, device_address: int = 0x48) -> None:
        self.i2c_addr = device_address
        self.bus = SMBus(bus_number)

    def read_adc_single(self, channel: int, power_down=constants.PowerDown.REF_ON_ADC_ON) -> int:
        """Read a single-ended analog value from the specified channel.

        Reads the analog value from a single channel referenced to ground.

        Args:
            channel (int): ADC channel number (0-7)
            power_down: Power management mode (default: 0x01)

        Returns:
            int: ADC conversion result (0-255)

        Raises:
            ValueError: If channel number is invalid
            RuntimeError: If I2C communication fails
        """

        if channel > 7:
            raise ValueError("Invalid channel. Channel must be between 0 and 7.")

        if channel % 2 == 0:
            command: int = constants.SINGLE_CH0 + (channel // 2)
        else:
            command: int = constants.SINGLE_CH1 + ((channel - 1) // 2)

        command <<= 4                       # Move the channel info into bits 7–4
        command |= (power_down << 2)        # Set power-down bits in bits 3–2

        try:
            self.bus.write_byte(self.i2c_addr, command)
            adc_val: int = self.bus.read_byte(self.i2c_addr)
            
            return adc_val
        except Exception as e:
            raise RuntimeError(f"I2C Read error: {e}") from e

    def read_adc_diff(self, channel:int, power_down:int=constants.PowerDown.REF_ON_ADC_ON) -> int:
        """Read a differential analog value between channel pairs.

        Reads the analog value as the difference between two channels.
        Channel pairs are: (0-1), (2-3), (4-5), (6-7)

        Args:
            channel (int): ADC channel number (0-7). Even numbers select positive input,
                         odd numbers select negative input of the pair.
            power_down (int): Power management mode (default: REF_ON_ADC_ON)

        Returns:
            int: ADC conversion result (0-255)

        Raises:
            ValueError: If channel number is invalid
            RuntimeError: If I2C communication fails
        """

        if channel > 7:
            raise ValueError("Invalid channel. Channel must be between 0 and 7.")

        if channel % 2 == 0:
            command: int = constants.DIFF_CH0_CH1 + (channel // 2)
        else:
            command: int = constants.DIFF_CH0_CH1 + ((channel - 1) // 2)

        command <<= 4
        command |= (power_down << 2)

        try:
            self.bus.write_byte(self.i2c_addr, command)
            adc_val: int = self.bus.read_byte(self.i2c_addr)
            return adc_val
        
        except Exception as e:
            raise RuntimeError(f"I2C Read error: {e}") from e