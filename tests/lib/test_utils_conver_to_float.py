from app.lib.utils.convert_to_float import convert_to_float

def test_convert_to_float():
    assert convert_to_float("79,500.5") == 79500.50

def test_convert_to_float_decimal_points():
    # make sure decimal points precision is 2.
    # i.e. 0.5 => 0.50, 2.5 => 2.50, 3 => 3.00, 0.20222 => 0.20 

    assert convert_to_float("0.5") == 0.50
    assert convert_to_float("2.5") == 2.50
    assert convert_to_float("3") == 3.00
    assert convert_to_float("0.20222") == 0.20