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


# pin_grid_spy/config.py
import pathlib

# --- Directory Setup ---
# Resolve paths relative to the project root (assuming main.py is run from root)
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
DEFAULT_INPUT_DIR = PROJECT_ROOT / "input_images"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_THUMBNAIL_DIR = DEFAULT_OUTPUT_DIR / "thumbnails"
DEFAULT_STATIC_DIR = PROJECT_ROOT / "static" # For sidebar assets
DEFAULT_MAP_FILENAME = "map.html"

# --- Image Processing ---
THUMBNAIL_SIZE = (200, 200)  # (width, height) in pixels
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# --- Map Generation ---
DEFAULT_MAP_LOCATION = [20, 0]  # Default center latitude/longitude if no images
DEFAULT_MAP_ZOOM = 2            # Default zoom level
GOOGLE_MAPS_URL_TEMPLATE = "https://www.google.com/maps?q={lat},{lon}"

# --- Sidebar ---
SIDEBAR_CSS_PATH = "static/leaflet-sidebar.min.css" # Relative to output html
SIDEBAR_JS_PATH = "static/leaflet-sidebar.min.js"   # Relative to output html