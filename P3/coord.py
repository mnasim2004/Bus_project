import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

# Function to get coordinates for a location
def get_coordinates(location_name, geolocator):
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching {location_name}: {e}")
        return None, None

# Load the Excel file
input_file = "stops.xlsx"  # Replace with your Excel file name
output_file = "stops_with_coordinates.xlsx"
sheet_name = "Sheet1"  # Replace with your sheet name if different

# Read the Excel file
df = pd.read_excel(input_file, sheet_name=sheet_name)

# Initialize the geolocator
geolocator = Nominatim(user_agent="stop_locator")

# Add latitude and longitude columns
latitudes = []
longitudes = []

# Fetch coordinates for each stop
for index, row in df.iterrows():
    stop_name = row['Stops']  # Replace with your column name
    full_location = f"{stop_name}, Trivandrum"  # Add "Trivandrum" to each stop
    print(f"Fetching coordinates for: {full_location}")
    lat, lon = get_coordinates(full_location, geolocator)
    latitudes.append(lat)
    longitudes.append(lon)
    sleep(1)  # Add a delay to avoid overloading the API

# Add results to the DataFrame
df['Latitude'] = latitudes
df['Longitude'] = longitudes

# Save the updated Excel file
df.to_excel(output_file, index=False)
print(f"Coordinates saved to: {output_file}")
