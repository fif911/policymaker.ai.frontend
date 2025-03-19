import json
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv
import os

def add_sidebar(st):
    st.markdown("### 📊 Data Source")

    # File uploader with better instructions
    custom_file = st.file_uploader(
        "Upload a JSON file with event data",
        type=["json"],
        help="File should contain events with node_id, insight, date, country, and category fields"
        # TODO: Update fields
    )

    # Use a default file if no custom file is uploaded
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


    # Add info section at the bottom of sidebar
    st.markdown("---")
    st.markdown("""
          **💡 Tips:**
          - Click on any node to view details
          - Hover over connections to see causation likelihood
          - Use mouse wheel to zoom in/out
          """)

    return show_percentages, json_file

def load_data(json_file):
    load_dotenv()
    assert (MONGODB_URI := os.getenv("MONGODB_URI"))
    RESEARCH_DIRECTORY: str = f"./researches/"
    os.makedirs(RESEARCH_DIRECTORY, exist_ok=True)

    if json_file:
        with open(json_file, 'r') as file:
            data = json.load(file)

        return data
    else:
        client: MongoClient = MongoClient(MONGODB_URI)
        db: Database = client.get_database("events")
        collection: Collection = db.get_collection("events")

        return collection.find().to_list()

def filter_data(st, json_file):
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

    return filtered_data, selected_countries, selected_categories
