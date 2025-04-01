from string import whitespace
import textwrap
import streamlit as st
import pandas as pd
import base64
from utils.mongo import get_mongo_connection
from utils.pages_styles import horizon_headers_style
# from utils.pages_visuals import add_one_event

TITLE_SYMBOLS = 100
REASONING_SYMBOLS = 120

@st.cache_data
def load_data():
    """Load data from MongoDB"""
    data = get_mongo_connection().find().to_list()
    return data

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

def filter_and_display_by_time_period(df: pd.DataFrame, period: str):
    filtered_df = df[df["due_date"] == period]

    filtered_df = filtered_df.sort_values("likelihood", ascending=False)

    if len(filtered_df) != 0:
        horizon_headers_style(period, len(filtered_df))

        # Display events in a grid
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        cols = [col1, col2, col3, col4]

        with st.container():
            st.markdown('<div class="cards-container">', unsafe_allow_html=True)

            for i, row in enumerate(filtered_df.head(4).itertuples()):
                with cols[i]:
                    add_one_event(row, period)

            st.markdown('</div>', unsafe_allow_html=True)

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
