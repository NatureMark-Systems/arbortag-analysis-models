import pandas as pd
import matplotlib.pyplot as plt

# Load your data
file_path = '/home/saif/final_codes/gps_test9.csv'
data = pd.read_csv(file_path)

# Calculating the average width for each Scientific_name
average_heights = data.groupby('scientific_name')['width'].mean()

# Create a bar graph for average widths
plt.figure(figsize=(55, 40))  # Adjust the figure size as needed
plt.bar(average_heights.index, average_heights, color='green')

# Set font sizes
title_font_size = 30  # Adjust the font size for the title
axis_label_font_size = 34  # Adjust the font size for the axis labels
axis_ticks_font_size = 26  # Adjust the font size for the axis ticks

# Add labels and title with specified font sizes
plt.xlabel('Scientific name', fontsize=axis_label_font_size)
plt.ylabel('Average Width', fontsize=axis_label_font_size)
plt.title('Average Tree Width', fontsize=title_font_size)

# Rotate the X-axis labels for better readability and adjust font size
plt.xticks(rotation=90, fontsize=axis_ticks_font_size)
plt.yticks(fontsize=axis_ticks_font_size)  # Set the font size for Y-axis ticks

# Adjust the subplot parameters to give some padding
plt.subplots_adjust(bottom=0.3)

# Save the figure as a PNG file
plt.savefig('/home/saif/final_codes/Tree_width.png')

# Display the plot
plt.show()

