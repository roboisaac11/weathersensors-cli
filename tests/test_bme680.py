import pytest
from BME680 import BME680Reader

def test_bme680_read_sensor_nohardware(mock_bme680_sensor):
    reader = BME680Reader(2, 0x77, _debug_sensor=mock_bme680_sensor)
    result = reader.read_sensor()

    assert result == {
        "temperature": 22.0,
        "pressure": 1000.0,
        "humidity": 55.5,
        "gas_resistance": 12345
    }

@pytest.mark.hardware
def test_bme680_read_sensor_hardware():
    try:
        reader = BME680Reader(2, 0x77)
    except Exception as e:
        pytest.fail(f"Error initializing BME680: {e}", pytrace=False)

    result = reader.read_sensor()

    assert len(result) == 4

