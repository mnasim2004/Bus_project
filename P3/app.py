from flask import Flask, render_template, request, jsonify
import openrouteservice
import pandas as pd

app = Flask(__name__)

# OpenRouteService API Client
client = openrouteservice.Client(key="5b3ce3597851110001cf6248ee24a26f504d482aa03e245a8b15fc07")

# Constants for carbon emissions
BUS_CO2_PER_KM = 1.7  # kg CO2 per km for the bus
CAR_CO2_PER_PERSON_PER_KM = 0.12  # kg CO2 per person per km for the car


# Read the stops from the Excel file
def load_stops_from_excel():
    df = pd.read_excel('stops_with_coordinates.xlsx')  # Update with your file path
    stops = []
    for _, row in df.iterrows():
        stop_name = row['Stops']
        latitude = row['Latitude']
        longitude = row['Longitude']
        if pd.notnull(latitude) and pd.notnull(longitude):
            stops.append({"name": stop_name, "lat": latitude, "lng": longitude})
    return stops

@app.route('/')
def index():
    stops = load_stops_from_excel()
    return render_template('index.html', stops=stops)

@app.route('/calculate_route')
def calculate_route():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    # Split the coordinates correctly and map to [longitude, latitude]
    origin_coords = list(map(float, origin.split(',')))
    destination_coords = list(map(float, destination.split(',')))

    try:
        # Fetch the route from OpenRouteService
        route = client.directions(
            coordinates=[origin_coords, destination_coords],
            profile='driving-car',
            format='geojson'
        )

        # Extract the distance in meters and convert to kilometers
        distance_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000
        
        # Extract the route geometry (coordinates of the path)
        route_geometry = route['features'][0]['geometry']['coordinates']

        # Return the distance and route geometry
        return jsonify({
            "distance_km": round(distance_km, 2),
            "route_geometry": route_geometry  # Sending the route geometry back
        })
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/calculate_carbon_footprint')
def calculate_carbon_footprint():
    distance_km = float(request.args.get('distance_km'))
    num_passengers = int(request.args.get('num_passengers'))

    # Calculate the carbon footprint for the bus
    bus_emissions = BUS_CO2_PER_KM * distance_km # in kg CO2

    # Calculate the carbon footprint for car travel (per person)
    car_emissions = CAR_CO2_PER_PERSON_PER_KM * distance_km * num_passengers  # in kg CO2

    # Return the results
    return jsonify({
        "bus_emissions": round(bus_emissions, 2),
        "car_emissions": round(car_emissions, 2),
        "emissions_saved": round(car_emissions - bus_emissions, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
