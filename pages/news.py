import streamlit as st
import pandas as pd
import base64
from utils.frontend_utils import load_data

image_size = [200, 200]

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
                                            default=countries_available)
        with col2:
            category_filter = st.multiselect("Filter by Category", options=categories_available,
                                             default=categories_available)

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

    if len(filtered_df) != 0:

        st.markdown(f"### {period} horizon")
        st.markdown("---")
        # "View All" button aligned right
        st.markdown("<div style='text-align: right; margin-top: 0px'><button>View All</button></div>", unsafe_allow_html=True)

        # Display events in a grid
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]

        for i, row in enumerate(filtered_df.itertuples()):
            with cols[i]:
                # Outer container to align both square and text blocks vertically
                st.markdown(
                    f'<div style="display:flex; flex-direction:column; justify-content:flex-start; align-items:center; height:700px;">' # TODO: Calculate heights based on text length
                    f'<div style="width:{image_size[0]}px; height:{image_size[1]}px; padding:10px; display:flex; justify-content:center; align-items:center;">'
                    f'<img src="https://picsum.photos/{image_size[0]}/{image_size[1]}" alt="Random Image" style="max-width:{image_size[0]}px; max-height:{image_size[1]}px; margin-top: 30px">'
                    f'</div>'
                    f'<div style="text-align:center; margin-top:20px;">'
                    f'<b>Potential event:</b> {row.potential_event}<br>'
                    f'<b>Reasoning:</b> {row.reasoning}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

# Page layout
st.set_page_config(layout="wide")

loaded_data = load_data()

df = pd.DataFrame(loaded_data)

filtered_data = filter_by_country_category(df)

# TODO: Think of a rule to sort days, weeks, months, years in that order.

for period in df["due_date"].unique():
    filter_and_display_by_time_period(filtered_data, period)
