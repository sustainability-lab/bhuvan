import streamlit as st
import folium
from streamlit_folium import st_folium
import gdown
import os
import json
import requests

# Function to download from Google Drive
def download_from_gdrive(gdrive_url, output_path="temp_file"):
    # Extract the file ID from the URL
    file_id = gdrive_url.split('/d/')[1].split('/')[0]
    gdrive_download_url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(gdrive_download_url, output_path, quiet=False)
    return output_path

# Title
st.title("KML/GeoJSON Viewer with Satellite Basemap")

# Get URL from Streamlit's query parameters
query_params = st.experimental_get_query_params()
file_url = query_params.get("file_url", [None])[0]

if file_url:
    # Check if it's a Google Drive link
    if "drive.google.com" in file_url:
        # Download the file locally
        local_file_path = download_from_gdrive(file_url)
        file_extension = local_file_path.split('.')[-1]
    else:
        # Standard HTTP URL for direct access
        try:
            response = requests.get(file_url)
            response.raise_for_status()  # Ensure URL is valid
            file_extension = file_url.split('.')[-1]

            # Save the content to a local file
            with open("temp_file." + file_extension, 'wb') as file:
                file.write(response.content)
            local_file_path = "temp_file." + file_extension
        except requests.exceptions.RequestException as e:
            st.error(f"Error loading file: {e}")
            local_file_path = None

    if local_file_path:
        # Create map without default tiles
        m = folium.Map(tiles=None)

        # Add Google Maps basemap
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
            attr='Google Maps',
            name='Google Maps',
            overlay=True,
            control=True
        ).add_to(m)

        # Add Google Satellite basemap
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=True,
            control=True
        ).add_to(m)

        # Determine if file is KML or GeoJSON and add accordingly
        if file_extension.lower() == 'kml':
            folium.Kml(local_file_path).add_to(m)
        elif file_extension.lower() == 'geojson':
            with open(local_file_path, 'r') as file:
                geojson_data = json.load(file)
            folium.GeoJson(geojson_data, name="GeoJSON Data").add_to(m)
        else:
            st.error("Unsupported file format. Please provide a KML or GeoJSON file.")
            local_file_path = None

        # Center and zoom on the layer
        if local_file_path:
            bounds = m.get_bounds()  # Adjusting the view to include KML or GeoJSON bounds
            m.fit_bounds(bounds)

        # Add a layer control to switch between basemaps
        folium.LayerControl().add_to(m)

        # Display the map in Streamlit
        st_folium(m, width=700, height=500)

        # Clean up the downloaded file after use
        os.remove(local_file_path)

else:
    st.warning("Please provide a KML or GeoJSON URL as a query parameter, e.g., `?file_url=<your_file_url>`")
