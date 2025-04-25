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

# main.py
import argparse
import logging
import pathlib
import sys
import time

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
        # Optional: Add FileHandler here if needed
        # logging.FileHandler("pin_grid_spy.log")
    ]
)
log = logging.getLogger(__name__)

# Import project modules *after* logging is configured
try:
    from pin_grid_spy import config, image_processor, map_generator
except ImportError as e:
    log.error(f"Import Error: {e}. Make sure you are running from the project root directory "
              "and the 'pin_grid_spy' package is accessible.")
    sys.exit(1)


def main():
    start_time = time.time()
    log.info("--- Starting Pin Grid Spy ---")

    parser = argparse.ArgumentParser(description="Process images and generate a geolocation map.")
    parser.add_argument(
        "-i", "--input-dir",
        type=pathlib.Path,
        default=config.DEFAULT_INPUT_DIR,
        help=f"Directory containing input images. Default: {config.DEFAULT_INPUT_DIR}"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=pathlib.Path,
        default=config.DEFAULT_OUTPUT_DIR,
        help=f"Directory to save the map and thumbnails. Default: {config.DEFAULT_OUTPUT_DIR}"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose debug logging."
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
        log.debug("Verbose logging enabled.")

    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()
    thumb_dir = output_dir / "thumbnails" # Dynamic thumbnail dir based on output
    map_file_path = output_dir / config.DEFAULT_MAP_FILENAME

    # --- Validate Inputs ---
    if not input_dir.is_dir():
        log.error(f"Input directory not found or is not a directory: {input_dir}")
        sys.exit(1)

    try:
        # Ensure output directories exist
        output_dir.mkdir(parents=True, exist_ok=True)
        thumb_dir.mkdir(parents=True, exist_ok=True)
        log.info(f"Using input directory: {input_dir}")
        log.info(f"Using output directory: {output_dir}")
    except OSError as e:
        log.error(f"Could not create output directories: {e}")
        sys.exit(1)


    # --- Processing ---
    log.info("Starting image processing...")
    image_data = image_processor.process_directory(input_dir, thumb_dir)

    if not image_data:
        log.warning("No images with usable GPS data found. Exiting.")
        sys.exit(0)

    # --- Map Generation ---
    log.info("Starting map generation...")
    map_generator.create_map(image_data, map_file_path)

    end_time = time.time()
    log.info(f"--- Pin Grid Spy finished in {end_time - start_time:.2f} seconds ---")
    log.info(f"Map saved to: {map_file_path}")
    log.info(f"Thumbnails saved in: {thumb_dir}")
    log.info("Open the map.html file in your browser.")

if __name__ == "__main__":
    main()# main.py
import argparse
import logging
import pathlib
import sys
import time

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
        # Optional: Add FileHandler here if needed
        # logging.FileHandler("pin_grid_spy.log")
    ]
)
log = logging.getLogger(__name__)

# Import project modules *after* logging is configured
try:
    from pin_grid_spy import config, image_processor, map_generator
except ImportError as e:
    log.error(f"Import Error: {e}. Make sure you are running from the project root directory "
              "and the 'pin_grid_spy' package is accessible.")
    sys.exit(1)


def main():
    start_time = time.time()
    log.info("--- Starting Pin Grid Spy ---")

    parser = argparse.ArgumentParser(description="Process images and generate a geolocation map.")
    parser.add_argument(
        "-i", "--input-dir",
        type=pathlib.Path,
        default=config.DEFAULT_INPUT_DIR,
        help=f"Directory containing input images. Default: {config.DEFAULT_INPUT_DIR}"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=pathlib.Path,
        default=config.DEFAULT_OUTPUT_DIR,
        help=f"Directory to save the map and thumbnails. Default: {config.DEFAULT_OUTPUT_DIR}"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose debug logging."
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
        log.debug("Verbose logging enabled.")

    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()
    thumb_dir = output_dir / "thumbnails" # Dynamic thumbnail dir based on output
    map_file_path = output_dir / config.DEFAULT_MAP_FILENAME

    # --- Validate Inputs ---
    if not input_dir.is_dir():
        log.error(f"Input directory not found or is not a directory: {input_dir}")
        sys.exit(1)

    try:
        # Ensure output directories exist
        output_dir.mkdir(parents=True, exist_ok=True)
        thumb_dir.mkdir(parents=True, exist_ok=True)
        log.info(f"Using input directory: {input_dir}")
        log.info(f"Using output directory: {output_dir}")
    except OSError as e:
        log.error(f"Could not create output directories: {e}")
        sys.exit(1)


    # --- Processing ---
    log.info("Starting image processing...")
    image_data = image_processor.process_directory(input_dir, thumb_dir)

    if not image_data:
        log.warning("No images with usable GPS data found. Exiting.")
        sys.exit(0)

    # --- Map Generation ---
    log.info("Starting map generation...")
    map_generator.create_map(image_data, map_file_path)

    end_time = time.time()
    log.info(f"--- Pin Grid Spy finished in {end_time - start_time:.2f} seconds ---")
    log.info(f"Map saved to: {map_file_path}")
    log.info(f"Thumbnails saved in: {thumb_dir}")
    log.info("Open the map.html file in your browser.")

if __name__ == "__main__":
    main()