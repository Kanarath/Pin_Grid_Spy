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

# pin_grid_spy/map_generator.py
import folium
from folium.plugins import MarkerCluster, MeasureControl
import logging
import pathlib
import html

from . import config

log = logging.getLogger(__name__)

def create_map(image_data_list: list, output_file: pathlib.Path):
    """Generates the Folium map with markers, clusters, tools, and sidebar."""
    if not image_data_list:
        log.warning("No image data with GPS coordinates provided. Map will be empty.")
        map_center = config.DEFAULT_MAP_LOCATION
        map_zoom = config.DEFAULT_MAP_ZOOM
    else:
        # Calculate map center based on average coordinates
        avg_lat = sum(item['latitude'] for item in image_data_list) / len(image_data_list)
        avg_lon = sum(item['longitude'] for item in image_data_list) / len(image_data_list)
        map_center = [avg_lat, avg_lon]
        map_zoom = 6 # Zoom in a bit if there's data

    # --- Initialize Map ---
    log.info(f"Initializing map centered at {map_center}, zoom {map_zoom}")
    m = folium.Map(location=map_center, zoom_start=map_zoom, tiles="OpenStreetMap")

    # --- Add Marker Cluster ---
    marker_cluster = MarkerCluster().add_to(m)

    # --- Add Markers ---
    log.info(f"Adding {len(image_data_list)} markers to the map.")
    for data in image_data_list:
        # Sanitize data for HTML display
        thumb_rel_path_html = html.escape(data['thumbnail_rel_path'])
        datetime_html = html.escape(data['datetime'])
        model_html = html.escape(data['model'])
        original_path_html = html.escape(data['original_path'])
        lat, lon = data['latitude'], data['longitude']
        google_maps_link = config.GOOGLE_MAPS_URL_TEMPLATE.format(lat=lat, lon=lon)

        # Create Popup HTML content
        popup_html = f"""
        <b>Date:</b> {datetime_html}<br>
        <b>Model:</b> {model_html}<br>
        <a href="{google_maps_link}" target="_blank">Open in Google Maps</a><br>
        <hr>
        <img src="{thumb_rel_path_html}" alt="Thumbnail" style="max-width:180px;"><br>
        <small><i>Path: {original_path_html}</i></small>
        """
        # Use IFrame for potentially complex HTML, or just Html for simple cases
        # iframe = folium.IFrame(html=popup_html, width=220, height=250)
        # popup = folium.Popup(iframe, max_width=250)
        popup = folium.Popup(popup_html, max_width=250)


        folium.Marker(
            location=[lat, lon],
            popup=popup,
            tooltip=f"Date: {data['datetime']}" # Tooltip on hover
        ).add_to(marker_cluster)

    # --- Add Map Tools ---
    MeasureControl(position='topleft', primary_length_unit='meters').add_to(m)
    folium.LayerControl().add_to(m) # Allows switching base maps if more are added

    # --- Add Sidebar ---
    log.info("Injecting Leaflet-Sidebar-v2 components.")

    # 1. Add Sidebar CSS to <head>
    sidebar_css_link = f'<link rel="stylesheet" href="{config.SIDEBAR_CSS_PATH}">'
    m.get_root().header.add_child(folium.Element(sidebar_css_link))

    # 2. Add Sidebar HTML structure before closing </body>
    #    Make sure paths in href/src are relative to the map.html file location
    sidebar_html = f"""
    <div id="sidebar" class="leaflet-sidebar collapsed">
        <!-- Nav tabs -->
        <div class="leaflet-sidebar-tabs">
            <ul role="tablist">
                <li><a href="#notes" role="tab"><i class="fa fa-sticky-note" aria-hidden="true"></i></a></li>
                <li><a href="#info" role="tab"><i class="fa fa-info" aria-hidden="true"></i></a></li>
            </ul>
        </div>

        <!-- Tab panes -->
        <div class="leaflet-sidebar-content">
            <div class="leaflet-sidebar-pane" id="notes">
                <h1 class="leaflet-sidebar-header">
                    Analyst Notes
                    <span class="leaflet-sidebar-close"><i class="fa fa-caret-left"></i></span>
                </h1>
                <p>Use this space to jot down findings, observations, or questions related to the map points.</p>
                <textarea id="notes-area" style="width: 95%; height: 300px; margin-top: 10px;" placeholder="Your notes here..."></textarea>
                <button onclick="saveNotes()">Save Notes</button>
                <button onclick="clearNotes()">Clear Notes</button>
                <p><small>Notes are saved in browser's local storage.</small></p>
            </div>

            <div class="leaflet-sidebar-pane" id="info">
                 <h1 class="leaflet-sidebar-header">
                    Pin Grid Spy Info
                    <span class="leaflet-sidebar-close"><i class="fa fa-caret-left"></i></span>
                </h1>
                <p>Pin Grid Spy - MVP</p>
                <p>This map displays geolocated images found in the input directory.</p>
                <ul>
                    <li>Click marker clusters to zoom in.</li>
                    <li>Click individual markers for details & thumbnails.</li>
                    <li>Use the measure tool (ruler icon) for distances/areas.</li>
                    <li>Use the notes tab to record observations.</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- Need Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    """
    m.get_root().html.add_child(folium.Element(sidebar_html))

    # 3. Add Sidebar JS *and* Initialization Script before closing </body>
    #    Make sure the initialization runs *after* the sidebar JS is loaded and *after* the map ('m') is defined.
    sidebar_js_link_and_init = f"""
    <script src="{config.SIDEBAR_JS_PATH}"></script>
    <script>
        // Wait for the map object to be defined by Folium
        // Note: Folium typically names the map variable 'map_xxxxxxxx...'
        // We assume 'm' here based on the folium object, but need to target the JS map object.
        // A safer way is to wait for DOMContentLoaded or find the map instance.
        // However, Folium places its map init script late, so this usually works:
        var map_instance = {{ map_variable }}; // Folium replaces this with the JS map variable name
        var sidebar = L.control.sidebar({{ container: 'sidebar' }}).addTo(map_instance);

        // Simple LocalStorage for Notes
        var notesArea = document.getElementById('notes-area');
        notesArea.value = localStorage.getItem('pinGridSpyNotes') || ''; // Load saved notes

        function saveNotes() {{
            localStorage.setItem('pinGridSpyNotes', notesArea.value);
            alert('Notes saved!');
        }}
        function clearNotes() {{
             if (confirm('Are you sure you want to clear all saved notes?')) {{
                notesArea.value = '';
                localStorage.removeItem('pinGridSpyNotes');
                alert('Notes cleared!');
            }}
        }}
    </script>
    """
    # This uses Folium's internal template variable `map_variable`
    m.get_root().script.add_child(folium.Element(sidebar_js_link_and_init))

    # --- Save Map ---
    log.info(f"Saving map to: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True) # Ensure output dir exists
    m.save(str(output_file))
    log.info("Map generation complete.")