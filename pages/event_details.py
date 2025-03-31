import streamlit as st
from utils.pages_styles import go_back_button_style

# Page layout and styles
st.set_page_config(layout="wide", page_title="Policymakers AI Main Page",)

query_params = st.query_params
event_id = query_params.get("event_id", None)
row = query_params.get("row", None)
period = query_params.get("period", None)

go_back_button_style()

if event_id:
    # Fetch event details based on event_id
    st.write(f"Displaying details for event ID: {event_id}")
    if st.button("Go to main", key=f"{event_id}_main"):
        st.switch_page("app.py")

    # TODO: Has to be a href
    if st.button(f"Go to view all for {period} horizon", key=f"{event_id}_{period}"):
        st.switch_page(f"potential_events_horizon.py?period={period}")

    # TODO: Query mongo
else:
    st.write("You did not pass a query parameter event_id. Please make sure you pass it.")
