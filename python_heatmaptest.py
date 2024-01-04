import pandas as pd
import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap

def add_matching_gradient_legend_to_map(folium_map, title, vmin, vmax):
    """
    Add a gradient legend to the folium map that matches the heatmap color scheme.
    """
    colors = ['#00FF00', '#FFFF00', '#FFA500', '#FF0000']  # green to red
    colormap = LinearColormap(colors, vmin=vmin, vmax=vmax)
    colormap.caption = title
    folium_map.add_child(colormap)

# Load the dataset
file_path = 'gps_test7.csv'  # Update this with the path to your dataset
data = pd.read_csv(file_path)

# Prepare data for the heatmap
heat_data = [[row['lat'], row['long'], row['heat_level']] for index, row in data.iterrows()]

# Create the map centered around the average coordinates
map_center = [data['lat'].mean(), data['long'].mean()]
map = folium.Map(location=map_center, zoom_start=12)

# Add HeatMap to the map
HeatMap(heat_data).add_to(map)

# Add the matching gradient legend to the map
add_matching_gradient_legend_to_map(map, "Heat Level", 1, 100)

# Save the map
map.save('heatmap_with_matching_legend.html')

