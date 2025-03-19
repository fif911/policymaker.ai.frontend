import re
import streamlit as st
import networkx as nx
from pyvis.network import Network
import json
import os
from datetime import datetime
from web.modal_js import modal_js_template
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv


# ======== Environment Variables =========
load_dotenv()
assert (MONGODB_URI := os.getenv("MONGODB_URI"))
RESEARCH_DIRECTORY: str = f"./researches/"
os.makedirs(RESEARCH_DIRECTORY, exist_ok=True)


# Set custom theme for Streamlit
def set_custom_theme():
    with open("web/theme.css", "r") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )

def load_data(json_file):
    if json_file:
        with open(json_file, 'r') as file:
            data = json.load(file)

        return data
    else:
        client: MongoClient = MongoClient(MONGODB_URI)
        db: Database = client.get_database("events")
        collection: Collection = db.get_collection("events")

        return collection.find().to_list()
    

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

        with open(node["research_path"], "r") as file:
            content = file.read()
            likelihood = int((
                re
                .search(r"\*\*likelihood\*\*:\s(\d+)/10", content)
                .group(1)
            )) * 10

        
        if show_percentages:
            edge_label = f"{likelihood:.0f}%"
        else:
            edge_label = ""
        edge_length = 200  # TODO: reformulate to work on date
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
    
    # Set options
    options = {
        "layout": {
            "hierarchical": {
                "enabled": True,
                "direction": "LR",
                "sortMethod": "directed",
                "levelSeparation": 200
            }
        },
        "edges": {
            "arrows": {
                "to": {
                    "enabled": True,
                    "scaleFactor": 1 # this changes arrow sizes
                }
            },
            "smooth": True,
            "font": {
                "size": 14,
                "color": "#343434",
                "face": "Inter, sans-serif",  # Changed to modern font
                "background": "rgba(255, 255, 255, 0.8)",  # Slightly more opaque
                "strokeWidth": 0,
                "align": "middle"
            }
        },
        "physics": {
            "enabled": True,
            "hierarchicalRepulsion": {
                "centralGravity": 0.0,
                "springLength": 200,
                "springConstant": 0.01,
                "nodeDistance": 150
            },
            "minVelocity": 0.75,
            "solver": "hierarchicalRepulsion"
        },
        "nodes": {
            "font": {
                "size": 16,
                "face": "Inter, sans-serif",  # Changed to modern font
                "color": "#333333"
            },
            "shape": "box",
            "margin": 12,  # Slightly larger margin
            "borderWidth": 1,
            "borderWidthSelected": 2,
            "shadow": True  # Added shadow for better visibility
        }
    }
    
    # Set the options
    nt.set_options(json.dumps(options))
    
    try:
        # Create a simplified data structure for the nodes
        node_info = {}
        for item in data:
            node_id = str(item["_id"])
            node_info[node_id] = {
                "research_country": item["research_country"],
                "date": item["date"],
                "potential_event": item["potential_event"],
                "due_date": item["due_date"],
                "country": item["country"],
                "actor": item["actor"],
                "category": item["category"],
                "source": item["source"],
                "reasoning": item["reasoning"],
            }
        
        # Also prepare a legend for categories
        legend_data = {category: color_map[category] for category in categories}
        
        # Save graph to a file
        file_path = "graph.html"
        nt.save_graph(file_path)
        
        # Check if file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
                
                # Find where to insert our custom code
                head_end_index = source_code.find('</head>')
                body_end_index = source_code.find('</body>')
                
                if head_end_index != -1 and body_end_index != -1:
                    # JSON.stringify the node data, and escape it properly
                    node_data_json = json.dumps(node_info)
                    node_data_json = node_data_json.replace('\\', '\\\\').replace("'", "\\'")
                    
                    # JSON for the legend
                    legend_json = json.dumps(legend_data)
                    legend_json = legend_json.replace('\\', '\\\\').replace("'", "\\'")
                    
                    # The modal and legend - improved styling, layout, UX
                    with open("web/modal.css", "r") as file:
                        modal_css: str = f"<style>{file.read()}</style>"
                    with open("web/modal.html", "r") as file:
                        modal_html: str = file.read()
                    modal_js: str = modal_js_template.format(node_data_json=node_data_json, legend_json=legend_json)
                    
                    # Insert CSS in head
                    head_part = source_code[:head_end_index] + modal_css + source_code[head_end_index:body_end_index]
                    
                    # Insert HTML and JS before body end
                    final_html = head_part + modal_html + modal_js + source_code[body_end_index:]
                    
                    return final_html
                else:
                    return "Error: Could not locate insertion points in the HTML"
        else:
            return "Error: Graph file is empty or doesn't exist"
    except Exception as e:
        return f"Error creating or reading graph: {str(e)}"

def main():
    # Set page config with custom icon and layout
    st.set_page_config(
        page_title="Policy maker AI", 
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom theme
    set_custom_theme()
    
    # Create a header with better formatting
    st.markdown("""
    # 🔄 Policy Maker AI
    """)
    
    # Add an introductory text
    st.markdown("""
    AI monitoring tool for real time geopolitical analysis.
    """)
    
    # Create columns for stats and filters later
    col1, col2 = st.columns([3, 1])
    
    # Sidebar with improved organization
    with st.sidebar:
        st.image("https://via.placeholder.com/150x60?text=EventGraph", width=150)
        
        st.markdown("### Data Source")
        
        # File uploader with better instructions
        custom_file = st.file_uploader(
            "Upload a JSON file with event data",
            type=["json"], 
            help="File should contain events with node_id, insight, date, country, and category fields"  # TODO: Update fields
        )
        
        # Use a default file if no custom file is uploaded
        # json_file = "message.json"  # Default file path
        json_file: None | str = None  # Default file path
        if custom_file is not None:
            # Save uploaded file temporarily
            with open("temp_upload.json", "wb") as f:
                f.write(custom_file.getbuffer())
            json_file = "temp_upload.json"
            st.success("✅ Custom data loaded successfully!")
        
        st.markdown("---")
        st.markdown("### Visualization Options")
        
        # Graph options with better organization
        show_percentages = st.checkbox(
            "Show likelihood percentages on connections", 
            value=True,
            help="Display the probability percentage on each causal relationship"
        )
        
        # Add date filter
        st.markdown("### Filters")
        
        # Load data for filtering options
        data = load_data(json_file)
        
        if data:
            # Extract unique countries and categories for filtering
            countries = sorted(list(set(item["research_country"] for item in data if "research_country" in item)))
            categories = sorted(list(set(item["category"] for item in data if "category" in item)))
            
            # Country filter multiselect
            selected_countries = st.multiselect(
                "Filter by Country",
                options=countries,
                default=countries,
                help="Select one or more countries to display"
            )
            
            # Category filter multiselect
            selected_categories = st.multiselect(
                "Filter by Category",
                options=categories,
                default=categories,
                help="Select one or more event categories to display"
            )
            
            # Add the filters to the data
            if selected_countries and selected_categories:
                filtered_data = [
                    item for item in data 
                    if item.get("research_country") in selected_countries and item.get("category") in selected_categories
                ]
            else:
                filtered_data = data
        else:
            filtered_data = []
        
        # Add info section at the bottom of sidebar
        st.markdown("---")
        st.markdown("""
        **💡 Tips:**
        - Click on any node to view details
        - Hover over connections to see causation likelihood
        - Use mouse wheel to zoom in/out
        """)
    
    # Main area
    if filtered_data:
        # Show dataset statistics in the new columns
        with col1:
            # Create graph from filtered data
            graph = create_graph(filtered_data, show_percentages)
            
            # Stats in a more attractive format
            st.markdown("### Dataset Overview")
            
            # Create three metrics in a row
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Total Events", len(filtered_data))
            with metric_col2:
                st.metric("Countries", len(selected_countries))
            with metric_col3:
                st.metric("Categories", len(selected_categories))
        
        # Draw graph
        html_content = draw_graph(graph, filtered_data)
        
        if isinstance(html_content, str) and html_content.startswith("Error"):
            st.error(html_content)
        else:
            # Display instructions for graph
            st.markdown("### Interactive Causation Graph")
            st.info("👆 Click on any node to view detailed information. Hover over lines to see causation likelihood.")
            
            # Display the graph with better styling
            st.components.v1.html(html_content, height=800, scrolling=True)
            
            # Add timestamp for last update
            st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    else:
        # Show warning if no data
        st.warning("⚠️ No data available. Please check your JSON file or adjust your filters.")
        
        # Add placeholder image when no data
        st.image("https://via.placeholder.com/800x400?text=No+Data+Available", use_column_width=True)

if __name__ == "__main__":
    main()
