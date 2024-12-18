import pandas as pd
import folium

# Load the Excel file with stops and coordinates
input_file = "stops_with_coordinates.xlsx"  # Replace with your file name
df = pd.read_excel(input_file)

# Create a base map centered around Trivandrum (default coordinates)
map_center = [8.5241, 76.9366]  # Latitude and Longitude of Trivandrum city center
stop_map = folium.Map(location=map_center, zoom_start=12)

# Add markers for each stop
for index, row in df.iterrows():
    stop_name = row['Stops']  # Replace with the actual column name for stop names
    latitude = row['Latitude']
    longitude = row['Longitude']
    
    if pd.notnull(latitude) and pd.notnull(longitude):  # Check for valid coordinates
        folium.Marker(
            location=[latitude, longitude],
            popup=f"{stop_name}",  # Tooltip or popup with stop name
            tooltip=stop_name,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(stop_map)

# Save the map to an HTML file
output_map_file = "trivandrum_stops_map.html"
stop_map.save(output_map_file)
print(f"Interactive map saved to: {output_map_file}")

