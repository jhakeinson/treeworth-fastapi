import pytest
import pandas as pd
from app.lib.utils.get_propety_data import get_property_data

### Test successful data loading
def test_get_property_data_success(tmp_path):
    # Create a sample CSV file
    property_data = pd.DataFrame({
        "Price": [10.99, 20.99, 30.99],
        "OtherColumn": ["Value1", "Value2", "Value3"]
    })
    tmp_csv_path = tmp_path / "property-data.csv"
    property_data.to_csv(tmp_csv_path, index=False)

    # Call the function with the sample CSV file
    result = get_property_data(tmp_csv_path)

    # Assert the result is a DataFrame with the expected data
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 2)
    assert result["price"].dtype == float

### Test handling null or empty values
def test_get_property_data_null_values(tmp_path):
    # Create a sample CSV file with null values
    property_data = pd.DataFrame({
        "Price": [10.99, None, 30.99],
        "OtherColumn": ["Value1", "Value2", "Value3"]
    })
    tmp_csv_path = tmp_path / "property-data.csv"
    property_data.to_csv(tmp_csv_path, index=False)

    # Call the function with the sample CSV file

    # Call the function with the sample CSV file
    with pytest.raises(ValueError) as exc_info:
        get_property_data(tmp_csv_path)

    # Assert the error message
    assert str(exc_info.value) == "Null found in property-data.csv"

def test_get_property_data_empty(tmp_path):
    # Create an empty CSV file
    tmp_csv_path = tmp_path / "property-data.csv"
    open(tmp_csv_path, "w").close()

    # Call the function with the empty CSV file
    with pytest.raises(ValueError) as exc_info:
        get_property_data(tmp_csv_path)

    # Assert the error message
    assert str(exc_info.value) == "No columns to parse from file"

### Test Price column data type conversion
def test_get_property_data_price_conversion(tmp_path):
    # Create a sample CSV file with Price column as string
    property_data = pd.DataFrame({
        "Price": ["10.99", "20.99", "30.99"],
        "OtherColumn": ["Value1", "Value2", "Value3"]
    })
    tmp_csv_path = tmp_path / "property-data.csv"
    property_data.to_csv(tmp_csv_path, index=False)

    # Call the function with the sample CSV file
    result = get_property_data(tmp_csv_path)

    # Assert the Price column data type is float
    assert result["price"].dtype == float