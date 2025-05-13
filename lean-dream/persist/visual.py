import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import os # For checking if the database file exists

# --- Configuration ---
DATABASE_FILE = 'microchip_risks_analysis.sqlite' # Ensure this matches the DB file name

# --- Database Operations ---
def fetch_all_risks_from_db(db_file):
    """Fetches all risk factor pairs (cause, effect) from the SQLite database."""
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' not found.")
        print("Please ensure the database was created and populated by the previous script.")
        return []
        
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT cause, effect FROM risk_factors")
        risk_data = cursor.fetchall()
        if not risk_data:
            print(f"No data found in 'risk_factors' table in '{db_file}'.")
            print("Please ensure the database was populated correctly.")
        return risk_data
    except sqlite3.Error as e:
        print(f"SQLite error fetching data: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- NetworkX Graph Operations ---
def build_risk_graph(risk_data):
    """Builds a directed graph from the risk factor data."""
    G = nx.DiGraph()
    if not risk_data:
        print("Cannot build graph: No risk data provided.")
        return G
        
    for cause, effect in risk_data:
        G.add_edge(cause, effect)
    print(f"Built NetworkX graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

# --- Visualization ---
def visualize_graph(graph, title="Risk Factor Network", layout_type='spring', save_to_file=None):
    """
    Visualizes the given NetworkX graph using Matplotlib.

    Args:
        graph (nx.DiGraph): The graph to visualize.
        title (str): The title for the plot.
        layout_type (str): Type of layout ('spring', 'kamada_kawai', 'circular', 'spectral', 'shell').
        save_to_file (str, optional): If provided, saves the plot to this filename.
    """
    if not graph.nodes():
        print("Graph is empty, nothing to visualize.")
        return

    plt.figure(figsize=(20, 20)) # Adjust figure size as needed for clarity

    # Choose a layout algorithm
    if layout_type == 'spring':
        # k controls the distance between nodes, iterations for convergence
        pos = nx.spring_layout(graph, k=0.25, iterations=30, seed=42)
    elif layout_type == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(graph)
    elif layout_type == 'circular':
        pos = nx.circular_layout(graph)
    elif layout_type == 'spectral':
        pos = nx.spectral_layout(graph)
    elif layout_type == 'shell':
        # For shell layout, you might want to define shells based on node properties
        # For a generic shell layout:
        shells = []
        if graph.number_of_nodes() > 0:
            # Example: create shells based on node degree or other criteria
            # For now, a simple split if you have many nodes
            nlist = list(graph.nodes())
            if len(nlist) > 50: # Arbitrary split for demonstration
                shells.append(nlist[:len(nlist)//2])
                shells.append(nlist[len(nlist)//2:])
            else:
                shells.append(nlist)
        if not shells or not shells[0]: # Ensure shells are not empty
             pos = nx.spring_layout(graph, k=0.25, iterations=30, seed=42) # Fallback
        else:
            pos = nx.shell_layout(graph, nlist=shells)

    else:
        print(f"Unknown layout type '{layout_type}'. Defaulting to spring layout.")
        pos = nx.spring_layout(graph, k=0.25, iterations=30, seed=42)

    # Draw the graph
    # For large graphs, labels can overlap heavily. Adjust font_size or skip labels.
    nx.draw(graph, pos, 
            with_labels=True, 
            node_size=100,       # Smaller nodes for large graphs
            node_color="skyblue", 
            font_size=7,         # Smaller font for labels
            font_weight="bold",
            width=0.5,           # Thinner edges
            arrowsize=8,         # Smaller arrows
            alpha=0.8,
            edge_color="gray")
    
    plt.title(title, fontsize=15)
    
    if save_to_file:
        try:
            plt.savefig(save_to_file, dpi=300, bbox_inches='tight')
            print(f"Graph saved to {save_to_file}")
        except Exception as e:
            print(f"Error saving graph to file: {e}")
    
    try:
        plt.show() # Display the plot
    except Exception as e:
        print(f"Could not display plot (matplotlib backend issue or no GUI available): {e}")
        print("If running in a non-GUI environment, ensure save_to_file is used.")

def visualize_subgraph_around_node(full_graph, node_name, radius=1, title_prefix="Subgraph around", save_to_file=None):
    """Visualizes a subgraph centered around a specific node."""
    if not full_graph.has_node(node_name):
        print(f"Node '{node_name}' not found in the graph.")
        return

    # Create an ego graph (node + neighbors within radius)
    subgraph = nx.ego_graph(full_graph, node_name, radius=radius)
    
    if subgraph.number_of_nodes() == 1 and subgraph.number_of_edges() == 0 and radius > 0:
        print(f"Node '{node_name}' has no neighbors within radius {radius} to form a meaningful subgraph.")
        # Optionally, still draw the single node
        # visualize_graph(subgraph, title=f"{title_prefix} '{node_name}' (isolated within radius)", save_to_file=save_to_file)
        return

    visualize_graph(subgraph, title=f"{title_prefix} '{node_name}' (radius {radius})", save_to_file=save_to_file)


# --- Main Execution ---
if __name__ == "__main__":
    # Step 1: Fetch risk data from the SQLite database
    print(f"Fetching risk data from '{DATABASE_FILE}'...")
    risk_data = fetch_all_risks_from_db(DATABASE_FILE)

    if risk_data:
        # Step 2: Build the NetworkX graph
        risk_graph = build_risk_graph(risk_data)

        # Step 3: Visualize the entire graph
        # For very large graphs, this can be slow and cluttered.
        # Consider commenting this out and using subgraph visualizations instead.
        print("\nVisualizing the full risk network (this might be dense)...")
        visualize_graph(risk_graph, title="Full Microchip Risk Factor Network", layout_type='spring', save_to_file="microchip_full_risk_network.png")

        # --- Examples of Subgraph Visualizations (often more useful) ---
        
        # Example 1: Visualize the neighborhood of a specific risk factor
        node_to_explore = 'manufacturing_complexity' 
        print(f"\nVisualizing subgraph around '{node_to_explore}'...")
        visualize_subgraph_around_node(risk_graph, node_to_explore, radius=1, title_prefix="Microchip - Neighborhood of", save_to_file=f"microchip_subgraph_{node_to_explore}.png")

        # Example 2: Visualize the neighborhood of another critical-looking node
        node_to_explore_2 = 'negative_stock_price_effect'
        print(f"\nVisualizing subgraph around '{node_to_explore_2}'...")
        visualize_subgraph_around_node(risk_graph, node_to_explore_2, radius=1, title_prefix="Microchip - Neighborhood of", save_to_file=f"microchip_subgraph_{node_to_explore_2}.png")
        
        # Example 3: Explore a node with potentially many outgoing connections (a root cause or major driver)
        # You might identify such nodes from previous analysis (e.g., find_root_causes or high out-degree nodes)
        # For instance, if 'intense_competition' was identified as a key driver:
        # node_to_explore_3 = 'intense_competition'
        # print(f"\nVisualizing subgraph around '{node_to_explore_3}'...")
        # visualize_subgraph_around_node(risk_graph, node_to_explore_3, radius=1, title_prefix="Microchip - Neighborhood of", save_to_file=f"microchip_subgraph_{node_to_explore_3}.png")

        print("\n--- Visualization script finished ---")
        print("Check for .png files in the script's directory if saving was enabled.")
    else:
        print("No risk data loaded, so no graph to visualize.")

