import streamlit as st
import networkx as nx
from pyvis.network import Network
import json  # Add this import statement

def create_graph():
    G = nx.DiGraph()  # Directed graph to show the flow of causation

    # Add nodes
    G.add_node("Bridge Collapse", title="Bridge Collapse", size=20, label="Bridge Collapse")
    G.add_node("Logistics Issues", title="Logistics Issues", size=20, label="Logistics Issues")
    G.add_node("Airport Closed", title="Airport Closed", size=20, label="Airport Closed")
    G.add_node("Military Aid Delayed", title="Military Aid Delayed", size=20, label="Military Aid Delayed")

    # Add edges with percentages as labels
    G.add_edge("Bridge Collapse", "Logistics Issues", title="70%", length=200, width=2)
    G.add_edge("Logistics Issues", "Airport Closed", title="10%", length=200, width=2)
    G.add_edge("Airport Closed", "Military Aid Delayed", title="", length=200, width=2)

    return G

def draw_graph(G):
    nt = Network("500px", "500px", notebook=False, directed=True)  # Set notebook to False for better compatibility outside Jupyter
    nt.from_nx(G)

    # Enable hierarchical layout for left-to-right arrangement
    options = {
        "layout": {
            "hierarchical": {
                "enabled": True,
                "direction": "LR",  # Left-to-right layout
                "sortMethod": "directed"
            }
        },
        "edges": {
            "arrows": {
                "to": {
                    "enabled": True,
                    "scaleFactor": 1
                }
            },
            "smooth": False,
            "font": {
                "size": 12,
                "align": "middle"
            }
        }
    }

    # Set the options
    nt.set_options(json.dumps(options))  # This line requires the `json` module

    try:
        nt.save_graph("graph.html")
        HtmlFile = open("graph.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        return source_code  # Return the HTML source directly
    except Exception as e:
        return f"Error creating or reading graph: {str(e)}"


def main():
    st.title("Event Causation Graph")
    G = create_graph()
    html_content = draw_graph(G)

    if "Error" not in html_content:
        st.components.v1.html(html_content, height=500)
    else:
        st.error(html_content)  # Display error if any

if __name__ == "__main__":
    main()

