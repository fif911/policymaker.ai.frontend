import streamlit as st
import re
from utils.mongo import get_mongo_connection
from bson import ObjectId
from utils.frontend_utils import decode_base64
from utils.pages_visuals import add_sidebar_and_layout
from utils.frontend_utils import insert_css
from utils.pages_visuals import show_full_event
from config import settings

# Page layout and styles
add_sidebar_and_layout("event_details")

query_params = st.query_params
event_id = query_params.get("event_id", None)
row = query_params.get("row", None)
period = query_params.get("period", None)

button_css = insert_css(f"{settings.root_directory}/web/buttons.css")
st.markdown(button_css, unsafe_allow_html=True)

if event_id:
    event = get_mongo_connection().find_one({"_id": ObjectId(event_id)})
    event["research"] = decode_base64(event["research"])

    event_details_style_css = insert_css(f"{settings.root_directory}/web/event_details.css")
    st.markdown(event_details_style_css, unsafe_allow_html=True)

    # Remove content between <think> tags
    event["research"] = re.sub(r'<think>.*?</think>', '', event["research"], flags=re.DOTALL)

    show_full_event(event, period)
else:
    st.markdown(
        f'<div class="go-back-button">'
        f'  <a href="/" target="_self">'
        f"Back to main page"
        f'  </a>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.error("You did not pass a query parameter event_id. Please make sure you pass it.")
