# Default I2C Address
ADS7830_I2C_ADDR: int = 0x48

# Power-Down Selection Enum
class PowerDown:
    BETWEEN_CONVERSIONS: int = 0x00
    REF_OFF_ADC_ON: int = 0x01
    REF_ON_ADC_OFF: int = 0x02
    REF_ON_ADC_ON: int = 0x03

# Channel Selection Control Enum (used internally for command byte logic)
SINGLE_CH0: int = 0x08
SINGLE_CH2: int = 0x09
SINGLE_CH4: int = 0x0A
SINGLE_CH6: int = 0x0B
SINGLE_CH1: int = 0x0C
SINGLE_CH3: int = 0x0D
SINGLE_CH5: int = 0x0E
SINGLE_CH7: int = 0x0F

DIFF_CH0_CH1: int = 0x00
DIFF_CH2_CH3: int = 0x01
DIFF_CH4_CH5: int = 0x02
DIFF_CH6_CH7: int = 0x03