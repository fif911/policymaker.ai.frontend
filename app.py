import streamlit as st
import pandas as pd
from random import choices
from utils.pages_styles import blocks_style
from utils.frontend_utils import filter_data_by_country_category, filter_and_display_by_time_period, convert_due_dates_into_dates
from utils.pages_visuals import add_sidebar_and_layout


add_sidebar_and_layout("app")

blocks_style()

# TODO: Where to put button to check the graph out?

filtered_df_by_country_category, _, _ = filter_data_by_country_category()

df = pd.DataFrame(filtered_df_by_country_category)

df["likelihood"] = choices(range(1, 10), k=len(df)) # TODO: Wait for Yehor to change in mongo

df["due_date_score"] = convert_due_dates_into_dates(df["due_date"])

df.sort_values("due_date_score", ascending=True, inplace=True)

for period in df["due_date"].unique():

    filter_and_display_by_time_period(df, period)
