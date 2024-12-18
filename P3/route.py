import pandas as pd
import openrouteservice
import json

# Load the Excel file with stops and coordinates
input_file = "stops_with_coordinates.xlsx"
df = pd.read_excel(input_file)

# Initialize OpenRouteService client
client = openrouteservice.Client(key="5b3ce3597851110001cf6248ee24a26f504d482aa03e245a8b15fc07")

# Function to calculate the route between two coordinates
def calculate_route(origin_coords, destination_coords):
    try:
        route = client.directions(
            coordinates=[origin_coords, destination_coords],
            profile='driving-car',
            format='geojson'
        )
        # Extract the distance and geometry (coordinates of the path)
        distance = route['features'][0]['properties']['segments'][0]['distance'] / 1000  # meters to km
        geometry = route['features'][0]['geometry']['coordinates']
        return distance, geometry
    except Exception as e:
        return None, None

# Prepare a dictionary to store distances and paths between stops
distance_data = {}

# Loop over each pair of stops
for i, row_i in df.iterrows():
    for j, row_j in df.iterrows():
        if i < j:  # To avoid calculating the same pair twice
            stop_i = row_i['Stops']
            stop_j = row_j['Stops']
            origin_coords = [row_i['Longitude'], row_i['Latitude']]
            destination_coords = [row_j['Longitude'], row_j['Latitude']]
            
            distance, geometry = calculate_route(origin_coords, destination_coords)
            if distance is not None and geometry is not None:
                distance_data[f"{stop_i}-{stop_j}"] = {
                    "distance": round(distance, 2),
                    "coordinates": geometry
                }

# Save the precomputed data to a JSON file
with open('precomputed_routes.json', 'w') as f:
    json.dump(distance_data, f)

print("Precomputed routes and distances saved.")
