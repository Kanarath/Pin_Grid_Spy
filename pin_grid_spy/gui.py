# pin_grid_spy/gui.py

import PySimpleGUI as sg
import pathlib
import logging

# Import necessary components from our project
from . import config, image_processor, map_generator, __main__ as main_module  # Assuming main logic is moved later

log = logging.getLogger(__name__)

# --- Constants for GUI Elements ---
# Keys allow us to identify elements in the event loop
FILE_LIST_KEY = "-FILE_LIST-"
DROP_TARGET_KEY = "-DROP_TARGET-" # Maybe use the file list itself?
STATUS_BAR_KEY = "-STATUS-"
PROCESS_BUTTON_KEY = "-PROCESS-"
MAP_BUTTON_KEY = "-MAP-"
CLEAR_BUTTON_KEY = "-CLEAR-"
SAVE_BUTTON_KEY = "-SAVE-"
LOAD_BUTTON_KEY = "-LOAD-"
NEW_BUTTON_KEY = "-NEW-"

# --- Initial GUI State ---
# We'll store the processed image data here for the current session
# List of dictionaries, like output from image_processor.process_directory
current_session_data = []
# Keep track of file paths added to the listbox to help with duplicates
# Using a set for quick lookups
files_in_list = set()


# --- Helper Functions ---
def update_status(window: sg.Window, message: str):
    """Updates the status bar"""
    if window:
        window[STATUS_BAR_KEY].update(message)

def add_file_to_list(window: sg.Window, filepath: pathlib.Path):
    """Adds a file path to the listbox if not already present."""
    filepath_str = str(filepath)
    if filepath_str not in files_in_list:
        files_in_list.add(filepath_str)
        # Display just the filename initially for cleaner UI
        window[FILE_LIST_KEY].update(values=list(files_in_list)) # Update listbox
        log.debug(f"Added to list: {filepath_str}")
        return True
    else:
        log.debug(f"Duplicate file ignored: {filepath_str}")
        return False

# --- GUI Layout Definition ---
def create_layout():
    """Creates the layout definition for the main window."""

    # Choose a theme
    sg.theme("DarkBlue3") # Explore themes: sg.theme_previewer()

    # Left Column (File Management)
    left_col = [
        [sg.Text("Drop Images Here or Add Manually:")],
        [sg.Listbox(
            values=[],          # Start empty
            size=(50, 15),      # Width (chars), Height (rows)
            key=FILE_LIST_KEY,
            enable_events=True, # Needed to detect clicks/selection if desired later
            # --- Enable Drag and Drop ---
            # Note: This is the primary way PySimpleGUI handles drops on specific elements
            metadata={'drop_target': True}
        )],
        # Maybe add manual "Add File" / "Add Folder" buttons later
        [
            sg.Button("Process Selected/New", key=PROCESS_BUTTON_KEY, tooltip="Process files added to the list"),
            sg.Button("Clear List", key=CLEAR_BUTTON_KEY, tooltip="Remove all files from the list"),
            sg.Button("Generate Map", key=MAP_BUTTON_KEY, tooltip="Create map from successfully processed images")
        ],
    ]

    # Right Column (Session Management & Info)
    right_col = [
        [sg.Text("Session:")],
        [sg.Button("New", key=NEW_BUTTON_KEY, size=(8,1)),
         sg.Button("Save", key=SAVE_BUTTON_KEY, size=(8,1)),
         sg.Button("Load", key=LOAD_BUTTON_KEY, size=(8,1))],
        # Placeholder for potential future info display or settings
        [sg.Multiline(size=(40, 10), disabled=True, background_color='lightgrey', key="-INFO-", autoscroll=True)],
    ]

    # --- Full Layout ---
    layout = [
        [
            sg.Column(left_col, element_justification='left'),
            sg.VSeperator(), # Vertical line separator
            sg.Column(right_col, element_justification='left')
        ],
        # Status Bar at the bottom
        [sg.StatusBar("Ready.", key=STATUS_BAR_KEY, size=(80, 1))]
    ]
    return layout

# --- Main Application Logic ---
def run():
    """Creates the window and runs the main event loop."""
    window = sg.Window("Pin Grid Spy", create_layout(), finalize=True)

    # Make the Listbox element accept drag-and-drop files
    # We use the key we assigned to the Listbox
    window[FILE_LIST_KEY].bind('<DragEnter>', '+DRAGENTER')
    window[FILE_LIST_KEY].bind('<DragLeave>', '+DRAGLEAVE')
    window[FILE_LIST_KEY].bind('<Drop>', '+DROP')

    # Enable Drop globally too just in case element binding is tricky sometimes
    window.bind('<Drop>', '+DROP_WINDOW')


    log.info("GUI Initialized. Waiting for events.")
    # --- Event Loop ---
    while True:
        event, values = window.read()
        log.debug(f"Event: {event}, Values: {values}")

        if event == sg.WINDOW_CLOSED:
            log.info("Window closed by user.")
            break

        # --- Drag and Drop Handling ---
        # PySimpleGUI often returns dropped file paths in the 'values' dictionary
        # associated with the element's key when the event happens.
        # The exact event name ('+DROP', '+DROP_WINDOW') and how values are passed
        # can sometimes vary slightly with PySimpleGUI versions or OS.
        # Let's check both the listbox event and a general window drop event.

        dropped_files_str = None
        if event == FILE_LIST_KEY + '+DROP':
            log.debug("Drop event on Listbox detected.")
            dropped_files_str = values.get(FILE_LIST_KEY)
        elif event == '+DROP_WINDOW': # Check general window drop
            log.debug("Drop event on Window detected.")
            # How files are reported for window drops needs checking; might be in `values` directly?
            # Let's assume it might use the focus element's key or a default key
            dropped_files_str = values.get(FILE_LIST_KEY) or values.get(0) # Try listbox key or default

        if isinstance(dropped_files_str, str) and dropped_files_str:
            update_status(window, "Processing dropped files...")
            # Files are often semicolon-separated in the string
            filepaths = [pathlib.Path(p.strip()) for p in dropped_files_str.split(';') if p.strip()]
            log.info(f"Files dropped: {filepaths}")
            added_count = 0
            for fp in filepaths:
                # Check if it's a file or directory (handle directories later if needed)
                if fp.is_file():
                    # Check extension (optional but good practice)
                    if fp.suffix.lower() in config.SUPPORTED_EXTENSIONS:
                        if add_file_to_list(window, fp):
                            added_count += 1
                    else:
                        log.warning(f"Ignoring unsupported file type: {fp}")
                elif fp.is_dir():
                     # TODO: Implement directory scanning if desired
                     log.warning(f"Directory dropping not yet implemented: {fp}")
                else:
                    log.warning(f"Dropped item is not a file or directory: {fp}")

            update_status(window, f"Added {added_count} new files to the list. Ready.")
            window.refresh() # Ensure UI updates


        # --- Button Clicks ---
        elif event == PROCESS_BUTTON_KEY:
            # TODO: Implement processing logic
            # - Get files from the listbox (maybe only unprocessed ones?)
            # - Call image_processor
            # - Update status / listbox appearance
            update_status(window, "Processing... (Not implemented yet)")
            sg.popup_scrolled("Processing logic not yet implemented.\n\nFiles currently in list:\n" + "\n".join(files_in_list), title="Info")


        elif event == MAP_BUTTON_KEY:
            # TODO: Implement map generation
            # - Use current_session_data
            # - Call map_generator.create_map
            # - Open the map file
            update_status(window, "Generating map... (Not implemented yet)")
            sg.popup("Map generation logic not yet implemented.", title="Info")

        elif event == CLEAR_BUTTON_KEY:
            update_status(window, "Clearing file list...")
            files_in_list.clear()
            current_session_data.clear() # Also clear processed data
            window[FILE_LIST_KEY].update(values=[])
            update_status(window, "File list cleared. Ready.")

        elif event == NEW_BUTTON_KEY:
            # TODO: Implement 'new session' confirmation/logic
            update_status(window, "New Session... (Not implemented yet)")
            sg.popup("New Session logic not yet implemented.", title="Info")

        elif event == SAVE_BUTTON_KEY:
            # TODO: Implement saving session state
            update_status(window, "Saving Session... (Not implemented yet)")
            sg.popup("Save Session logic not yet implemented.", title="Info")

        elif event == LOAD_BUTTON_KEY:
            # TODO: Implement loading session state
            update_status(window, "Loading Session... (Not implemented yet)")
            sg.popup("Load Session logic not yet implemented.", title="Info")

    log.info("Closing GUI.")
    window.close()

if __name__ == '__main__':
    # This is useful if you want to run the GUI directly for testing
    # Setup logging similar to main.py if running this way
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run()