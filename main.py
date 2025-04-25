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
import logging
import sys
import argparse # Keep argparse for command-line flags like verbose

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
    # Import the run function from the gui module
    from pin_grid_spy import gui, config
except ImportError as e:
    log.error(f"Import Error: {e}. Make sure you are running from the project root directory "
              "and the 'pin_grid_spy' package is accessible.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Run Pin Grid Spy GUI.")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose debug logging."
    )
    # Add other CLI args if needed in the future (e.g., load specific session)
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
        log.debug("Verbose logging enabled.")

    log.info("--- Starting Pin Grid Spy GUI ---")
    # Call the run function from the gui module
    gui.run()
    log.info("--- Pin Grid Spy GUI Closed ---")

if __name__ == "__main__":
    main()