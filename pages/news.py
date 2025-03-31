import streamlit as st
import pandas as pd
import base64
import textwrap
from random import choices
from utils.frontend_utils import load_data

IMAGE_SIZE = [200, 200]
SHOW_FIRST_SYMBOLS = 80

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

        st.markdown(f"### {period} horizon")
        st.markdown("---")
        # "View All" button aligned right
        st.markdown("<div style='text-align: right; margin-top: 0px'><button>View All</button></div>", unsafe_allow_html=True)

        # Display events in a grid
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]

        # TODO: Get uuids

        for i, row in enumerate(filtered_df.head(4).itertuples()):
            with cols[i]:
                # Outer container to align both square and text blocks vertically
                st.markdown(
                    f'<div style="display:flex; flex-direction:column; justify-content:flex-start; align-items:center; height:400px; border:1px solid #ddd; border-radius:10px;">' # TODO: Calculate heights based on text length
                    f'<div style="width:{IMAGE_SIZE[0]}px; height:{IMAGE_SIZE[1]}px; padding:10px; display:flex; justify-content:center; align-items:center;">'
                    f'<img src="https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM=" alt="Random Image" style="max-width:{IMAGE_SIZE[0]}px; max-height:{IMAGE_SIZE[1]}px; margin-top: 30px">'
                    f'</div>'
                    f'<div style="text-align:center; margin-top:20px;">'
                    f'<b>Potential event:</b> {textwrap.shorten(row.potential_event, width=SHOW_FIRST_SYMBOLS, placeholder="...")}<br>'
                    f'<b>Reasoning:</b> {textwrap.shorten(row.reasoning, width=SHOW_FIRST_SYMBOLS, placeholder="...")}<br>'
                    f'<b>Likelihood:</b> {row.likelihood}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

# Page layout
st.set_page_config(layout="wide")

loaded_data = load_data()

df = pd.DataFrame(loaded_data)

df["likelihood"] = choices(range(1,10),k=len(df))

df["due_date_score"] = convert_due_dates_into_dates(df["due_date"])

df.sort_values("due_date_score", ascending=True, inplace=True)

filtered_data = filter_by_country_category(df)

for period in df["due_date"].unique():
    filter_and_display_by_time_period(filtered_data, period)
