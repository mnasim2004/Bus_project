import ast

# Function to read the content of a text file and return a list of lines
def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Parse the combined data from the file
def parse_combined_data(file_path):
    data = read_file(file_path)
    combined_data = {}
    
    # Read the data as dictionary format
    data_str = ''.join(data)
    combined_data = ast.literal_eval(data_str)
    
    return combined_data

# Sort the bus stops by their colors
def sort_stops_by_color(combined_data):
    # Initialize a dictionary to hold lists of stops for each color
    color_dict = {"R": [], "B": [], "Br": [], "G": [], "Y": [], "V": [], "M": []}
    
    # Iterate through the combined data and categorize stops by their colors
    for stop_id, stop_info in combined_data.items():
        grid = stop_info["Grid"]
        stop = stop_info["Stop"]
        colors = stop_info["Colors"]
        
        # Add the stop to the corresponding color categories
        for color in colors:
            if color in color_dict:
                color_dict[color].append({"Grid": grid, "Stop": stop})
    
    return color_dict

# Write the sorted stops by color to a new text file
def write_sorted_data(color_dict, output_file):
    with open(output_file, 'w') as file:
        for color, stops in color_dict.items():
            file.write(f'"{color}": [\n')
            for stop in stops:
                file.write(f'    {{ "Grid": "{stop["Grid"]}", "Stop": "{stop["Stop"]}" }},\n')
            file.write("],\n")

    print(f"Sorted data has been written to '{output_file}'.")

# Main execution
combined_data = parse_combined_data('formatted_combined_data.txt')  # Read the combined data file
sorted_data = sort_stops_by_color(combined_data)  # Sort stops by color
write_sorted_data(sorted_data, 'sorted_by_color.txt')  # Write the result to a new file
