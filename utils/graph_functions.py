import numpy as np
import networkx as nx
import datetime
from base64 import b64decode
import re
from pyvis.network import Network
from utils.graph_utils import options_setting, create_graph_structure_and_legend, get_final_html
from utils.frontend_utils import whitespaces_to_line_breaks


def create_graph(data, show_percentages=True):
    graph = nx.DiGraph()  # Directed graph to show the flow of causation

    # TODO: find a better way to get the country for node Now. Also will be a problem when there are many countries.
    # Add root node for "Now"
    research_country = data[0]["research_country"]
    graph.add_node(
        0,
        title="Now",
        size=20,
        label="Now",
        country=research_country,
        category="Now",
        research="Now",
        due_date="Now",
        research_date = "Now",
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
            category=node["category"],
            research=node["research"],
            due_date=node["due_date"],
            research_date=node["research_date"],
        )

        research = b64decode(node["research"].encode()).decode()
        likelihood = int((
            re
            .search(r"\*\*likelihood\*\*:\s\**(\d+)/10", research, re.IGNORECASE)
            .group(1)
        )) * 10

        if show_percentages:
            edge_label = f"{likelihood:.0f}%"
        else:
            edge_label = ""

        graph.add_edge(
            0,
            node_id,
            title=edge_label,
            label=edge_label,
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
    distance_between_nodes = 200
    dist = (len(graph.nodes) - 2) * distance_between_nodes / 2
    y_values: list = np.linspace(-dist, dist, len(graph.nodes)).tolist()

    i: int = 0

    for node in nt.nodes:
        node_id = node['id']
        node['color'] = color_map[graph.nodes[node_id]['category']]

        if node_id == 0:
            node['x'] = 0
            node['y'] = 0
            continue

        research = b64decode(graph.nodes[node_id]['research'].encode()).decode()
        research_date = graph.nodes[node_id]['research_date']
        try:
            due_date = (
                    re
                    .search(r"\*\*(Due Date|due_date)\*\*:\s(\d{4}-\d{2}-\d{2})", research, re.IGNORECASE)
                    .group(2)
                )
        except:
            print(research)
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d")
        research_date = datetime.datetime.strptime(research_date, "%Y-%m-%d")

        days = (due_date - research_date).days

        node['x'] = int(np.sqrt(days)) * 100
        # pick one from y_values and remove it
        node['y'] = y_values[i]
        i += 1
    options_setting(nt)

    try:
        legend_data, node_info = create_graph_structure_and_legend(data, color_map, categories)
        # Save graph to a file
        file_path = "graph.html"
        final_result = get_final_html(nt, graph, color_map, legend_data, node_info, file_path)
    except Exception as e:
        return f"Error creating or reading graph: {str(e)}"
    return final_result
