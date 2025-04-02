from string import whitespace
import streamlit as st
import pandas as pd
import base64
from utils.mongo import get_mongo_connection

TITLE_SYMBOLS = 100
REASONING_SYMBOLS = 120

@st.cache_data
def load_data():
    """Load data from MongoDB"""
    data = get_mongo_connection().find().to_list()
    return data


def filter_data_by_country_category(data: pd.DataFrame | None = None):
    # Add date filter
    st.markdown("### Filters")

    if data is None:
        # Load data for filtering options
        data = load_data()

        # Extract unique countries and categories for filtering
        countries = sorted(list(set(item["research_country"] for item in data if "research_country" in item)))
        categories = sorted(list(set(item["category"] for item in data if "category" in item)))
    else:
        countries = data["research_country"].unique()
        categories = data["category"].unique()

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

    # Add the filters to the data and check whether it is a list or a dataframe
    if selected_countries and selected_categories and isinstance(data, pd.DataFrame):
        filtered_data = [
            item for ind, item in data.iterrows()
            if item.get("research_country") in selected_countries and item.get("category") in selected_categories
        ]
    elif selected_countries and selected_categories and isinstance(data, list):
        filtered_data = [
            item for item in data
            if item.get("research_country") in selected_countries and item.get("category") in selected_categories
        ]
    else:
        filtered_data = data

    return filtered_data, selected_countries, selected_categories


def insert_css(file_name: str):
    # Function to load and inject CSS
    with open(file_name, "r") as f:
        css = f'<style>{f.read()}</style>'
    return css

def decode_base64(encoded_text):
    try:
        return base64.b64decode(encoded_text).decode("utf-8")
    except Exception:
        return "[Error decoding]"

def convert_due_dates_into_dates(due_dates):
    dates_coded = {"day": 1, "days": 1, "week": 1, "weeks": 7, "month": 30, "months": 30, "year": 365, "years": 365}

    dates_scores = []
    for date in due_dates:
        date = date.split(" ")
        date_in_days = int(date[0]) * dates_coded[date[1]]
        dates_scores.append(date_in_days)
    return dates_scores


def whitespaces_to_line_breaks(string: str, each_num: int = 5) -> str:
    indexes = [i for i, char in enumerate(string) if char in whitespace]

    indexes = indexes[each_num-1::each_num]

    for index in indexes:
        string = string[:index] + "\n" + string[index + 1:]

    return string
