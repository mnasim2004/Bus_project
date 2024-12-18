# Function to read the content of a text file and return a list of lines
def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Read stop data and color data from their respective files
stop_data = read_file('stop.txt')
color_data = read_file('color.txt')

# Initialize an empty dictionary to store the combined data
combined_data = {}

# Iterate through the stop data and color data to combine them
for i in range(len(stop_data)):
    grid_stop = stop_data[i].split(" | ")
    
    # Check if the line contains exactly two parts (Grid and Stop)
    if len(grid_stop) == 2:
        grid = grid_stop[0]
        stop = grid_stop[1]
        
        # Get colors, split them by commas, and remove any extra spaces
        colors = set(color.strip() for color in color_data[i].split(","))
        
        # Add the combined data to the dictionary
        combined_data[i+1] = {"Grid": grid, "Stop": stop, "Colors": colors}
    else:
        # Handle cases where the line doesn't contain the expected format
        print(f"Skipping invalid line: {stop_data[i]}")

# Write the combined dictionary to a new text file with a better format
with open('combined_data.txt', 'w') as file:
    for key, value in combined_data.items():
        file.write(f"{key}: {{\n")
        file.write(f"    \"Grid\": \"{value['Grid']}\",\n")
        file.write(f"    \"Stop\": \"{value['Stop']}\",\n")
        file.write(f"    \"Colors\": {value['Colors']}\n")
        file.write("}\n\n")

print("Combined data has been written to 'combined_data.txt' with line breaks.")
