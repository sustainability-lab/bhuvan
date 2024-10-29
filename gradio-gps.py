import gradio as gr

# This function receives latitude and longitude from JavaScript
def get_location(latitude, longitude):
    if latitude and longitude:
        return f"Latitude: {latitude}, Longitude: {longitude}"
    else:
        return "Location not available or permission denied."

# Gradio interface with JavaScript for GPS
with gr.Blocks() as iface:
    gr.Markdown("## Device GPS Location Finder")

    # JavaScript to get GPS and pass it to the Python function
    js = """
    () => {
        navigator.geolocation.getCurrentPosition(
            position => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                // Return latitude and longitude to Gradio input
                gradioApp().querySelector('#latitude input').value = latitude;
                gradioApp().querySelector('#longitude input').value = longitude;
                gradioApp().querySelector('#submit').click();
            },
            error => {
                alert("Geolocation access was denied.");
            }
        );
    }
    """
    latitude = gr.Textbox(label="Latitude", interactive=False, elem_id="latitude", visible=False)
    longitude = gr.Textbox(label="Longitude", interactive=False, elem_id="longitude", visible=False)

    # Button to trigger JavaScript and get GPS
    gps_button = gr.Button("Get GPS Location", elem_id="submit").click(
        get_location, [latitude, longitude], gr.Textbox(label="Result")
    ).then(None, [], _js=js)

# Launch the app
iface.launch()
