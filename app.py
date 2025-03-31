import streamlit as st
import pandas as pd
from random import choices
from utils.pages_styles import blocks_style
from utils.frontend_utils import load_data
from utils.pages_utils import convert_due_dates_into_dates
from utils.pages_filters import filter_by_country_category, filter_and_display_by_time_period

# Page layout and styles
st.set_page_config(layout="wide", page_title="Policymakers AI Main Page",)
blocks_style()

collection = load_data()
loaded_data = collection.find().to_list()

# st.write(loaded_data)

df = pd.DataFrame(loaded_data) # TODO: Cache in some way

df["likelihood"] = choices(range(1, 10), k=len(df)) # TODO: Wait for Yehor to change in mongo

df["due_date_score"] = convert_due_dates_into_dates(df["due_date"])

df.sort_values("due_date_score", ascending=True, inplace=True)

filtered_df_by_country_category = filter_by_country_category(df)

for period in filtered_df_by_country_category["due_date"].unique():

    filter_and_display_by_time_period(filtered_df_by_country_category, period)
