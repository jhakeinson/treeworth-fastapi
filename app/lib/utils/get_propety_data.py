from calendar import c
import pandas as pd
from .convert_to_float import convert_to_float

def get_property_data(csv_path="data/property-data.csv"):
    # Load the data/property-data.csv
    property_data = pd.read_csv(csv_path, encoding="latin1")

    # check for null or empty values.
    # if any null or empty values are found, throw an error
    if property_data.isnull().values.any():
        raise ValueError("Null found in property-data.csv")
    if property_data.empty:
        raise ValueError("No columns to parse from file")

    # check if Price is a float.
    # if not, convert it to a float with precision of 2
    if not property_data["Price"].dtype == float:
        property_data["Price"] = property_data["Price"].apply(convert_to_float)

    # rename the columns
    # current columns: Date of Sale (dd/mm/yyyy),Address,Street Name,Price
    # new columns: date_of_sale,full_address,street_name,price
    property_data = property_data.rename(columns={
        "Date of Sale (dd/mm/yyyy)": "date_of_sale",
        "Address": "full_address",
        "Street Name": "street_name",
        "Price": "price"
    })

    return property_data