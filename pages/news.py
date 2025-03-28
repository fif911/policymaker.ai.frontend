import streamlit as st
import pandas as pd
import base64
from utils.frontend_utils import load_data

def decode_base64(encoded_text):
    try:
        return base64.b64decode(encoded_text).decode("utf-8")
    except Exception:
        return "[Error decoding]"

def filter_by_country_category(df: pd.DataFrame):
    countries_available = df["research_country"].unique()
    categories_available = df["category"].unique()

    # Topbar with filters
    with st.expander("Filters", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            country_filter = st.multiselect("Filter by Country", options=countries_available,
                                            default=countries_available[0])
        with col2:
            category_filter = st.multiselect("Filter by Category", options=categories_available,
                                             default=categories_available[0])

    # Add the filters to the data
    if country_filter and category_filter:
        filtered_data = [
            item for ind, item in df.iterrows()
            if item.get("research_country") in country_filter and item.get("category") in category_filter
        ]

        filtered_data = pd.DataFrame(filtered_data)

        return filtered_data
    else:
        return df


def filter_and_display_by_time_period(df: pd.DataFrame, period: str):
    filtered_df = df[df["due_date"] == period].head(4)

    st.markdown(f"### {period} horizon")
    st.markdown("---")
    # "View All" button aligned right
    st.markdown("<div style='text-align: right;'><button>View All</button></div>", unsafe_allow_html=True)

    # Display events in a grid
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]

    for i, row in enumerate(filtered_df.itertuples()):
        with cols[i]:
            st.markdown(f'<div style="width:200px; height:200px; border:1px solid #ddd; padding:10px; text-align:center;"></div>', unsafe_allow_html=True)
            st.markdown(f'<div><b text-align:center>Potential event: {row.potential_event}</b><br text-align:center>Reasoning: {row.reasoning}</div>', unsafe_allow_html=True)

# Page layout
st.set_page_config(layout="wide")

loaded_data = load_data()

df = pd.DataFrame(loaded_data)

filtered_data = filter_by_country_category(df)

filter_and_display_by_time_period(filtered_data, '1 month')

filter_and_display_by_time_period(filtered_data, '2 months')