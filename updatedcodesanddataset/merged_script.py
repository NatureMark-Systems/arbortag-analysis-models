import concurrent.futures
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from PIL import Image, ImageDraw, ImageFont
import textwrap

def run_script(script_name):
    """Function to run a script and return its output"""
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    return result.stdout

# List of script names to be run
scripts = ['python_width.py', 'python_height.py', 'python_distribution.py', 'python_stats.py', 
           'python_diversity_png1.py', 'python_heatmap_png1.py']

# Run scripts concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(run_script, scripts)

    for script, result in zip(scripts, results):
        print(f"Output of {script}:")
        print(result)
        print("-" * 40)

# --- Statistical Analysis from python_stats.py ---
# Load your data
file_path = '/home/saif/final_codes/gps_test9.csv'  # Replace with the path to your CSV file
data = pd.read_csv(file_path)

# Calculate the most and least abundant scientific names and their counts
value_counts = data['scientific_name'].value_counts()
most_abundant = value_counts.idxmax()
least_abundant = value_counts.idxmin()
most_abundant_count = value_counts.max()
least_abundant_count = value_counts.min()

# Calculate the highest and lowest height and width for each scientific name
highest_height = data.groupby('scientific_name')['height'].max()
lowest_height = data.groupby('scientific_name')['height'].min()
highest_width = data.groupby('scientific_name')['width'].max()
lowest_width = data.groupby('scientific_name')['width'].min()

# Extracting the scientific names and actual values for the highest and lowest heights and widths
tallest_height = highest_height.max()
tallest_height_name = highest_height.idxmax()
shortest_height = lowest_height.min()
shortest_height_name = lowest_height.idxmin()

widest_width = highest_width.max()
widest_width_name = highest_width.idxmax()
slimmest_width = lowest_width.min()
slimmest_width_name = lowest_width.idxmin()

# Calculate the count of trees for the species with the highest and lowest height and width
highest_height_count = data[data['scientific_name'] == tallest_height_name]['height'].count()
lowest_height_count = data[data['scientific_name'] == shortest_height_name]['height'].count()
highest_width_count = data[data['scientific_name'] == widest_width_name]['width'].count()
lowest_width_count = data[data['scientific_name'] == slimmest_width_name]['width'].count()

# Calculate the highest and lowest carbon sequestration for each scientific name
highest_carbon_seq = data.groupby('scientific_name')['carbon_seq'].max()
lowest_carbon_seq = data.groupby('scientific_name')['carbon_seq'].min()

# Extracting the scientific names and values for the highest and lowest carbon sequestration
highest_carbon_seq_name = highest_carbon_seq.idxmax()
highest_carbon_seq_value = highest_carbon_seq.max()
lowest_carbon_seq_name = lowest_carbon_seq.idxmin()
lowest_carbon_seq_value = lowest_carbon_seq.min()

# --- PDF Generation functionality ---
A4_SIZE = (2480, 3508)  # A4 size in pixels at 300 DPI

def draw_multiline_text(draw, text, position, font, max_width):
    lines = textwrap.wrap(text, width=max_width)
    y = position[1]
    for line in lines:
        line_width, line_height = draw.textsize(line, font=font)
        x = (A4_SIZE[0] - line_width) / 2
        draw.text((x, y), line, font=font, fill="black")
        y += line_height

def resize_image_to_a4(img):
    img.thumbnail(A4_SIZE, Image.ANTIALIAS)
    background = Image.new('RGB', A4_SIZE, color='white')
    x_offset = (A4_SIZE[0] - img.width) // 2
    y_offset = (A4_SIZE[1] - img.height) // 2
    background.paste(img, (x_offset, y_offset))
    return background

def convert_images_to_pdf_with_custom_text_and_font(image_files, texts, font_sizes, output_pdf):
    if len(image_files) - 1 != len(texts) or len(image_files) - 1 != len(font_sizes):
        raise ValueError("The number of images, texts, and font sizes must be the same")

    images = []
    front_img = Image.open(image_files[0])
    if front_img.mode == 'RGBA':
        front_img = front_img.convert('RGB')
    front_img = resize_image_to_a4(front_img)
    images.append(front_img)

    for file, text, font_size in zip(image_files[1:], texts, font_sizes):
        img = Image.open(file)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img = resize_image_to_a4(img)
        images.append(img)

        blank_img = Image.new('RGB', A4_SIZE, color='white')
        draw = ImageDraw.Draw(blank_img)
        font_path = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        font = ImageFont.truetype(font_path, font_size)

        wrapped_text = textwrap.wrap(text, width=40)
        text_height = sum(draw.textsize(line, font=font)[1] for line in wrapped_text)
        y_start = (A4_SIZE[1] - text_height) // 2
        draw_multiline_text(draw, text, (0, y_start), font, 40)
        images.append(blank_img)

    images[0].save(output_pdf, save_all=True, append_images=images[1:])

# Image files and custom text
image_files = ['Front.png', 'Tree_width.png', 'Tree_height.png', 'Distribution.png', 
               'diversity_map.png', 'carbon_seq_heatmap.png', 'summary_table.png']

custom_texts = [
    f"Average Width: Detailed bargraph above showing the average widths of the trees for each species. The total width for that species is taken and divided by the total number of trees for that species to give an average estimate of the width for that species. The widest species is {widest_width_name} with the width of {widest_width}. The narrowest species is {slimmest_width_name} with the width of {slimmest_width}.",
    f"Average Height: Detailed bargraph above showing the average heights of the trees for each species.The total height for that species is taken and divided by the total number of trees for that species to give an average estimate of the height for that species. The tallest species is {tallest_height_name} with the height of {tallest_height}. The shortest species is {shortest_height_name} with the height of {shortest_height}.",
    f"Species Diversity: Detailed Piechart above showing the breakdown of all the species in the dataset and their total percentage. Each colour in the piechart represents its corresponding species in the figure legend. The percentage values show how much of the total that species makes. The most abundant species is {most_abundant} with a count of {most_abundant_count}. The least abundant species is {least_abundant} with a count of {least_abundant_count}.",
    f"Species Distribution: Above image maps each tree to its exact coordinates with each species colour coded. Each colour coded dot is unique to each colour coded tree species in the legend. NOTE: As these are exact geocords some dots may overlap based on how close the trees are to each other.",
    f"Carbon Sequestration: Above heatmap shows the level of carbon sequestered by each tree. As the scale above shows, the lower the ability of the tree to sequester carbon the closer it is to green which is the lower range. The more efficiant the tree at sequestering carbon the closer it is to red as can be compared on the scale. The highest carbon sequestration is by {highest_carbon_seq_name} with a value of {highest_carbon_seq_value}. The lowest is by {lowest_carbon_seq_name} with a value of {lowest_carbon_seq_value}.",
    "Key Statistics: Provided above are some key statistics about the dataset."
]

custom_font_sizes = [70, 70, 70, 70, 70, 70]

# Output PDF file name
output_pdf = 'combined_images_with_custom_text_and_fonts.pdf'

# Generate the PDF
convert_images_to_pdf_with_custom_text_and_font(image_files, custom_texts, custom_font_sizes, output_pdf)

