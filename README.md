Trivandrum City Route Planner
Overview
The Trivandrum City Route Planner is a Flask-based web application designed to help users find optimal routes within Trivandrum city. The application integrates modern mapping and routing technologies to calculate distances, estimate travel times, and assess carbon emissions for both bus and car travel. It empowers users to make informed, sustainable transportation choices by visualizing routes and their environmental impact.

Features
Route Optimization
Calculates the shortest route between two stops using OpenRouteService API.
Provides distance, estimated travel time, and route geometry.

Carbon Footprint Analysis
Estimates carbon emissions for bus and car travel.
Highlights environmental savings when choosing public transportation.

Interactive Stop Selection
Dynamically loads stop names and coordinates from an Excel file.
Offers an easy-to-use interface for selecting origin and destination points.

Real-Time Visualization
Displays route geometry on the map for better route understanding.

File Structure
P5/find_path.py
Contains the logic for calculating the best path between stops in Trivandrum city.
Implements algorithms to determine optimal routes while minimizing time and line changes.

P3/app.py
Handles carbon emission calculations and provides a user-friendly interface for comparing environmental impacts of travel modes.
Uses OpenRouteService API to fetch route details and calculate emissions for both bus and car travel.

Technologies Used
Backend: Flask, Python
Frontend: HTML, CSS, JavaScript
API Integration: OpenRouteService for routing and distance calculation
Data Handling: Pandas for processing stop data
Deployment: Flask development server
Setup Instructions
Clone the Repository

bash
Copy code
git clone https://github.com/username/trivandrum-city-route-planner.git
cd trivandrum-city-route-planner
Install Dependencies
Ensure Python is installed on your system, then run:

bash
Copy code
pip install -r requirements.txt
Add Stop Data
Replace stops_with_coordinates.xlsx with your updated Excel file containing stop names, latitudes, and longitudes.

Run the Applications

To find the best path:
bash
Copy code
python P5/find_path.py
To calculate carbon emissions:
bash
Copy code
python P3/app.py
Access the Application
Open a browser and navigate to:

arduino
Copy code
http://127.0.0.1:5000/
Usage
Select Stops
Choose your starting and destination stops from the dropdown menus.

Calculate Route

Use find_path.py to determine the best path with minimized time and line changes.
Use app.py to visualize the route and estimate carbon emissions for bus and car travel.
Carbon Footprint
Compare carbon emissions for bus and car travel using app.py and see how public transport saves on emissions.

Future Enhancements
Integration with real-time traffic data for accurate travel time estimation.
Support for additional travel modes like biking or walking.
Advanced data visualization with maps and graphs.
Localization for wider audience usability.
