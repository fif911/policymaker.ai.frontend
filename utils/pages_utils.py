import streamlit as st
import base64
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import textwrap

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

def add_one_event(row, period):
    st.markdown(
        f'<a href="event_details?event_id={row._1}&period={period}" target="_self" style="color: inherit; text-decoration: none;">'
        f'  <div class="event-card">'
        f'      <div class="card-image">'
        f'          <img src="https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM=" '
        f'               alt="Event thumbnail">'
        f'      </div>'
        f'      <div class="card-content">'
        f'          <div>'
        f'              <h3 class="event-title">{textwrap.shorten(row.potential_event, width=SHOW_FIRST_SYMBOLS, placeholder="...")}</h3>'
        f'              <p class="event-reasoning">{textwrap.shorten(row.reasoning, width=SHOW_FIRST_SYMBOLS, placeholder="...")}</p>'
        f'          </div>'
        f'          <div class="event-meta">'
        f'              <span class="meta-chip likelihood-chip">Likelihood: {row.likelihood}</span>'
        f'              <span class="meta-chip category-chip">{row.category}</span>'
        f'              <span class="meta-chip country-chip">{row.research_country}</span>'
        f'          </div>'
        f'      </div>'
        f'  </div>'
        f'</a>',
        unsafe_allow_html=True
    )