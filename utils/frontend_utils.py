from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import streamlit as st

def add_sidebar(st):
    # Use a default file if no custom file is uploaded

    st.markdown("### Visualization Options")

    # Graph options with better organization
    show_percentages = st.checkbox(
        "Show likelihood percentages on connections",
        value=True,
        help="Display the probability percentage on each causal relationship"
    )


    # Add info section at the bottom of sidebar
    st.markdown("---")
    st.markdown("""
          **💡 Tips:**
          - Click on any node to view details
          - Hover over connections to see causation likelihood
          - Use mouse wheel to zoom in/out
          """)

    return show_percentages

def load_data():
    assert (MONGODB_URI := st.secrets["MONGODB_URI"]), "No MongoDB URI provided in secrets.toml."

    client: MongoClient = MongoClient(MONGODB_URI)
    db: Database = client.get_database("events")
    collection: Collection = db.get_collection("events")
    return collection.find().to_list()

def filter_data(st):
    # Add date filter
    st.markdown("### Filters")

    # Load data for filtering options
    data = load_data()

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
        selected_countries = []
        selected_categories = []

    return filtered_data, selected_countries, selected_categories
