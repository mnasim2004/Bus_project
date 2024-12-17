from django.shortcuts import render
import pandas as pd
import networkx as nx
from .models import Stop
import heapq


def load_excel_data(file_path):
    """ Load Excel data containing stop details """
    data = pd.read_excel(file_path)
    return data

def build_graph(data):
    """ Build a graph using NetworkX """
    G = nx.DiGraph()
    for _, row in data.iterrows():
        G.add_node(row['Stop'], color=row['Color'], grid=row['Grid'])
    for color in data['Color'].unique():
        stops = data[data['Color'] == color]
        for i in range(1, len(stops)):
            stop1 = stops.iloc[i - 1]['Stop']
            stop2 = stops.iloc[i]['Stop']
            grid1 = stops.iloc[i - 1]['Grid']
            grid2 = stops.iloc[i]['Grid']
            distance = calculate_distance(grid1, grid2)
            weight = 5 + distance
            G.add_edge(stop1, stop2, weight=weight, color=color)
    return G

def calculate_distance(grid1, grid2):
    """ Calculate approximate distance between two grid points """
    def grid_to_coordinates(grid):
        letter, number = grid[0], int(grid[1:])
        x = ord(letter.upper()) - ord('A')
        y = number - 1
        return (x, y)

    coord1 = grid_to_coordinates(grid1)
    coord2 = grid_to_coordinates(grid2)
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

# def find_best_route(G, start, end):
#     """ Find the best route with the shortest time and minimized color changes. """
#     if start not in G or end not in G:
#         return None, None, None

#     # Initialize variables to keep track of the best route
#     best_path = None
#     best_total_weight = float('inf')
#     best_color_changes = float('inf')
#     best_route_colors = None

#     # Get all possible paths from start to end (considering all possible paths)
#     all_paths = list(nx.all_simple_paths(G, source=start, target=end))
    
#     for path in all_paths:
#         total_weight = 0
#         color_changes = 0
#         route_colors = []
#         last_color = None
        
#         # Calculate total weight and count color changes for the current path
#         for i in range(len(path) - 1):
#             edge_data = G.get_edge_data(path[i], path[i + 1])
#             color = edge_data['color']
#             distance = edge_data['weight']
#             total_weight += distance

#             # Count color change if color differs from the last one
#             if color != last_color:
#                 color_changes += 1
#                 route_colors.append(color)
#             last_color = color

#         # Compare this path with the previous best one
#         if (color_changes < best_color_changes) or (color_changes == best_color_changes and total_weight < best_total_weight):
#             best_path = path
#             best_total_weight = total_weight
#             best_color_changes = color_changes
#             best_route_colors = route_colors

#     # If no valid path is found
#     if best_path is None:
#         return None, None, None, None

#     return best_path, best_total_weight, best_color_changes, best_route_colors
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

    # Add zero-weight edges for direct connections within the same route to avoid unnecessary line changes
    for color in data['Color'].unique():
        stops = data[data['Color'] == color]['Stop'].tolist()
        for i in range(len(stops)):
            for j in range(i + 1, len(stops)):
                G.add_edge(stops[i], stops[j], weight=0, color=color)
                G.add_edge(stops[j], stops[i], weight=0, color=color)

    # Add small weights for interchanges between routes (minimize color changes)
    shared_stops = data['Stop'].value_counts()[data['Stop'].value_counts() > 1].index
    for stop in shared_stops:
        routes = data[data['Stop'] == stop]['Color'].unique()
        for i in range(len(routes)):
            for j in range(i + 1, len(routes)):
                G.add_edge(stop, stop, weight=2, color='interchange')
    
    return G
def find_best_route(G, start, end):
    """ Find the best route with minimized line changes, and within that, minimized travel time. """
    if start not in G or end not in G:
        return None, None, None, None

    # Priority Queue: stores (line_changes, total_weight, node, path_taken, route_colors)
    pq = [(0, 0, start, [], [])]  # (line_changes, total_weight, node, path, colors)
    visited = {}  # Keeps track of visited nodes with (line_changes, total_weight)

    while pq:
        line_changes, total_weight, current, path, colors = heapq.heappop(pq)

        # If we reached the destination, return the path with all stops and their colors
        if current == end:
            # Include the start and end with their respective colors
            combined_path_with_colors = [f"{start} ({colors[0]})"] + \
                                        [f"{stop} ({color})" for stop, color in zip(path, colors)] + \
                                        [f"{end} ({colors[-1]})"]
            return path, total_weight, line_changes, combined_path_with_colors

        # Skip if we have visited this node with fewer line changes and less weight
        if current in visited:
            prev_line_changes, prev_weight = visited[current]
            if (line_changes > prev_line_changes) or (line_changes == prev_line_changes and total_weight >= prev_weight):
                continue

        # Mark the current node as visited
        visited[current] = (line_changes, total_weight)

        # Explore neighbors
        for neighbor in G.neighbors(current):
            edge_data = G.get_edge_data(current, neighbor)
            edge_color = edge_data['color']
            edge_weight = edge_data['weight']

            # Check if we are changing lines
            new_line_changes = line_changes
            new_colors = colors[:]
            if not colors or edge_color != colors[-1]:
                new_line_changes += 1
                new_colors.append(edge_color)

            # Update the total weight for the path
            new_total_weight = total_weight + edge_weight

            # Add the neighbor to the priority queue
            heapq.heappush(pq, (new_line_changes, new_total_weight, neighbor, path + [neighbor], new_colors))

    return None, None, None, None



def user_interface(request):
    file_path = 'formatted_routes.xlsx'  # path to your Excel file
    data = load_excel_data(file_path)
    G = build_graph(data)

    stops = data['Stop'].unique()
    colors = data['Color'].unique()

    if request.method == 'POST':
        start_stop = request.POST.get('start_stop')
        end_stop = request.POST.get('end_stop')

        path, total_weight, color_changes, combined_path_with_colors = find_best_route(G, start_stop, end_stop)

        return render(request, 'bus_routes/result.html', {
            'path': path,
            'total_weight': total_weight,
            'color_changes': color_changes,
            'combined_path': combined_path_with_colors,  # Pass the path with colors here
            'stops': stops,
            'colors': colors,
        })

    return render(request, 'bus_routes/index.html', {
        'stops': stops,
        'colors': colors,
    })
