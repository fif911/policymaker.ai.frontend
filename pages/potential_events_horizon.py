import streamlit as st
from utils.pages_filters import layout_for_one_horizon_page
from utils.pages_styles import blocks_style, go_back_button_style

# Check if the data exists in session state
if 'view_all_data' in st.session_state:
    # Page layout
    st.set_page_config(layout="wide", page_title=f"Policymakers AI, all events for {st.session_state.period} horizon", )
    layout_for_one_horizon_page(st.session_state.view_all_data, st.session_state.period)
    blocks_style()
    go_back_button_style()
    # Optionally, clear the data from session state after using it
    # del st.session_state.view_all_data

else:
    # TODO: Query mongo
    st.write("No data to display. Please go back and click 'View All'.")
