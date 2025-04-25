"""
Copyright (C) 2025 Kanarath.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


INTRODUCE HERE PIN GRID SPY DESCRIPTION------------------------> <----------------------------- IMPORTANT
"""

# tests/test_utils.py
import pytest
from unittest.mock import MagicMock

# Assuming your project structure allows this import
from pin_grid_spy import utils

# Helper to create mock EXIF tag objects
def create_mock_tag(value):
    tag = MagicMock()
    tag.values = value
    return tag

# --- Tests for _dms_to_dd ---

@pytest.mark.parametrize("degrees, minutes, seconds, direction, expected", [
    (40, 44, 54.3, 'N', 40.74841666666667), # Example: NYC Latitude
    (73, 59, 9.5, 'W', -73.98597222222223), # Example: NYC Longitude
    (34, 0, 0, 'S', -34.0),
    (18, 0, 0, 'E', 18.0),
    (0, 0, 0, 'N', 0.0),
])
def test_dms_to_dd(degrees, minutes, seconds, direction, expected):
    """Tests Degrees Minutes Seconds to Decimal Degrees conversion."""
    result = utils._dms_to_dd(degrees, minutes, seconds, direction)
    assert result == pytest.approx(expected)

# --- Tests for get_decimal_coords ---

def test_get_decimal_coords_success():
    """Tests successful extraction of decimal coordinates."""
    mock_tags = {
        'GPS GPSLatitude': create_mock_tag([40, 44, 54.3]),
        'GPS GPSLatitudeRef': create_mock_tag('N'),
        'GPS GPSLongitude': create_mock_tag([73, 59, 9.5]),
        'GPS GPSLongitudeRef': create_mock_tag('W'),
    }
    lat, lon = utils.get_decimal_coords(mock_tags)
    assert lat == pytest.approx(40.7484166)
    assert lon == pytest.approx(-73.9859722)

def test_get_decimal_coords_missing_tags():
    """Tests coordinate extraction when essential tags are missing."""
    mock_tags = {
        'GPS GPSLatitude': create_mock_tag([40, 44, 54.3]),
        'GPS GPSLatitudeRef': create_mock_tag('N'),
        # Missing Longitude
    }
    lat, lon = utils.get_decimal_coords(mock_tags)
    assert lat is None
    assert lon is None

def test_get_decimal_coords_empty_tags():
    """Tests coordinate extraction with an empty tag dictionary."""
    lat, lon = utils.get_decimal_coords({})
    assert lat is None
    assert lon is None

# --- Tests for format_datetime ---

def test_format_datetime_success():
    mock_tags = {'EXIF DateTimeOriginal': create_mock_tag("2023:10:27 10:30:00")}
    assert utils.format_datetime(mock_tags) == "2023:10:27 10:30:00"

def test_format_datetime_missing():
    assert utils.format_datetime({}) == "N/A"

# --- Tests for format_model ---

def test_format_model_success():
    mock_tags = {'Image Model': create_mock_tag("TestCamera S1")}
    assert utils.format_model(mock_tags) == "TestCamera S1"

def test_format_model_missing():
    assert utils.format_model({}) == "N/A"