import pandas as pd
import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap
from selenium import webdriver
import time
import os

def add_matching_gradient_legend_to_map(folium_map, title, vmin, vmax):
    colors = ['#00FF00', '#FFFF00', '#FFA500', '#FF0000']  # green to red
    colormap = LinearColormap(colors, vmin=vmin, vmax=vmax)
    colormap.caption = title
    folium_map.add_child(colormap)

# Load the dataset
file_path = 'gps_test9.csv'  # Update this with the path to your dataset
data = pd.read_csv(file_path)

# Prepare data for the heatmap
heat_data = [[row['lat'], row['long'], row['carbon_seq']] for index, row in data.iterrows()]

# Create the map centered around the average coordinates with increased zoom level
map_center = [data['lat'].mean(), data['long'].mean()]
heatmap_map = folium.Map(location=map_center, zoom_start=18)

# Add HeatMap to the map
HeatMap(heat_data).add_to(heatmap_map)

# Add the matching gradient legend to the map
add_matching_gradient_legend_to_map(heatmap_map, "Carbon Sequestration Level", 1, 100)

# Save the map as HTML
html_path = 'carbon_seq_heatmap.html'
heatmap_map.save(html_path)

# Set up Selenium WebDriver for Chromium
options = webdriver.ChromeOptions()
options.binary_location = '/path/to/chromium'  # Specify the path to chromium
options.add_argument('--headless')  # Run Chromium in headless mode (without a UI)
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--window-size=2180x3024')  # Specify window size

driver = webdriver.Chrome(options=options)

# Load the HTML file
full_html_path = 'file://' + os.path.abspath(html_path)
driver.get(full_html_path)

# Give it time to render and take a screenshot
time.sleep(5)  # Adjust time as needed
png_path = 'carbon_seq_heatmap.png'
driver.save_screenshot(png_path)

# Close the browser
driver.quit()

