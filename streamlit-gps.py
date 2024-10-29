import streamlit as st

# HTML + JavaScript to get GPS coordinates
js_code = """
<script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById('latitude').value = latitude;
            document.getElementById('longitude').value = longitude;
            document.getElementById('locationForm').submit();
        },
        (error) => {
            alert("Geolocation access denied.");
        }
    );
</script>
"""

st.title("Device GPS Location Finder")
st.write("Click the button below to get your GPS location.")

# HTML form to send data back to Streamlit
st.components.v1.html(
    f"""
    <form id="locationForm" action="/" method="get">
        <input type="hidden" name="latitude" id="latitude">
        <input type="hidden" name="longitude" id="longitude">
        <input type="button" value="Get GPS Location" onclick="{js_code}">
    </form>
    """,
    height=0,
)

# Display GPS if data is available
latitude = st.experimental_get_query_params().get("latitude", [None])[0]
longitude = st.experimental_get_query_params().get("longitude", [None])[0]

if latitude and longitude:
    st.write(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    st.write("Location not found or permission denied.")
