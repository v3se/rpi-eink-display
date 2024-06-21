import plotly.graph_objects as go
import plotly.io as pio
import requests
from datetime import datetime

URL = ""
direction_mapping = {
    'SingleUp': '↑',
    'SingleDown': '↓',
    'Flat': '→',
    'FortyFiveUp': '↗',
    'FortyFiveDown': '↘',
}

def custom_round(number):
    # Check if the absolute value is less than 0.5
    return 0 if abs(number) < 0.5 else round(number)

def format_nightscout_data(data):
    sgv_mmol = round(data[0]['sgv'] * 0.0555, 1)  # Convert to mmol
    sgv_10min = round(data[9]['sgv'] * 0.0555, 1)  # Convert to mmol
    epoch_timestamp = data[0]['date'] / 1000
    timestamp_datetime = datetime.fromtimestamp(epoch_timestamp)
    current_datetime = datetime.now()
    time_difference = current_datetime - timestamp_datetime
    minutes_ago = str(custom_round(time_difference.total_seconds() / 60))

    return {
        'sgv': sgv_mmol,
        'sgv_10min_ago': sgv_10min,
        'minutes_ago': minutes_ago,
        'direction': direction_mapping[data[0]["direction"]]
    }

def fetch_nightscout_data():
    # Implement your API request logic here
    response = requests.get(URL)
    return format_nightscout_data(response.json())

def main():
    # Set the dimensions for a 4.2-inch screen at 96 DPI
    dpi = 96  # dots per inch
    screen_size_inches = 4.2
    width_pixels = screen_size_inches * dpi
    aspect_ratio = 9 / 16  # for a 16:9 aspect ratio
    height_pixels = width_pixels * aspect_ratio
    data = fetch_nightscout_data()

    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = data["sgv"],
        mode = "gauge+number+delta",
        title = {'text': "SGV"},
        delta = {'reference': data["sgv_10min_ago"]},
        gauge = {'axis': {'range': [None, 25]},
                'steps' : [
                    {'range': [0, 3.8], 'color': "grey"},
                    {'range': [3.8, 10.8], 'color': "lightgrey"},
                    {'range': [10.8, 30], 'color': "yellow"}],
                'bar': {'color': "black"}
                }))

    fig.update_layout(
        margin=dict(l=19, r=19, t=50, b=20)  # Adjust margins to make the gauge larger
    )

    pio.write_image(fig, './sgv_gauge.png', width=width_pixels, height=height_pixels)
    print("Image saved successfully!")

if __name__ == "__main__":
    main()
