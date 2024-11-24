import pytest
from app.lib.utils.flatten_json import flatten_json

def test_flatten_json():
    input_json = {
        "short": {
            "drive": {
                "abbey": {
                    "abbey drive": 0
                }
            }
        },
        "tall": {
            "avenue": {
                "ayrfield": {
                    "ayrfield avenue": 10
                }
            }
        }
    }
    expected_output = {
        "short": {
            "abbey drive": 0
        },
        "tall": {
            "ayrfield avenue": 10
        }
    }
    assert flatten_json(input_json) == expected_output

def test_flatten_json_empty():
    input_json = {}
    expected_output = {}
    assert flatten_json(input_json) == expected_output

def test_flatten_json_no_integers():
    input_json = {
        "short": {
            "drive": {
                "abbey": {
                    "abbey drive": "hello"
                }
            }
        }
    }
    expected_output = {}
    assert flatten_json(input_json) == expected_output

def test_flatten_json_raises_error():
    # Test that the function raises a TypeError when input_json is None
    # Expect this to pass if the function raises a TypeError

    input_json = None
    with pytest.raises(TypeError):
        flatten_json(input_json)
