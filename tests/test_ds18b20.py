import pytest
from DS18B20 import DS18B20Reader

def test_read_temperature_nohardware(fake_sysfs_ds18b20):
    reader = DS18B20Reader(2, 0x18)
    temp = reader.read_temperature()
    assert round(temp, 3) == 26.312

@pytest.mark.hardware
def test_read_temperature_hardware():
    try:
        reader = DS18B20Reader(2, 0x18)
    except Exception as e:
        pytest.fail(f"Error initializing DS18B20: {e}", pytrace=False)
    
    temp = reader.read_temperature()
    assert temp is not None
    print(f"DS18B20 temperature reading: {temp}")