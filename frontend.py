import streamlit as st
import networkx as nx
from pyvis.network import Network
import json
import os
import html
from datetime import datetime

# Set custom theme for Streamlit
def set_custom_theme():
    st.markdown("""
    <style>
    /* Main page styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #1E3A8A;
        padding-bottom: 1rem;
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 2rem;
    }
    
    /* Card-like containers for content */
    .stAlert {
        border-radius: 8px;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F8FAFC;
    }
    
    .sidebar .sidebar-content {
        background-color: #F8FAFC;
    }
    
    /* Sidebar header styling */
    .sidebar .block-container {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebarNav"] {
        background-color: #F8FAFC;
        padding-top: 1rem;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Info box styling */
    .stInfo {
        background-color: #EFF6FF;
        padding: 1rem;
        border-left: 4px solid #3B82F6;
        margin-bottom: 1rem;
    }
    
    /* Error box styling */
    .stError {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
    }
    
    /* Warning box styling */
    .stWarning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background-color: #F9FAFB;
        padding: 1rem;
        border-radius: 8px;
        border: 1px dashed #D1D5DB;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        font-weight: 500;
    }
    
    /* Dividers */
    hr {
        margin: 1.5rem 0;
        border-color: #E5E7EB;
    }
    
    /* Graph container styling */
    [data-testid="stHtmlFrame"] {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

def load_data(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        st.error(f"Error loading JSON data: {str(e)}")
        return []

def create_graph(data, show_percentages=True):
    G = nx.DiGraph()  # Directed graph to show the flow of causation
    
    # Add nodes
    for node in data:
        node_id = str(node["node_id"])  # Convert IDs to strings for compatibility
        label = node["insight"]
        title = f"{node['date']}: {node['insight']}\n{node['event_description']}"
        
        # Add node with attributes
        G.add_node(
            node_id, 
            title=title, 
            size=20, 
            label=label,
            country=node["country"],
            category=node["category"]
        )
    
    # Add edges based on causation relationships
   # Add edges based on causation relationships
    for node in data:
        node_id = str(node["node_id"])  # Convert to string
        
        # Add edges for events that caused this node
        if "caused_by" in node:
            for causer_node_id in node["caused_by"]:
                causer_node_id = str(causer_node_id)  # Convert to string
                
                # Find the likelihood value for this connection
                likelihood = node.get("likelihood", 0.75) * 100  # Default 75% if not specified
                
                if show_percentages:
                    edge_label = f"{likelihood:.0f}%"
                else:
                    edge_label = ""
                
                if causer_node_id in G:  # Make sure the node exists
                    G.add_edge(causer_node_id, node_id, title=edge_label, 
                           label=edge_label, length=200, width=2)
    
    return G

def draw_graph(G, data):
    # Create Network object
    nt = Network("800px", "800px", notebook=False, directed=True)
    
    # Check if graph is empty
    if len(G.nodes) == 0:
        return "Error: Graph has no nodes to display"
    
    # Add graph data to Network
    nt.from_nx(G)
    
    # Create a color mapping based on categories
    categories = set()
    for node_id in G.nodes():
        if 'category' in G.nodes[node_id]:
            categories.add(G.nodes[node_id]['category'])
    
    categories = list(categories)
    color_map = {}
    colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#FF6D01", "#46BDC6", "#7B1FA2", "#C2185B", 
              "#1A73E8", "#D93025", "#F9AB00", "#1E8E3E", "#E37400", "#00ACC1", "#6A1B9A", "#B00020"]
    
    for i, category in enumerate(categories):
        color_map[category] = colors[i % len(colors)]
    
    # Update node colors based on category
    for node in nt.nodes:
        node_id = node['id']
        if 'category' in G.nodes[node_id]:
            node['color'] = color_map[G.nodes[node_id]['category']]
    
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
                    "scaleFactor": 1
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
                "nodeDistance": 200
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
            node_id = str(item["node_id"])
            node_info[node_id] = {
                "insight": item["insight"],
                "date": item["date"],
                "description": item["event_description"],
                "country": item["country"],
                "category": item["category"]
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
                    
                    # CSS for the modal and legend - improved styling
                    modal_css = """
                    <style>
                    /* Import Google Font */
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
                    
                    /* General styling */
                    body {
                        font-family: 'Inter', sans-serif;
                    }
                    
                    /* Modal styling */
                    #node-modal {
                        display: none;
                        position: fixed;
                        z-index: 1000;
                        left: 0;
                        top: 0;
                        width: 100%;
                        height: 100%;
                        background-color: rgba(0, 0, 0, 0.5);
                        backdrop-filter: blur(3px);
                        transition: opacity 0.3s ease;
                    }
                    
                    .modal-content {
                        background-color: #ffffff;
                        margin: 10% auto;
                        padding: 30px;
                        border: none;
                        width: 70%;
                        max-width: 700px;
                        border-radius: 12px;
                        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                        animation: modalFadeIn 0.3s ease-out;
                    }
                    
                    @keyframes modalFadeIn {
                        from {opacity: 0; transform: translateY(-20px);}
                        to {opacity: 1; transform: translateY(0);}
                    }
                    
                    .close-btn {
                        color: #666;
                        float: right;
                        font-size: 24px;
                        font-weight: bold;
                        cursor: pointer;
                        transition: color 0.2s;
                        margin-top: -10px;
                    }
                    
                    .close-btn:hover {
                        color: #000;
                    }
                    
                    .modal-header {
                        border-bottom: 2px solid #f0f0f0;
                        padding-bottom: 15px;
                        margin-bottom: 20px;
                    }
                    
                    .modal-header h2 {
                        color: #1a56db;
                        font-weight: 600;
                        margin: 0;
                        font-size: 1.5rem;
                        line-height: 1.3;
                    }
                    
                    .modal-body p {
                        margin: 12px 0;
                        line-height: 1.5;
                        color: #333;
                    }
                    
                    .modal-label {
                        font-weight: 600;
                        color: #4b5563;
                        display: inline-block;
                        min-width: 100px;
                    }
                    
                    #modal-description {
                        background-color: #f9fafb;
                        padding: 15px;
                        border-radius: 8px;
                        margin-top: 5px;
                        line-height: 1.6;
                    }
                    
                    /* Category and country badges */
                    #modal-category, #modal-country {
                        display: inline-block;
                        background-color: #e5e7eb;
                        padding: 4px 10px;
                        border-radius: 20px;
                        font-size: 0.9rem;
                        font-weight: 500;
                    }
                    
                    /* Legend styling */
                    #category-legend {
                        position: absolute;
                        top: 15px;
                        right: 15px;
                        background-color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 15px;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                        z-index: 100;
                        max-width: 250px;
                        transition: opacity 0.3s;
                    }
                    
                    #category-legend:hover {
                        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
                    }
                    
                    .legend-title {
                        font-weight: 600;
                        margin-bottom: 12px;
                        text-align: center;
                        color: #374151;
                        font-size: 1rem;
                        border-bottom: 1px solid #e5e7eb;
                        padding-bottom: 8px;
                    }
                    
                    .legend-item {
                        display: flex;
                        align-items: center;
                        margin-bottom: 8px;
                        padding: 3px 0;
                    }
                    
                    .color-box {
                        width: 16px;
                        height: 16px;
                        margin-right: 10px;
                        border-radius: 4px;
                        border: 1px solid rgba(0, 0, 0, 0.1);
                    }
                    
                    /* Mobile responsiveness */
                    @media (max-width: 768px) {
                        .modal-content {
                            width: 90%;
                            margin: 20% auto;
                            padding: 20px;
                        }
                        
                        #category-legend {
                            max-width: 200px;
                            font-size: 0.9rem;
                        }
                    }
                    </style>
                    """
                    
                    # HTML for the modal - improved layout
                    modal_html = """
                    <div id="node-modal">
                        <div class="modal-content">
                            <span class="close-btn">&times;</span>
                            <div class="modal-header">
                                <h2 id="modal-title"></h2>
                            </div>
                            <div class="modal-body">
                                <p><span class="modal-label">Date:</span> <span id="modal-date"></span></p>
                                <p><span class="modal-label">Country:</span> <span id="modal-country"></span></p>
                                <p><span class="modal-label">Category:</span> <span id="modal-category"></span></p>
                                <p><span class="modal-label">Description:</span></p>
                                <p id="modal-description"></p>
                            </div>
                        </div>
                    </div>
                    
                    <div id="category-legend">
                        <div class="legend-title">Event Categories</div>
                        <div id="legend-items"></div>
                    </div>
                    """
                    
                    # JavaScript for the modal and legend - improved UX
                    modal_js = f"""
                    <script>
                    // Wait for network to be fully initialized
                    document.addEventListener('DOMContentLoaded', function() {{
                        // Make sure we have access to the network object
                        setTimeout(function() {{
                            try {{
                                // Node data
                                const nodeData = {node_data_json};
                                
                                // Legend data
                                const legendData = {legend_json};
                                
                                // Modal elements
                                const modal = document.getElementById('node-modal');
                                const modalTitle = document.getElementById('modal-title');
                                const modalDate = document.getElementById('modal-date');
                                const modalCountry = document.getElementById('modal-country');
                                const modalCategory = document.getElementById('modal-category');
                                const modalDescription = document.getElementById('modal-description');
                                const closeBtn = document.getElementsByClassName('close-btn')[0];
                                
                                // Close the modal when clicking the X
                                closeBtn.onclick = function() {{
                                    modal.style.display = 'none';
                                }};
                                
                                // Close the modal when clicking outside of it
                                window.onclick = function(event) {{
                                    if (event.target == modal) {{
                                        modal.style.display = 'none';
                                    }}
                                }};
                                
                                // Close modal with Escape key
                                document.addEventListener('keydown', function(event) {{
                                    if (event.key === 'Escape' && modal.style.display === 'block') {{
                                        modal.style.display = 'none';
                                    }}
                                }});
                                
                                // Create legend items
                                const legendContainer = document.getElementById('legend-items');
                                for (const category in legendData) {{
                                    const color = legendData[category];
                                    const item = document.createElement('div');
                                    item.className = 'legend-item';
                                    
                                    const colorBox = document.createElement('div');
                                    colorBox.className = 'color-box';
                                    colorBox.style.backgroundColor = color;
                                    
                                    const text = document.createElement('span');
                                    text.textContent = category;
                                    
                                    item.appendChild(colorBox);
                                    item.appendChild(text);
                                    legendContainer.appendChild(item);
                                    
                                    // Make legend items interactive - highlight related nodes
                                    item.style.cursor = 'pointer';
                                    item.addEventListener('mouseenter', function() {{
                                        if (typeof network !== 'undefined') {{
                                            const nodeIds = [];
                                            Object.keys(nodeData).forEach(nodeId => {{
                                                if (nodeData[nodeId].category === category) {{
                                                    nodeIds.push(nodeId);
                                                }}
                                            }});
                                            
                                            network.selectNodes(nodeIds);
                                        }}
                                    }});
                                    
                                    item.addEventListener('mouseleave', function() {{
                                        if (typeof network !== 'undefined') {{
                                            network.unselectAll();
                                        }}
                                    }});
                                }}
                                
                                // Add click event to the network
                                if (typeof network !== 'undefined') {{
                                    network.on('click', function(params) {{
                                        if (params.nodes.length) {{
                                            const nodeId = params.nodes[0];
                                            const data = nodeData[nodeId];
                                            
                                            if (data) {{
                                                modalTitle.textContent = data.insight;
                                                modalDate.textContent = data.date;
                                                modalCountry.textContent = data.country;
                                                
                                                // Set color for category based on legend
                                                modalCategory.textContent = data.category;
                                                const categoryColor = legendData[data.category];
                                                if (categoryColor) {{
                                                    modalCategory.style.backgroundColor = categoryColor;
                                                    modalCategory.style.color = getContrastColor(categoryColor);
                                                }}
                                                
                                                modalDescription.textContent = data.description;
                                                modal.style.display = 'block';
                                            }}
                                        }}
                                    }});
                                    
                                    // Make nodes bigger on hover for better UX
                                    network.on('hoverNode', function(params) {{
                                        network.canvas.body.container.style.cursor = 'pointer';
                                    }});
                                    
                                    network.on('blurNode', function(params) {{
                                        network.canvas.body.container.style.cursor = 'default';
                                    }});
                                    
                                    console.log('Event handlers attached successfully');
                                }} else {{
                                    console.error('Network object not available');
                                }}
                                
                                // Helper function to determine text color based on background
                                function getContrastColor(hexColor) {{
                                    // Convert hex to RGB
                                    let r = parseInt(hexColor.substr(1, 2), 16);
                                    let g = parseInt(hexColor.substr(3, 2), 16);
                                    let b = parseInt(hexColor.substr(5, 2), 16);
                                    
                                    // Calculate luminance
                                    let luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                                    
                                    // Return black or white depending on background brightness
                                    return luminance > 0.5 ? '#000000' : '#ffffff';
                                }}
                                
                            }} catch (error) {{
                                console.error('Error initializing interactive elements:', error);
                            }}
                        }}, 1000); // Wait 1 second for network to initialize
                    }});
                    </script>
                    """
                    
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
        page_title="Policymakers AI", 
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom theme
    set_custom_theme()
    
    # Create a header with better formatting
    st.markdown("""
    # 🔄 Policymakers AI
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
            help="File should contain events with node_id, insight, date, country, and category fields"
        )
        
        # Use a default file if no custom file is uploaded
        # json_file = "message.json"  # Default file path
        json_file = "final.json"  # Default file path
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
            countries = sorted(list(set(item["country"] for item in data if "country" in item)))
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
                    if item.get("country") in selected_countries and item.get("category") in selected_categories
                ]
            else:
                filtered_data = data
        else:
            filtered_data = []
        
        # Advanced options collapsed section
        with st.expander("🔧 Advanced Options"):
            debug_mode = st.checkbox("Debug Mode", value=False)
            st.slider("Node Size", 10, 50, 20, help="Adjust the size of event nodes in the graph")
            st.slider("Edge Width", 1, 5, 2, help="Adjust the width of connection lines in the graph")
        
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
            G = create_graph(filtered_data, show_percentages)
            
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
        
        # If in debug mode, show more details
        if debug_mode:
            st.subheader("Debug Information")
            debug_col1, debug_col2 = st.columns(2)
            with debug_col1:
                st.info(f"Graph Nodes: {len(G.nodes)}")
            with debug_col2:
                st.info(f"Graph Edges: {len(G.edges)}")
            
            # Show sample of the data
            with st.expander("Sample Data (First 2 Records)"):
                st.write(filtered_data[:2])
        
        # Draw graph
        html_content = draw_graph(G, filtered_data)
        
        if isinstance(html_content, str) and html_content.startswith("Error"):
            st.error(html_content)
        else:
            # Show raw HTML in debug mode
            if debug_mode and st.button("Show Raw HTML"):
                with st.expander("Raw HTML Preview"):
                    st.code(html_content[:1000] + "...", language="html")
            
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