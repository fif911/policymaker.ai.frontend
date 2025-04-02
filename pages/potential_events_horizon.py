import streamlit as st
import pandas as pd
from utils.mongo import get_mongo_connection
from utils.pages_visuals import add_sidebar_and_layout, layout_for_one_horizon_page
from utils.frontend_utils import insert_css

# Get the period from query parameters
query_params = st.query_params
period = query_params.get("period", None)

add_sidebar_and_layout("potential_events_horizon")

insert_css("web/buttons.css")

# Back button
st.markdown(
    f'<div class="go-back-button">'
    f'  <a href="/" target="_self">'
    f"Back to main page"
    f'  </a>'
    f'</div>',
    unsafe_allow_html=True
)

if period:

    events_for_period = get_mongo_connection().find({"due_date": period})
    data_for_period = pd.DataFrame(events_for_period.to_list())

    layout_for_one_horizon_page(data_for_period, period)
else:
    st.error("Please specify a time period in the URL parameters.")
