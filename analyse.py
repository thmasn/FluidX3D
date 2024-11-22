import csv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

# File path to the .dat file
file_path = "2xforces.dat"
file_path = "1xforces.dat"
file_path = "0_5xforces.dat"
file_path = "0_25xforces.dat"
file_path = "0_25xforces_1.dat"
file_path = "1xforces3.dat"
file_path = "2xforces3.dat"
file_path = "./bin/export/halfTimeStep3/forces.dat"
file_path = "./bin/export/origTimeStep3/forces.dat"
file_path = "./bin/export/doubTimeStep3/forces.dat"

# Colors for each column
colors = [(0,0,0), (200,0,0), (0,128,0), (0,0,255), (128,128,0), (0,128,128), (128,0,128)]

# Read data from the file, gives us an array of csv rows (time / x) with an array of values (x, y, z)
data = []
column_names = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    column_names = next(reader)  # Extract the header
    for row in reader:
        # Filter out empty strings caused by trailing commas and convert to floats
        clean_row = [float(value) for value in row if value.strip()]
        data.append(clean_row)

# Transpose data to access columns, gives us an array of values (x, y, z) with an array of data points (time / x)
data = np.array(data).T

# create average history
startAverageX = int(len(data[0]) / 2)
averaged_data = []
totals = []
sample = []

for column in data: # go through each value
    total = 0.0
    samples = 0
    averaged_points = []
    for x in range(startAverageX, len(column)): # go through data points in second half
        total += column[x]
        samples += 1
        averaged_points.append(total / samples)
    totals.append(0.0)
    sample.append(0)
    averaged_data.append(averaged_points)

# Prepare for plotting
scaleFacY = 4 #10
width = len(data[0])
height = 200*scaleFacY
background_color = (0, 0, 0)  # Black background

# Mapping values from 0-40000 to 0-200
def map_value(value):
    min_val = -5000
    max_val = 5000
    new_min = height
    new_max = 0
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
# Map averages data
mapped_averaged_data = []
for column in averaged_data:
    mapped_column = [map_value(value) for value in column]
    mapped_averaged_data.append(mapped_column)

# Create an image
image = Image.new("RGB", (width, height), background_color)
pixels = image.load()  # Access pixel data for additive blending

def add_colors(color1, color2):
    return tuple(min(c1 + c2, 255) for c1, c2 in zip(color1, color2))

# Function to draw a line with additive blending
def draw_line(xy, fill, lineWidth = 1):
    #print("drawing line"+str(xy))
    start, end = xy
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steps = int(max(dx, dy, 1))  # Determine the number of interpolation steps
    #print(str(dx)+","+str(dy)+","+str(steps))
    for step in range(steps+1):
        t = np.float64(step) / np.float64(steps)
        interp_x = int(x1 + t * np.float64(x2 - x1))
        interp_y = int(y1 + t * np.float64(y2 - y1))
        if interp_x >= width or interp_x < 0 or interp_y >= height or interp_y < 0:
            #print("outside of image area!" + str(interp_x)+","+str(interp_y))
            pass
        else:
            pixels[interp_x, interp_y] = add_colors(pixels[interp_x, interp_y], fill)

def drawHorizontalLine(y, color):
    draw_line([(0, map_value(y)), (width - 1, map_value(y))], fill=color)#, width=1

# Add a horizontal white line in the middle of the image
drawHorizontalLine(0, (128, 128, 128))
#lines = [1, 10, 100, 1000, 10000, -1, -10, -100, -1000, -10000]
#for line in lines:
#    drawHorizontalLine(line, (64, 64, 64))
for x in range(-9, 10):
    line = x *1000
    drawHorizontalLine(line, (32, 32, 32))

# Draw the graph
for col_idx, column_data in enumerate(mapped_data):
    for x in range(1, len(column_data)):
        #print(x)
        # Coordinates of the previous and current points
        prev_y = column_data[x - 1]
        curr_y = column_data[x]
        # Draw a line connecting the points
        draw_line([(x, prev_y), (x, curr_y)], fill=colors[col_idx % len(colors)])#, width=1
# Draw averages graph
for col_idx, column_data in enumerate(mapped_averaged_data):
    for x in range(startAverageX, len(column_data)):
        # Coordinates of the previous and current points
        prev_y = column_data[x - 1]
        curr_y = column_data[x]
        # Draw a line connecting the points
        draw_line([(x, prev_y), (x, curr_y)], fill=colors[col_idx % len(colors)])#, width=1

# Save the image
output_file = file_path+"__.png"
image.save(output_file)
print(f"Graph saved as {output_file}")