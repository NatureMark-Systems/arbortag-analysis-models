import pandas as pd
import matplotlib.pyplot as plt

# Load your data
file_path = '/home/saif/Pytest/gps_test9.csv'
data = pd.read_csv(file_path)

# Calculating the average height for each Arbor_Tag
average_heights = data.groupby('scientific_name')['height'].mean()

# Create a bar graph for average heights
plt.figure(figsize=(15, 8))  # Adjust the figure size as needed
plt.bar(average_heights.index, average_heights, color='maroon')

# Add labels and title
plt.xlabel('Scientific name')
plt.ylabel('Average Height')
plt.title('Average Tree Height')
plt.xticks(rotation=90)  # Rotate the X-axis labels for better readability

# Adjust the subplot parameters to give some padding
plt.subplots_adjust(bottom=0.3)

# Save the figure as a PNG file
plt.savefig('/home/saif/Pytest/average_tree_heights_by_arbor_tag.png')

# Display the plot
plt.show()

