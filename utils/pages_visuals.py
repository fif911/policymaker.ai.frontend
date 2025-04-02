import textwrap
import markdown
import streamlit as st
import toml
import pandas as pd
from utils.frontend_utils import filter_data_by_country_category, insert_css, TITLE_SYMBOLS, REASONING_SYMBOLS
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
            if 'event_details' not in page["path"] and 'potential_events_horizon' not in page["path"]:
                st.page_link(page=page["path"], label=page["name"], icon=page["icon"])

def layout_for_one_horizon_page(data: pd.DataFrame, period: str):
    # TODO: Add support for checking the theme whenever streamlit update for it rolls out (track github issue)
    # will have to modify color of <h3 class="event-title">
    #
    # css = insert_css('web/blocks.css')
    # st.markdown(css, unsafe_allow_html=True)

    filtered_df_by_country_category, _, _ = filter_data_by_country_category(data)

    data = pd.DataFrame(filtered_df_by_country_category)

    if any(not isinstance(num, int) for num in data['likelihood']):
        data['likelihood'] = data['likelihood'].to_numeric()

    data.sort_values("likelihood", ascending=False, inplace=True)

    horizon_headers(period, len(data), show_view_all=False)

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


def filter_and_display_by_time_period(df: pd.DataFrame, period: str):
    filtered_df = df[df["due_date"] == period]

    filtered_df = filtered_df.sort_values("likelihood", ascending=False)

    if len(filtered_df) != 0:

        horizon_headers(period, len(filtered_df))

        # Display events in a grid
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        cols = [col1, col2, col3, col4]

        with st.container():
            st.markdown('<div class="cards-container">', unsafe_allow_html=True)

            for i, row in enumerate(filtered_df.head(4).itertuples()):
                with cols[i]:
                    add_one_event(row, period)

            st.markdown('</div>', unsafe_allow_html=True)


def horizon_headers(period: str, data_length: int, show_view_all: bool = True):

    button_css = insert_css(f"{settings.root_directory}/web/buttons.css")
    st.markdown(button_css, unsafe_allow_html=True)

    # TODO: Add support for checking the theme whenever streamlit update for it rolls out (track github issue)
    # will need to change color in .horizon-header h2
    horizon_headers_css = insert_css(f"{settings.root_directory}/web/horizon_headers.css")
    st.markdown(horizon_headers_css, unsafe_allow_html=True)

    view_all_button = f'<a href="potential_events_horizon?period={period}" class="view-all-button" target="_self">View All</a>' if show_view_all else ""
    st.markdown(
        f'<div class="horizon-header">'
        f'  <div class="horizon-header-content">'
        f'    <div class="horizon-header-left">'
        f'      <h2>'
        f'        {period} horizon'
        f'        <span class="event-count">{data_length} events</span>'
        f'      </h2>'
        f'    </div>'
        f'   {view_all_button}'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True
    )

def add_one_event(row, period):
    # TODO: Add support for checking the theme whenever streamlit update for it rolls out (track github issue)
    # will have to modify color of <h3 class="event-title">

    css = insert_css(f"{settings.root_directory}/web/blocks.css")
    st.markdown(css, unsafe_allow_html=True)

    st.markdown(
        f'<a href="event_details?event_id={row._1}&period={period}" target="_self" class="event-details-link">'
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

def show_full_event(event, period):
    # Render the event details with proper styling and tooltips

    if " - " in event["research"]:
        event["research"] = event["research"].replace("- ", "   - ")
    st.markdown(
        f"""
        <div class="outer-container">
            <div class="go-back-button">
                    <a href="/" target="_self">
                        Back to main page
                    </a>
                    <a href="potential_events_horizon?period={period}" target="_self">
                        Back to {period} horizon
                    </a>
            </div>
            <div class="custom-container">
              <div class="event-header">
                <h1 class="event-title">{event["potential_event"]}</h1>
                <div class="event-meta">
                  <span class="meta-chip date-chip" data-tooltip="Date when this event was added to the database">{event["research_date"]}</span>
                  <span class="meta-chip country-chip" data-tooltip="Country or region this event relates to">{event["research_country"]}</span>
                  <span class="meta-chip category-chip" data-tooltip="Category of the potential event">{event["category"]}</span>
                  <span class="meta-chip likelihood-chip" data-tooltip="Expected timeline for this event">{event["due_date"]}</span>
                </div>
              </div>
              <div class="event-content">
                {markdown.markdown(event["research"])}
              </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )