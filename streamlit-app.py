import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import gdown
import os
import json

def download_from_gdrive(gdrive_url, output_path="temp_geojson.geojson"):
    # Extract the file ID from the URL
    file_id = gdrive_url.split('/d/')[1].split('/')[0]
    gdrive_download_url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(gdrive_download_url, output_path, quiet=False)
    return output_path


# Title
st.title("GeoJSON Viewer with Satellite Basemap")

# Get URL from Streamlit's query parameters
query_params = st.experimental_get_query_params()
geojson_url = query_params.get("geojson_url", [None])[0]

if geojson_url:
    # Check if it's a Google Drive link
    if "drive.google.com" in geojson_url:
        # Download the file locally
        geojson_path = download_from_gdrive(geojson_url)
        with open(geojson_path, 'r') as file:
            geojson_data = json.load(file)
        os.remove(geojson_path)  # Clean up downloaded file after use
    else:
        # Standard HTTP URL for direct access
        try:
            response = requests.get(geojson_url)
            response.raise_for_status()  # Ensure URL is valid
            geojson_data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error loading GeoJSON data: {e}")
            geojson_data = None

    if geojson_data:
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

        # Add GeoJSON overlay
        geojson_layer = folium.GeoJson(
            geojson_data,
            name="GeoJSON Data"
        ).add_to(m)

        # Center and zoom on the GeoJSON data
        bounds = geojson_layer.get_bounds()
        m.fit_bounds(bounds)

        # Add a layer control to switch between basemaps
        folium.LayerControl().add_to(m)

        # Display the map in Streamlit
        st_folium(m, width=700, height=500)

else:
    st.warning("Please provide a GeoJSON URL as a query parameter, e.g., `?geojson_url=<your_geojson_url>`")
