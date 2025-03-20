import networkx as nx
from base64 import b64decode
import re
from pyvis.network import Network
from utils.graph_utils import whitespaces_to_line_breaks, options_setting, create_graph_structure_and_legend, get_final_html

def create_graph(data, show_percentages=True):
    graph = nx.DiGraph()  # Directed graph to show the flow of causation

    # Add root node for "Now"
    research_country = data[0]["research_country"]  # TODO: find a better way to get the country
    graph.add_node(
        0,
        title="Now",
        size=20,
        label="Now",
        country=research_country,
        category="Now"
    )

    # Add nodes
    for node in data:
        node_id = str(node["_id"])  # Convert IDs to strings for compatibility
        label = node["potential_event"]
        label = whitespaces_to_line_breaks(label, each_num=5)
        title = f"{node['due_date']}: {node['potential_event']}"  # TODO: Add research details

        # Add node with attributes
        graph.add_node(
            node_id,
            title=title,
            size=20,
            label=label,
            country=node["research_country"],  # TODO: country vs research_country
            category=node["category"]
        )

        research = b64decode(node["research"].encode()).decode()
        likelihood = int((
            re
            .search(r"\*\*likelihood\*\*:\s(\d+)/10", research, re.IGNORECASE)
            .group(1)
        )) * 10

        if show_percentages:
            edge_label = f"{likelihood:.0f}%"
        else:
            edge_label = ""
        edge_length = likelihood  # TODO: reformulate to work on date
        graph.add_edge(
            0,
            node_id,
            title=edge_label,
            label=edge_label,
            length=edge_length,
            width=2
        )

    return graph

def draw_graph(graph, data):
    # Create Network object
    nt = Network("800px", "800px", notebook=False, directed=True)

    # Check if graph is empty
    if len(graph.nodes) == 0:
        return "Error: Graph has no nodes to display"

    # Add graph data to Network
    nt.from_nx(graph)

    nt.toggle_physics(True)

    # Create a color mapping based on categories
    categories = set()
    for node_id in graph.nodes():
        if 'category' in graph.nodes[node_id]:
            categories.add(graph.nodes[node_id]['category'])

    categories = list(categories)
    color_map = {}
    colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#FF6D01", "#46BDC6", "#7B1FA2", "#C2185B",
              "#1A73E8", "#D93025", "#F9AB00", "#1E8E3E", "#E37400", "#00ACC1", "#6A1B9A", "#B00020"]

    for i, category in enumerate(categories):
        color_map[category] = colors[i % len(colors)]

    # Update node colors based on category
    for node in nt.nodes:
        node_id = node['id']
        if 'category' in graph.nodes[node_id]:
            node['color'] = color_map[graph.nodes[node_id]['category']]

    options_setting(nt)

    try:
        legend_data, node_info = create_graph_structure_and_legend(data, color_map, categories)
        # Save graph to a file
        file_path = "graph.html"
        final_result = get_final_html(nt, graph, color_map, legend_data, node_info, file_path)
    except Exception as e:
        return f"Error creating or reading graph: {str(e)}"
    return final_result
