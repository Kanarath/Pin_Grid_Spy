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

# pin_grid_spy/utils.py
import logging

log = logging.getLogger(__name__)

def _dms_to_dd(degrees, minutes, seconds, direction):
    """Converts Degrees Minutes Seconds (DMS) to Decimal Degrees (DD)."""
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ['S', 'W']:
        dd *= -1
    return dd

def get_decimal_coords(tags):
    """Extracts and converts GPS coordinates from EXIF tags to decimal degrees."""
    lat = None
    lon = None

    try:
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _dms_to_dd(
                gps_latitude.values[0],
                gps_latitude.values[1],
                gps_latitude.values[2],
                gps_latitude_ref.values
            )
            lon = _dms_to_dd(
                gps_longitude.values[0],
                gps_longitude.values[1],
                gps_longitude.values[2],
                gps_longitude_ref.values
            )
            log.debug(f"Converted coords: Lat {lat}, Lon {lon}")
        else:
             log.debug("Missing required GPS tags for coordinate conversion.")

    except Exception as e:
        log.error(f"Error converting GPS coordinates: {e}", exc_info=True)

    return lat, lon

def format_datetime(tags):
    """Safely extracts and formats DateTimeOriginal."""
    try:
        datetime_tag = tags.get('EXIF DateTimeOriginal')
        if datetime_tag:
            return str(datetime_tag.values)
    except Exception as e:
        log.warning(f"Could not format DateTimeOriginal: {e}")
    return "N/A"

def format_model(tags):
    """Safely extracts camera model."""
    try:
        model_tag = tags.get('Image Model')
        if model_tag:
            return str(model_tag.values)
    except Exception as e:
         log.warning(f"Could not format Image Model: {e}")
    return "N/A"