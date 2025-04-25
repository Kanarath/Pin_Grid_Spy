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

# tests/test_image_processor.py

import pytest
import pathlib

from PIL import Image

from pin_grid_spy import image_processor, config, utils

# Define paths relative to the test file location or project root
TEST_DIR = pathlib.Path(__file__).parent
SAMPLE_DATA_DIR = TEST_DIR / "sample_data"
IMG_WITH_GPS = SAMPLE_DATA_DIR / "image_with_gps.jpg"
IMG_NO_GPS = SAMPLE_DATA_DIR / "image_no_gps.jpg"
NOT_AN_IMAGE = SAMPLE_DATA_DIR / "not_an_image.txt"
NON_EXISTENT_FILE = SAMPLE_DATA_DIR / "does_not_exist.jpg"

# --- Fixtures ---

@pytest.fixture(scope="module") # Only run once per module
def sample_images_exist():
    """Check if sample image files exist before running tests."""
    if not IMG_WITH_GPS.exists():
        pytest.fail(f"Required test file missing: {IMG_WITH_GPS}")
    if not IMG_NO_GPS.exists():
        pytest.fail(f"Required test file missing: {IMG_NO_GPS}")
    if not NOT_AN_IMAGE.exists():
        pytest.fail(f"Required test file missing: {NOT_AN_IMAGE}")

# --- Tests for create_thumbnail ---

@pytest.mark.usefixtures("sample_images_exist")
def test_create_thumbnail_success(tmp_path):
    """Tests successful thumbnail creation."""
    thumb_dir = tmp_path / "thumbnails"
    thumb_path = thumb_dir / f"{IMG_WITH_GPS.stem}_thumb{IMG_WITH_GPS.suffix}"

    created = image_processor.create_thumbnail(IMG_WITH_GPS, thumb_path)

    assert created is True
    assert thumb_path.exists()
    # Check dimensions (Pillow maintains aspect ratio within the bounds)
    with Image.open(thumb_path) as thumb_img:
        width, height = thumb_img.size
        assert width <= config.THUMBNAIL_SIZE[0]
        assert height <= config.THUMBNAIL_SIZE[1]

@pytest.mark.usefixtures("sample_images_exist")
def test_create_thumbnail_already_exists(tmp_path):
    """Tests thumbnail creation when the file already exists."""
    thumb_dir = tmp_path / "thumbnails"
    thumb_path = thumb_dir / f"{IMG_WITH_GPS.stem}_thumb{IMG_WITH_GPS.suffix}"
    # Create it once
    image_processor.create_thumbnail(IMG_WITH_GPS, thumb_path)
    assert thumb_path.exists()
    # Call again
    created = image_processor.create_thumbnail(IMG_WITH_GPS, thumb_path)
    assert created is True # Should still report success

@pytest.mark.usefixtures("sample_images_exist")
def test_create_thumbnail_not_an_image(tmp_path):
    """Tests thumbnail creation failure for non-image files."""
    thumb_dir = tmp_path / "thumbnails"
    thumb_path = thumb_dir / f"{NOT_AN_IMAGE.stem}_thumb{NOT_AN_IMAGE.suffix}"

    created = image_processor.create_thumbnail(NOT_AN_IMAGE, thumb_path)

    assert created is False
    assert not thumb_path.exists()

# --- Tests for process_image ---

@pytest.mark.usefixtures("sample_images_exist")
def test_process_image_success(tmp_path):
    """Tests processing an image with valid GPS data."""
    thumb_dir = tmp_path / "thumbnails"
    result = image_processor.process_image(IMG_WITH_GPS, thumb_dir)

    assert isinstance(result, dict)
    assert "latitude" in result
    assert "longitude" in result
    assert "datetime" in result
    assert "model" in result
    assert "thumbnail_rel_path" in result

    # --- Update to match test image in case we change image to test with: ---
    EXPECTED_LAT = 40.74341666666667
    EXPECTED_LON = -74.02541666666667
    EXPECTED_DATETIME = "2023:10:27 11:10:00"
    EXPECTED_MODEL = "TestCamera S9"
    # --- End of values to update ---

    assert result["latitude"] == pytest.approx(EXPECTED_LAT) # pytest.approx is good for floats
    assert result["longitude"] == pytest.approx(EXPECTED_LON) # pytest.approx is good for floats
    assert result["datetime"] == EXPECTED_DATETIME
    assert result["model"] == EXPECTED_MODEL

    # Check relative thumbnail path calculation
    expected_thumb_rel_path = f"thumbnails/{IMG_WITH_GPS.stem}_thumb{IMG_WITH_GPS.suffix}"
    assert result["thumbnail_rel_path"] == expected_thumb_rel_path.replace("\\", "/") # Normalize slashes

    # Check thumbnail file was actually created
    expected_thumb_abs_path = tmp_path / expected_thumb_rel_path
    assert expected_thumb_abs_path.exists()


@pytest.mark.usefixtures("sample_images_exist")
def test_process_image_no_gps(tmp_path):
    """Tests processing an image without GPS data."""
    thumb_dir = tmp_path / "thumbnails"
    result = image_processor.process_image(IMG_NO_GPS, thumb_dir)
    assert result is None

@pytest.mark.usefixtures("sample_images_exist")
def test_process_image_not_an_image(tmp_path):
    """Tests processing a non-image file."""
    thumb_dir = tmp_path / "thumbnails"
    result = image_processor.process_image(NOT_AN_IMAGE, thumb_dir)
    assert result is None

def test_process_image_non_existent(tmp_path):
    """Tests processing a non-existent file path."""
    thumb_dir = tmp_path / "thumbnails"
    result = image_processor.process_image(NON_EXISTENT_FILE, thumb_dir)
    assert result is None # Should be handled by try-except FileNotFoundError

# --- Tests for process_directory ---

@pytest.mark.usefixtures("sample_images_exist")
def test_process_directory(tmp_path):
    """Tests processing a directory with various file types."""
    # Setup temporary input directory
    input_dir = tmp_path / "test_input"
    input_dir.mkdir()
    # Copy sample files into temp input directory
    import shutil
    shutil.copy(IMG_WITH_GPS, input_dir)
    shutil.copy(IMG_NO_GPS, input_dir)
    shutil.copy(NOT_AN_IMAGE, input_dir)
    (input_dir / "unsupported.gif").touch() # Add an unsupported image type

    # Setup temporary output directory
    thumb_dir = tmp_path / "test_output_thumbs"

    # Process the directory
    results = image_processor.process_directory(input_dir, thumb_dir)

    # Assertions
    assert isinstance(results, list)
    assert len(results) == 1 # Only the image with GPS should be processed fully

    # Check the content of the result
    result_data = results[0]
    assert result_data["original_path"] == str(input_dir / IMG_WITH_GPS.name)
    assert result_data["latitude"] is not None # Already tested exact value above
    assert result_data["longitude"] is not None

    # Check that only the expected thumbnail was created
    expected_thumb_path = thumb_dir / f"{IMG_WITH_GPS.stem}_thumb{IMG_WITH_GPS.suffix}"
    unexpected_thumb_path = thumb_dir / f"{IMG_NO_GPS.stem}_thumb{IMG_NO_GPS.suffix}"
    assert expected_thumb_path.exists()
    assert not unexpected_thumb_path.exists()