import streamlit as st
import pandas as pd
from utils.mongo import get_mongo_connection
from utils.pages_filters import layout_for_one_horizon_page
from utils.pages_styles import blocks_style, go_back_button_style
from utils.pages_utils import add_sidebar_and_layout

# Get the period from query parameters
query_params = st.query_params
period = query_params.get("period", None)

add_sidebar_and_layout("potential_events_horizon")

# Back button
st.markdown(
    f'<div style="margin-bottom: 24px;">'
    f'  <a href="/" target="_self" style="color: white; background-color: #333; padding: 8px 16px; border-radius: 16px; text-decoration: none;">'
    f"Back to main page"
    f'  </a>'
    f'</div>',
    unsafe_allow_html=True
)

if period:

    events_for_period = get_mongo_connection().find({"due_date": period})
    data_for_period = pd.DataFrame(events_for_period.to_list())

    layout_for_one_horizon_page(data_for_period, period)
    blocks_style()
    go_back_button_style()

else:
    st.error("Please specify a time period in the URL parameters.")
