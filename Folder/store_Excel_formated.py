import json
from openpyxl import Workbook

# Load the previously formatted routes from the text file (which is a JSON file)
try:
    with open('sorted_by_color.txt', 'r') as file:
        formatted_routes = json.load(file)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    # Handle the error, for example, by inspecting the file content
    raise

# Create a new Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Routes Data"

# Add headers for Color, Grid, and Stop
ws.append(["Color", "Grid", "Stop"])

# Add data for each route (color) and its stops
for color, stops in formatted_routes.items():
    for stop in stops:
        grid = stop["Grid"]  # Get the route number (Grid)
        stop_name = stop["Stop"]  # Get the stop name
        # Append a new row with color, grid, and stop information
        ws.append([color, grid, stop_name])

# Save the Excel file
wb.save("routes_with_colors.xlsx")
