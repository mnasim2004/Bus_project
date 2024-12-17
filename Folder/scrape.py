import json
from openpyxl import Workbook

# Function to reformat routes
def format_routes(routes):
    formatted_routes = {}

    for route_name, stops in routes.items():
        formatted_routes[route_name] = []
        
        for i, stop in enumerate(stops):
            formatted_routes[route_name].append({
                "route": i,
                "Stop": stop
            })
    
    return formatted_routes

# Original routes dictionary
routes = {
    "Red": ["East Port", "Thampanoor", "Ayurveda College", "Statue", "VJT", 
            "Kerala University", "Palayam", "Niyamasabha", "PMG", "LMS", 
            "Museum", "Kanakakunnu", "Manaveeyam Road", "Police Headquarters", 
            "Vazhuthacad", "Police Training College", "Mettukada", "Thycaud Hospital", 
            "Flyover", "Thampanoor","East Port"],
    
    "Blue": ["East Port","Thampanoor", "Ayurveda College", "Uppiddamoodu Bridge", 
             "Vanchiyoor Court", "Pattoor", "General Hospital", "Kerala University", 
             "Palayam", "Niyamasabha", "PMG", "Museum", "Vellayambalam", 
             "Sasthamangalam", "Maruthankuzhy", "Kochar Road", "Edapazhinji", 
             "Jagathy", "Vazhuthakkad", "Bakery Jn", "Jacobs Jn.", 
             "Contonment Gate", "Statue", "Thampanoor","East Port"],
    
    "Brown": ["East Port","Thampanoor","Chenthitta", "Kannettumukku", "Jagathy", "Pangode Market", 
              "Sasthamangalam", "Maruthamangalam", "PTP Nagar", "Vettamukku", 
              "Elippodu", "Valiyavila", "Thirumala", "Poojapura", "Kunchalummoodu", 
              "Karamana", "Killipalam", "Attakulangara Road","East Port"],
    
    "Green": ["East Port","Transport Bhavan", "Vazhapally", "Fort Hospital", "Uppidamoodu Bridge", 
              "Pettah Pallimukku", "Kannamoola", "Kumarapuram", "Medical College", 
              "Murinjapalam", "Pottakuzhy", "Thekkumoodu", "Anadiyil Hospital", 
              "Law College Jn", "Vikas Bhavan Depot", "PMG", "Niyamasabha", 
              "Palayam", "Statue","Ayurveda College","Thampanoor","East Port"],
    
    "Majenta": ["Peroorkada Depot", "Ambalamukku", "Kowdiar", "TTC", "Vellayambalam", 
                "Museum", "LMS", "Palayam", "Statue", "Thampanoor", "Aristo", 
                "Model School", "Bakery", "Palayam", "Niyamasabha", "PMG", 
                "Plammoodu", "Pattom", "Kesavadasapuram", "Pattom", "Kuravankonam", 
                "Kowdiar", "Ambalamukku", "Peroorkada Depot"],
    
    "Yellow": ["Peroorkada Depot", "Ambalamukku", "Kowdiar", "TTC", "Devaswom Board", 
               "Nanthancode", "Museum", "LMS", "Palayam", "VJT", "Kerala University", 
               "Flyover", "Niyamasabha", "PMG", "Plammoodu", "Pattom", "Pottakuzhy", 
               "Medical College", "Ulloor", "Kesavadasapuram", "Paruthipara", "Muttada", 
               "Vayalikada", "Santhwana Jn.", "Ambalamukku", "Peroorkada Depot"],
    
    "Violet": ["Peroorkada Depot", "Oolampara", "HLL", "Paippinmoodu", "Sasthamangalam", 
               "Edapazhanji", "Cotton Hill School", "Vazhuthacaud", "Mettukada", 
               "Thycaud", "Thampanoor", "Ayurveda College", "Statue", "Palayam", 
               "Niyamasabha", "LMS", "Museum", "Vellayambalam", "TTC", "Kowdiar", 
               "Ambalamukku", "Peroorkada Depot"]
}

# Reformat the routes
formatted_routes = format_routes(routes)

# Create a new Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Routes"

# Add headers
ws.append(["Color", "Stop"])

# Add data to the Excel sheet
for route_name, stops in formatted_routes.items():
    for stop_info in stops:
        ws.append([route_name, stop_info["Stop"]])

# Save the Excel file
wb.save("formatted_routes.xlsx")

