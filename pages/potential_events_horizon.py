import streamlit as st
import pandas as pd

from utils.mongo import get_mongo_connection
from utils.pages_filters import layout_for_one_horizon_page
from utils.pages_styles import blocks_style, go_back_button_style

query_params = st.query_params
period = query_params.get('period', None)

# Check if the data exists in session state
if period:
    # Page layout
    st.set_page_config(layout="wide", page_title=f"Policymakers AI, all events for {period} horizon", )

    events_for_period = get_mongo_connection().find({"due_date": period})
    data_for_period = pd.DataFrame(events_for_period.to_list())

    layout_for_one_horizon_page(data_for_period, period)
    blocks_style()
    go_back_button_style()

else:
    st.write("You did not pass a query parameter period. Please make sure you pass it.")

