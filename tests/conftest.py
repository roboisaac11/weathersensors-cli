import os
import shutil
import tempfile
import pytest
from unittest.mock import MagicMock, patch

def pytest_addoption(parser):
    parser.addoption(
        "--hardware", action="store_true", default=False, help="Run hardware tests"
    )

def pytest_runtest_setup(item):
    # If the test is marked as hardware, but `-m hardware` wasn't passed
    if "hardware" in item.keywords:
        selected_marker = item.config.getoption("-m")
        if selected_marker != "hardware":
            pytest.skip("skipped hardware test: pass `-m hardware` to run")

@pytest.fixture
def fake_sysfs_ds18b20(monkeypatch):
    # Setup fake sysfs structure
    fake_sys = tempfile.mkdtemp()
    fake_i2c_path = os.path.join(fake_sys, "sys/bus/i2c/devices/i2c-2")
    fake_w1_path = os.path.join(fake_sys, "sys/bus/w1/devices/28-000005e2fdc3")
    os.makedirs(fake_i2c_path)
    os.makedirs(fake_w1_path)

    # Create files
    with open(os.path.join(fake_i2c_path, "new_device"), "w") as f:
        f.write("")
    with open(os.path.join(fake_w1_path, "w1_slave"), "w") as f:
        f.write("a1 01 4b 46 7f ff 0c 10 aa : crc=aa YESn\n1 01 4b 46 7f ff 0c 10 aa t=26312")

    # 2. Patch `glob.glob` to find the fake slave file
    def fake_glob(_path):
        return [os.path.join(fake_w1_path, "w1_slave")]

    monkeypatch.setattr("glob.glob", fake_glob)

    # 3. Patch `open` to redirect only sysfs-related files
    real_open = open

    def fake_open(file, mode='r', *args, **kwargs):
        if "w1_slave" in file:
            return real_open(os.path.join(fake_w1_path, "w1_slave"), mode, *args, **kwargs)
        elif "new_device" in file:
            return real_open(os.path.join(fake_i2c_path, "new_device"), mode, *args, **kwargs)
        return real_open(file, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    yield 

    # 4. Cleanup
    shutil.rmtree(fake_sys)

@pytest.fixture
def fake_bme680_sensor():
    mock_sensor = MagicMock()
    mock_sensor.get_sensor_data.return_value = True
    mock_sensor.data.temperature = 22.0
    mock_sensor.data.pressure = 1000.0
    mock_sensor.data.humidity = 55.5
    mock_sensor.data.gas_resistance = 12345
    mock_sensor.data.heat_stable = True
    return mock_sensor

@pytest.fixture
def mock_bme680_sensor(fake_bme680_sensor):
    with patch("BME680.bme680.BME680", return_value=fake_bme680_sensor):
        yield fake_bme680_sensor