import pandas as pd
import streamlit as st
from utils.pages_utils import add_one_event
from utils.pages_styles import horizon_headers_style

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

        filtered_df = pd.DataFrame(filtered_data)

        return filtered_df
    else:
        return df

def filter_and_display_by_time_period(df: pd.DataFrame, period: str):
    filtered_df = df[df["due_date"] == period]

    filtered_df = filtered_df.sort_values("likelihood", ascending=False)

    if len(filtered_df) != 0:

        horizon_headers_style(period, len(filtered_df))

        if st.button("View All", key=period):
            # Store the data you want to pass in session state
            st.session_state.view_all_data = filtered_df
            st.session_state.period = period
            # Switch to the page that will display all data
            st.switch_page("pages/potential_events_horizon.py")

        # Display events in a grid
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        cols = [col1, col2, col3, col4]

        # TODO: Get uuids

        with st.container():
            st.markdown('<div class="cards-container">', unsafe_allow_html=True)

            for i, row in enumerate(filtered_df.head(4).itertuples()):
                with cols[i]:
                    add_one_event(row)

            st.markdown('</div>', unsafe_allow_html=True)

def layout_for_one_horizon_page(data: pd.DataFrame, period: str):
    # Page layout
    st.set_page_config(layout="wide", page_title=f"Policymakers AI, all events for {period} horizon",)

    data = filter_by_country_category(data)

    horizon_headers_style(period, len(data))

    with st.container():
        st.markdown('<div class="cards-container">', unsafe_allow_html=True)
        # Initialize column counter and cycle through column positions
        col_index = 0
        cols = []

        for i, row in enumerate(data.itertuples()):
            # Create new row every 4th item
            if i % 4 == 0:
                cols = st.columns(4, gap = "medium")  # Creates new row with 4 columns
                col_index = 0  # Reset column counter for new row

            # Use current column in the row
            with cols[col_index]:
                add_one_event(row)

            # Move to next column (0-3)
            col_index = (col_index + 1) % 4

        st.markdown('</div>', unsafe_allow_html=True)
