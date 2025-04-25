# Pin Grid Spy - MVP

Pin Grid Spy is a tool to visualize geolocated images on an interactive map. This MVP focuses on processing locally stored images.

## Features

*   Scans a directory for JPG/JPEG/PNG images.
*   Extracts EXIF metadata (GPS Coordinates, Date/Time, Camera Model).
*   Generates thumbnails for map popups.
*   Creates a single, self-contained `map.html` file.
*   Interactive Map Features:
    *   OpenStreetMap base layer.
    *   Markers clustered for performance (`MarkerCluster`).
    *   Popups on marker click showing thumbnail, metadata, and Google Maps link.
    *   Measurement tool (`MeasureControl`) for distance/area.
    *   Sidebar (`Leaflet-Sidebar-v2`) for analyst notes (saved to browser local storage).
*   Runs entirely locally, zero hosting cost.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd pin-grid-spy
    ```
2.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate    # Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **(Manual Step)** Download Sidebar Assets:
    *   Download `leaflet-sidebar.min.css` from [here](https://github.com/nickpeihl/leaflet-sidebar-v2/blob/master/css/leaflet-sidebar.min.css) and place it in the `static/` directory.
    *   Download `leaflet-sidebar.min.js` from [here](https://github.com/nickpeihl/leaflet-sidebar-v2/blob/master/js/leaflet-sidebar.min.js) and place it in the `static/` directory.

## Usage

1.  **Place Images:** Put your JPG, JPEG, or PNG images (containing GPS EXIF data) into the `input_images/` directory (or specify a different directory using the `-i` flag).
2.  **Run the script:**
    ```bash
    python main.py
    ```
    *   **Optional Arguments:**
        *   `-i /path/to/your/images`: Specify a custom input directory.
        *   `-o /path/to/output`: Specify a custom output directory.
        *   `-v` or `--verbose`: Enable detailed debug logging.

3.  **View the Map:** Open the generated `output/map.html` file in your web browser. The `output/thumbnails/` directory will contain the generated thumbnails.

## Project Structure

pin-grid-spy/
├── input_images/ # Default image input
├── output/ # Default output (map, thumbnails)
├── pin_grid_spy/ # Source code package
├── static/ # Sidebar CSS/JS assets
├── tests/ # Unit tests (coming soon)
├── main.py # Main executable script
├── requirements.txt # Dependencies
└── README.md # This file

## Testing

This project uses `pytest` for unit testing.

1.  **Install development dependencies:**
    ```bash
    pip install -r requirements-dev.txt
    ```
2.  **Prepare Test Data:** Ensure you have the necessary sample images in the `tests/sample_data/` directory:
    *   `image_with_gps.jpg`: Must contain valid GPS, DateTimeOriginal, and Model EXIF tags. **You need to update the expected values in `tests/test_image_processor.py` to match your specific test image.**
    *   `image_no_gps.jpg`: An image without GPS tags.
    *   `not_an_image.txt`: A simple text file.
3.  **Run tests:**
    ```bash
    pytest
    ```
    Or for more verbose output:
    ```bash
    pytest -v
    ```

## Future Enhancements (Phase 2)

On-demand data fetching from social media APIs (Twitter, Reddit, Telegram).
Optional backend for dynamic querying.
Advanced filtering and search on the map.
See original project brief for more details.