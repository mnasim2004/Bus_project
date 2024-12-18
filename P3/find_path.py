import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def load_excel_data(file_path):
    """ Load Excel data containing stop details """
    data = pd.read_excel(file_path)
    return data

def calculate_distance(grid1, grid2):
    """ Calculate approximate distance between two grid points (A-K, 1-9 matrix). """
    def grid_to_coordinates(grid):
        letter, number = grid[0], int(grid[1:])
        x = ord(letter.upper()) - ord('A')  # Convert letter to numeric x-coordinate
        y = number - 1  # Numeric y-coordinate
        return (x, y)

    coord1 = grid_to_coordinates(grid1)
    coord2 = grid_to_coordinates(grid2)
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

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
    """ Find the best route with shortest time and minimized color changes. """
    if start not in G or end not in G:
        return None, None, None

    # Use Dijkstra to find the shortest path
    try:
        path = nx.shortest_path(G, source=start, target=end, weight='weight')
        total_weight = nx.shortest_path_length(G, source=start, target=end, weight='weight')

        # Extract color changes
        color_changes = 0
        last_color = None
        route_colors = []
        for i in range(len(path) - 1):
            edge_data = G.get_edge_data(path[i], path[i + 1])
            color = edge_data['color']
            if color != last_color:
                color_changes += 1
                route_colors.append(color)
            last_color = color

        return path, total_weight, color_changes, route_colors
    except nx.NetworkXNoPath:
        return None, None, None

def user_interface(G):
    """ User interface to input start and end stops and display the best route. """
    print("Welcome to the Bus Route Planner!\n")
    start = input("Enter the starting stop: ")
    end = input("Enter the destination stop: ")

    path, total_weight, color_changes, route_colors = find_best_route(G, start, end)
    if path:
        print("\nBest Route:", " -> ".join(path))
        print(f"Total Travel Time: {total_weight:.2f} minutes")
        print(f"Number of Line Changes: {max(color_changes - 1, 0)}")
        print("Route Colors Taken:", " -> ".join(route_colors))
    else:
        print("\nError: One or both stops are invalid, or no path exists between them. Please check the stop names.")

def main():
    file_path = "formatted_routes.xlsx"  # File with stop details
    try:
        data = load_excel_data(file_path)
        print("Data loaded successfully!")

        G = build_graph(data)
        print("Graph built successfully!")

        # Run the user interface
        user_interface(G)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
