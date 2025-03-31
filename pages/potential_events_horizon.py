import streamlit as st
from utils.pages_filters import layout_for_one_horizon_page

# Check if the data exists in session state
if 'view_all_data' in st.session_state:
    layout_for_one_horizon_page(st.session_state.view_all_data, st.session_state.period)
    # Optionally, clear the data from session state after using it
    # del st.session_state.view_all_data
else:
    st.write("No data to display. Please go back and click 'View All'.")
