import pandas as pd
import folium
import matplotlib.colors as mcolors

def create_colormap(unique_values):
    """
    Create a colormap that maps each unique value to a color.
    """
    colors = list(mcolors.TABLEAU_COLORS.values())  # Using Tableau's color scheme
    color_count = len(colors)

    colormap = {}
    for i, value in enumerate(unique_values):
        colormap[value] = colors[i % color_count]

    return colormap

def plot_points_with_legend(map_obj, data, colormap, column_name):
    """
    Plot points on the map, each with a color based on its value in a specific column.
    """
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['long']],
            radius=5,
            color=colormap[row[column_name]],
            fill=True,
            fill_color=colormap[row[column_name]],
            fill_opacity=0.7
        ).add_to(map_obj)

    # Adding the legend manually
    legend_html = '<div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: {}px; background-color: white; border:2px solid grey; z-index:9999;">'
    legend_html += '<h4 style="margin:10px">{}</h4>'.format(column_name)
    for subregion, color in colormap.items():
        legend_html += '<i style="background: {}; width: 10px; height: 10px; margin-left: 20px; display: inline-block;"></i> {}<br>'.format(color, subregion)
    legend_html += '</div>'
    map_obj.get_root().html.add_child(folium.Element(legend_html.format(20 * len(colormap))))

# Load the dataset
file_path = 'gps_test7.csv'  # Replace with your dataset file path
data = pd.read_csv(file_path)

# Create a color map for the subregions
unique_subregions = data['subregion'].unique()
subregion_colormap = create_colormap(unique_subregions)

# Create the map centered around the average coordinates
map_center = [data['lat'].mean(), data['long'].mean()]
map_with_points = folium.Map(location=map_center, zoom_start=12)

# Plot each point with a color based on its subregion
plot_points_with_legend(map_with_points, data, subregion_colormap, "subregion")

# Save the map
map_with_points.save('map_with_points_and_legend.html')

