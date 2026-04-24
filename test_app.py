import pytest
import pandas as pd
from app import generate_sensor_data

def test_data_generation():
    """Test if generate_sensor_data returns correct structure"""
    df = generate_sensor_data()
    
    # Check if DataFrame is not empty
    assert not df.empty
    
    # Check required columns
    expected_columns = ['timestamp', 'sensor', 'temperature', 'humidity']
    for col in expected_columns:
        assert col in df.columns
    
    # Check data types
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])
    assert df['temperature'].dtype in ['float64', 'int64']
    assert df['humidity'].dtype in ['float64', 'int64']

def test_temperature_range():
    """Test if temperatures are within realistic range"""
    df = generate_sensor_data()
    assert df['temperature'].between(15, 35).all()

def test_humidity_range():
    """Test if humidity is within realistic range"""
    df = generate_sensor_data()
    assert df['humidity'].between(30, 70).all()

def test_sensor_names():
    """Test if all sensors are from expected set"""
    df = generate_sensor_data()
    expected_sensors = ['Sensor-A', 'Sensor-B', 'Sensor-C']
    assert df['sensor'].isin(expected_sensors).all()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])