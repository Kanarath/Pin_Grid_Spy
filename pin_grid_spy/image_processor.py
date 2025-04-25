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

# pin_grid_spy/image_processor.py
import os
import pathlib
import logging
from PIL import Image, UnidentifiedImageError
import exifread

from . import config
from . import utils

log = logging.getLogger(__name__)

# Suppress verbose ExifRead warnings about MakerNote tags
logging.getLogger('exifread').setLevel(logging.ERROR)

def create_thumbnail(image_path: pathlib.Path, thumb_path: pathlib.Path):
    """Creates a thumbnail for the image if it doesn't exist."""
    if thumb_path.exists():
        log.debug(f"Thumbnail already exists: {thumb_path}")
        return True
    try:
        with Image.open(image_path) as img:
            img.thumbnail(config.THUMBNAIL_SIZE)
            # Ensure target directory exists
            thumb_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(thumb_path)
            log.info(f"Created thumbnail: {thumb_path}")
            return True
    except UnidentifiedImageError:
        log.warning(f"Cannot create thumbnail for non-image file: {image_path}")
        return False
    except Exception as e:
        log.error(f"Failed to create thumbnail for {image_path}: {e}", exc_info=True)
        return False

def process_image(image_path: pathlib.Path, thumb_dir: pathlib.Path):
    """
    Extracts EXIF data, creates a thumbnail, and returns structured data.
    Returns None if essential data (GPS) is missing or processing fails.
    """
    log.info(f"Processing image: {image_path}")
    try:
        # 1. Read EXIF Tags
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='DateTimeOriginal') # Optimization

        if not tags:
            log.warning(f"No EXIF tags found in {image_path}")
            return None

        # 2. Extract GPS Coordinates
        lat, lon = utils.get_decimal_coords(tags)
        if lat is None or lon is None:
            log.warning(f"No valid GPS coordinates found in {image_path}")
            return None # Skip images without GPS

        # 3. Extract Other Metadata
        date_time = utils.format_datetime(tags)
        model = utils.format_model(tags)

        # 4. Create Thumbnail
        # Use a safe filename for the thumbnail (e.g., based on original)
        # Add a hash or unique ID if filename collisions are a concern, but simple is fine for MVP
        thumb_filename = f"{image_path.stem}_thumb{image_path.suffix}"
        thumb_path = thumb_dir / thumb_filename
        if not create_thumbnail(image_path, thumb_path):
            log.warning(f"Skipping image due to thumbnail creation failure: {image_path}")
            return None # Skip if thumbnail fails

        # 5. Return Structured Data
        image_data = {
            "original_path": str(image_path),
            "thumbnail_rel_path": str(thumb_path.relative_to(thumb_dir.parent)).replace("\\", "/"), # Ensure forward slashes
            "latitude": lat,
            "longitude": lon,
            "datetime": date_time,
            "model": model,
        }
        log.info(f"Successfully processed {image_path}")
        return image_data

    except FileNotFoundError:
        log.error(f"Image file not found: {image_path}")
        return None
    except Exception as e:
        log.error(f"Error processing image {image_path}: {e}", exc_info=True)
        return None


def process_directory(input_dir: pathlib.Path, thumb_dir: pathlib.Path):
    """Processes all supported images in the input directory."""
    processed_data = []
    image_count = 0
    processed_count = 0

    log.info(f"Scanning directory: {input_dir}")
    thumb_dir.mkdir(parents=True, exist_ok=True) # Ensure thumbnail dir exists

    for item in input_dir.iterdir():
        if item.is_file() and item.suffix.lower() in config.SUPPORTED_EXTENSIONS:
            image_count += 1
            data = process_image(item, thumb_dir)
            if data:
                processed_data.append(data)
                processed_count += 1

    log.info(f"Scan complete. Found {image_count} images, processed {processed_count} with GPS data.")
    return processed_data