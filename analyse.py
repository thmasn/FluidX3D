import csv
import matplotlib.pyplot as plt
import numpy as np

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
scaleFacY = 20
width = len(data[0])*scaleFacX
height = 200*scaleFacY
fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)

# Set background color to black
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Adjust axes limits and turn off axes
ax.set_xlim(0, width - 1)
ax.set_ylim(0, 200)
ax.axis("off")  # Turn off the axes for a clean graph

# Add a horizontal white line in the middle of the image
ax.axhline(y=map_value(     0), color="white", alpha=0.35, linewidth=1)
lines = [1, 10, 100, 1000, 10000, -1, -10, -100, -1000, -10000]
for line in lines:
    ax.axhline(y=map_value(line), color="white", alpha=0.25, linewidth=2.)

# Plot each column of data
for col_idx, column_data in enumerate(mapped_data):
    x_coords = range(0, len(column_data)*scaleFacX, scaleFacX)
    ax.plot(x_coords, column_data, color=colors[col_idx % len(colors)], alpha=0.5, linewidth=1.5*scaleFacX, label=column_names[col_idx])

# Save the graph to an image file
output_file = file_path+".png"
plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
plt.close()

print(f"Graph saved as {output_file}")
