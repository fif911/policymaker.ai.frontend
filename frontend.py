import streamlit as st
import os
from datetime import datetime
from graph_functions import create_graph, draw_graph
from frontend_utils import add_sidebar, filter_data

# Set custom theme for Streamlit
def set_custom_theme():
    with open("web/theme.css", "r") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )

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
        show_percentages, json_file = add_sidebar(st)

    filtered_data, selected_countries, selected_categories = filter_data(st, json_file)

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
