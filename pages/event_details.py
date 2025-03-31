import streamlit as st

from utils.mongo import get_mongo_connection
from utils.pages_styles import go_back_button_style
from bson import ObjectId
from utils.pages_utils import decode_base64

# Page layout and styles
st.set_page_config(layout="wide", page_title="Policymakers AI Main Page",)

query_params = st.query_params
event_id = query_params.get("event_id", None)
row = query_params.get("row", None)
period = query_params.get("period", None)

go_back_button_style()

if event_id:
    st.markdown(
        f'<a href="/" target="_self" style="color: white; background-color: #333; padding: 5px; border-radius: 5px; text-decoration: none;">'
        f"Go to main page"
        f'</a>', unsafe_allow_html=True)

    st.markdown(
        f'<a href="potential_events_horizon?period={period}" target="_self" style="color: white; background-color: #333; padding: 5px; border-radius: 5px; text-decoration: none;">'
        f"Go to view all for {period} horizon"
        f'</a>', unsafe_allow_html=True)

    event = get_mongo_connection().find_one({"_id": ObjectId(event_id)})

    event["research"] = decode_base64(event["research"])

    # TODO: Parse
    st.write(event)

else:
    st.write("You did not pass a query parameter event_id. Please make sure you pass it.")
