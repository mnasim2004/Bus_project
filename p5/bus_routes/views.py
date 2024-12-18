import pandas as pd
import networkx as nx
from django.shortcuts import render

def load_excel_data(file_path):
    """ Load Excel data containing stop details """
    data = pd.read_excel(file_path)
    return data

def calculate_distance(grid1, grid2):
    """ Calculate distance between two grid points. """
    def grid_to_coordinates(grid):
        letter, number = grid[0], int(grid[1:])
        x = ord(letter.upper()) - ord('A')  # Convert letter to numeric x-coordinate
        y = number - 1  # Numeric y-coordinate
        return (x, y)

    coord1 = grid_to_coordinates(grid1)
    coord2 = grid_to_coordinates(grid2)
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5



def find_all_paths(G, start, end):
    """ Find all paths from start to end with straight routes first, then 2-line routes. """
    if start not in G or end not in G:
        return [], None

    all_paths = []
    shortest_path = None
    min_distance = float('inf')

    # Find direct paths (straight buses)
    for path in nx.all_simple_paths(G, source=start, target=end):
        # Check the number of line changes
        line_changes = count_line_changes(G, path)
        if line_changes == 0:
            all_paths.append((path, calculate_path_distance(G, path)))
            avg_distance = calculate_path_distance(G, path) / len(path)

            if avg_distance < min_distance:
                shortest_path = path
                min_distance = avg_distance

    # If no direct path is found, find paths with one line change
    if not all_paths:
        for path in nx.all_simple_paths(G, source=start, target=end):
            line_changes = count_line_changes(G, path)
            if line_changes == 1:
                all_paths.append((path, calculate_path_distance(G, path)))
                avg_distance = calculate_path_distance(G, path) / len(path)

                if avg_distance < min_distance:
                    shortest_path = path
                    min_distance = avg_distance

    return all_paths, shortest_path

def count_line_changes(G, path):
    """ Count the number of line changes in a given path. """
    last_color = None
    line_changes = 0
    for i in range(len(path) - 1):
        edge_data = G.get_edge_data(path[i], path[i + 1])
        if not edge_data:
            continue
        color = edge_data['color']
        if color != last_color:
            line_changes += 1
        last_color = color
    return max(line_changes - 1, 0)



def calculate_path_distance(G, path):
    """ Calculate the total distance covered by a given path. """
    total_distance = 0
    for i in range(len(path) - 1):
        edge_data = G.get_edge_data(path[i], path[i + 1])
        if not edge_data:
            continue
        weight = edge_data.get('weight', 0)
        total_distance += weight
    return total_distance



def build_graph(data):
    """ Build a graph using NetworkX where stops are nodes and edges are based on routes. """
    G = nx.DiGraph()

    # Add stops as nodes
    for _, row in data.iterrows():
        G.add_node(row['Stop'], color=row['Color'], grid=row['Grid'])

    # Add edges between consecutive stops on the same color route
    for color in data['Color'].unique():
        stops = data[data['Color'] == color]
        for i in range(1, len(stops)):
            stop1 = stops.iloc[i - 1]['Stop']
            stop2 = stops.iloc[i]['Stop']
            grid1 = stops.iloc[i - 1]['Grid']
            grid2 = stops.iloc[i]['Grid']
            distance = calculate_distance(grid1, grid2)
            weight = 5 + distance  # 5 mins base + distance penalty
            G.add_edge(stop1, stop2, weight=weight, color=color)

    return G

def find_best_route(G, start, end):
    """ Find the best route prioritizing line changes, followed by travel time. """
    if start not in G or end not in G:
        return None, None, None, None

    # Initialize the best path variables
    best_path = None
    best_color_changes = float('inf')
    best_total_weight = float('inf')
    best_route_colors = None

    # Get all paths using all_simple_paths (prioritizing correctness over efficiency for this case)
    all_paths = list(nx.all_simple_paths(G, source=start, target=end))
    
    for path in all_paths:
        total_weight = 0
        color_changes = 0
        route_colors = []
        last_color = None

        # Calculate the total weight and color changes for the current path
        for i in range(len(path) - 1):
            edge_data = G.get_edge_data(path[i], path[i + 1])
            color = edge_data['color']
            weight = edge_data['weight']
            total_weight += weight

            # Check for color changes
            if color != last_color:
                color_changes += 1
                route_colors.append(color)
            last_color = color

        # Update the best path based on fewer color changes, or equal changes with lower weight
        if (color_changes < best_color_changes) or \
           (color_changes == best_color_changes and total_weight < best_total_weight):
            best_path = path
            best_color_changes = color_changes
            best_total_weight = total_weight
            best_route_colors = route_colors

    # If no valid path exists
    if best_path is None:
        return None, None, None, None

    return best_path, best_total_weight, best_color_changes, best_route_colors


def user_interface(request):
    """ Django view to handle user interaction for finding routes. """
    file_path = 'formatted_routes.xlsx'  # Path to your Excel file
    data = load_excel_data(file_path)
    G = build_graph(data)

    # Collect unique stops for dropdown
    stops = data['Stop'].unique()

    if request.method == 'POST':
        start_stop = request.POST.get('start_stop')
        end_stop = request.POST.get('end_stop')

        # Find all paths and the shortest path
        all_paths, shortest_path = find_all_paths(G, start_stop, end_stop)

        # Prepare paths with their average distances
        paths_with_details = [
            {
                'path': path,
                'total_distance': total_distance,
                'avg_distance': total_distance / len(path),
                'line_changes': count_line_changes(G, path)
            }
            for path, total_distance in all_paths
        ]

        return render(request, 'bus_routes/result.html', {
            'paths_with_details': paths_with_details,
            'shortest_path': shortest_path,
            'stops': stops,
        })

    return render(request, 'bus_routes/index.html', {
        'stops': stops,
    })