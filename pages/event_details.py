import streamlit as st
import markdown
import re

from utils.mongo import get_mongo_connection
from utils.pages_styles import go_back_button_style, event_details_style
from bson import ObjectId
from utils.pages_utils import decode_base64

# Page layout and styles
st.set_page_config(layout="wide", page_title="Policymakers AI Main Page",initial_sidebar_state="collapsed")
event_details_style()

query_params = st.query_params
event_id = query_params.get("event_id", None)
row = query_params.get("row", None)
period = query_params.get("period", None)

go_back_button_style()

if event_id:
    st.markdown(
        f'<div style="margin-bottom: 24px;">'
        f'  <a href="/" target="_self" style="color: white; background-color: #333; padding: 8px 16px; border-radius: 16px; text-decoration: none; margin-right: 12px;">'
        f"Back to main page"
        f'  </a>'
        f'  <a href="potential_events_horizon?period={period}" target="_self" style="color: white; background-color: #333; padding: 8px 16px; border-radius: 16px; text-decoration: none;">'
        f"Back to {period} horizon"
        f'  </a>'
        f'</div>',
        unsafe_allow_html=True
    )

    event = get_mongo_connection().find_one({"_id": ObjectId(event_id)})
    event["research"] = decode_base64(event["research"])
    
    # Remove content between <think> tags
    event["research"] = re.sub(r'<think>.*?</think>', '', event["research"], flags=re.DOTALL)

    # Render the event details with proper styling and tooltips
    st.markdown(
        f'<div class="event-details">'
        f'  <div class="event-header">'
        f'    <h1 class="event-title">{event["potential_event"]}</h1>'
        f'    <div class="event-meta">'
        f'      <span class="meta-chip date-chip" data-tooltip="Date when this event was added to the database">{event["research_date"]}</span>'
        f'      <span class="meta-chip country-chip" data-tooltip="Country or region this event relates to">{event["research_country"]}</span>'
        f'      <span class="meta-chip category-chip" data-tooltip="Category of the potential event">{event["category"]}</span>'
        f'      <span class="meta-chip likelihood-chip" data-tooltip="Expected timeline for this event">{event["due_date"]}</span>'
        f'    </div>'
        f'  </div>'
        f'  <div class="event-content">'
        f'    {markdown.markdown(event["research"])}'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True
    )

else:
    st.error("You did not pass a query parameter event_id. Please make sure you pass it.")
    st.markdown(
        f'<div style="margin-bottom: 24px;">'
        f'  <a href="/" target="_self" style="color: white; background-color: #333; padding: 8px 16px; border-radius: 16px; text-decoration: none; margin-right: 12px;">'
        f"Back to main page"
        f'  </a>'
        f'</div>',
        unsafe_allow_html=True
    )
