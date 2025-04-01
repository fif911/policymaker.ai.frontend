import streamlit as st
import textwrap
import toml
import pandas as pd
from random import choices
from utils.pages_styles import horizon_headers_style
from utils.frontend_utils import filter_data_by_country_category
from config import settings

IMAGE_SIZE = [200, 200]
TITLE_SYMBOLS = 100
REASONING_SYMBOLS = 120

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

def add_one_event(row, period):

    # TODO: Add support for checking the theme whenever streamlit update for it rolls out (track github issue)
    # will have to modify color of <h3 class="event-title">

    st.markdown(
        f'<a href="event_details?event_id={row._1}&period={period}" target="_self" style="color: inherit; text-decoration: none;">'
        f'  <div class="event-card">'
        f'      <div class="card-image">'
        f'          <img src="https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM=" '
        f'               alt="Event thumbnail">'
        f'      </div>'
        f'      <div class="card-content">'
        f'          <div>'
        f'              <h3 class="event-title">{textwrap.shorten(row.potential_event, width=TITLE_SYMBOLS, placeholder="...")}</h3>'
        f'              <p class="event-reasoning">{textwrap.shorten(row.reasoning, width=REASONING_SYMBOLS, placeholder="...")}</p>'
        f'          </div>'
        f'          <div class="event-meta">'
        f'              <span class="meta-chip likelihood-chip">Likelihood: {row.likelihood}</span>'
        f'              <span class="meta-chip category-chip">{row.category}</span>'
        f'              <span class="meta-chip country-chip">{row.research_country}</span>'
        f'          </div>'
        f'      </div>'
        f'  </div>'
        f'</a>',
        unsafe_allow_html=True
    )

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
