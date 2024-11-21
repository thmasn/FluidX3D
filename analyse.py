import csv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

# File path to the .dat file
file_path = "2xforces.dat"
scaleFacX = 8
file_path = "1xforces.dat"
scaleFacX = 4
file_path = "0_5xforces.dat"
scaleFacX = 2
file_path = "0_25xforces.dat"
scaleFacX = 1
file_path = "0_25xforces_1.dat"
scaleFacX = 1
file_path = "1xforces3.dat"
scaleFacX = 2
file_path = "2xforces3.dat"
scaleFacX = 4
file_path = "./bin/export/doubTimeStep3/forces.dat"
file_path = "./bin/export/origTimeStep3/forces.dat"
file_path = "./bin/export/halfTimeStep3/forces.dat"
file_path = "./bin/export/origTimeStep3/forces.dat"
scaleFacX = 1

# Colors for each column
colors = ["black", "red", "green", "blue", "orange", "purple"]

# Read data from the file
data = []
column_names = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    column_names = next(reader)  # Extract the header
    for row in reader:
        # Filter out empty strings caused by trailing commas and convert to floats
        clean_row = [float(value) for value in row if value.strip()]
        data.append(clean_row)

# Transpose data to access columns
data = np.array(data).T

# Mapping values from 0-40000 to 0-200
def map_value(value):
    min_val = -20000
    max_val = 20000
    new_min = 0
    new_max = 200
    return np.interp(value, [min_val, max_val], [new_min, new_max])
    #return new_min + (value - min_val) * (new_max - min_val) / (max_val - min_val)
    # map logarithmically with sign
    mapped = 0
    if value != 0:
        sign = np.sign(value)
        magnitude = np.log1p(abs(value)) / np.log(np.e)  # Logarithmic transform
        mapped = sign * magnitude
    return mapped *10 +100

# Map all data points to the range 0-200
mapped_data = []
for column in data:
    mapped_column = [map_value(value) for value in column]
    mapped_data.append(mapped_column)

# Prepare for plotting
scaleFacY = 10
width = len(data[0])*scaleFacX
height = 200*scaleFacY
background_color = (0, 0, 0)  # Black background

# Create an image
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

def drawHorizontalLine (y):
    draw.line([(0, map_value(y)*scaleFacY), (width - 1, map_value(y)*scaleFacY)], fill=(128, 128, 128), width=1)

# Add a horizontal white line in the middle of the image
drawHorizontalLine(0)
lines = [1, 10, 100, 1000, 10000, -1, -10, -100, -1000, -10000]
for line in lines:
    drawHorizontalLine(line)

# Draw the graph
for col_idx, column_data in enumerate(mapped_data):
    for x in range(1, len(column_data)):
        # Coordinates of the previous and current points
        prev_x, prev_y = x, height - column_data[x - 1]*scaleFacY
        curr_x, curr_y = x, height - column_data[x]*scaleFacY
        # Draw a line connecting the points
        draw.line([(prev_x, prev_y), (curr_x, curr_y)], fill=colors[col_idx % len(colors)], width=1)

# Save the image
output_file = file_path+"_.png"
image.save(output_file)
print(f"Graph saved as {output_file}")