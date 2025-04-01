import streamlit as st
import toml
import pandas as pd
from random import choices
from utils.pages_styles import horizon_headers_style
from utils.frontend_utils import filter_data_by_country_category, add_one_event
from config import settings

IMAGE_SIZE = [200, 200]

def add_sidebar_and_layout(file_called_from: str):
    # Load pages.toml file
    pages_config = toml.load(f"{settings.root_directory}/.streamlit/pages.toml")
    pages = pages_config.get("pages", [])

    current_page = next(item for item in pages if file_called_from in item["path"])

    # Page layout and styles
    st.set_page_config(
        layout="wide",
        page_title=current_page["name"],
        page_icon=current_page["icon"],
        initial_sidebar_state="collapsed"
    )

    with st.sidebar:
        for page in pages:
            st.page_link(page=page["path"], label=page["name"], icon=page["icon"])

def layout_for_one_horizon_page(data: pd.DataFrame, period: str):

    filtered_df_by_country_category, _, _ = filter_data_by_country_category(data)

    data = pd.DataFrame(filtered_df_by_country_category)

    data["likelihood"] = choices(range(1, 10), k=len(data))

    data.sort_values("likelihood", ascending=False, inplace=True)

    horizon_headers_style(period, len(data), show_view_all=False)

    # Get the number of columns based on window width
    num_columns = 4

    with st.container():
        st.markdown('<div class="cards-container">', unsafe_allow_html=True)
        # Initialize column counter and cycle through column positions
        col_index = 0
        cols = []

        for i, row in enumerate(data.itertuples()):
            # Create new row when needed
            if i % num_columns == 0:
                cols = st.columns(num_columns, gap="medium")
                col_index = 0

            # Use current column in the row
            with cols[col_index]:
                add_one_event(row, period)

            # Move to next column
            col_index = (col_index + 1) % num_columns

            # Add gap between rows
            if col_index == 0 and i != len(data) - 1:
                st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
