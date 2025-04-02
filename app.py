import streamlit as st
import pandas as pd
from utils.frontend_utils import filter_data_by_country_category, convert_due_dates_into_dates
from utils.pages_visuals import add_sidebar_and_layout, filter_and_display_by_time_period
from utils.frontend_utils import insert_css

add_sidebar_and_layout("app")

# TODO: Where to put button to check the graph out?

filtered_df_by_country_category, _, _ = filter_data_by_country_category()

df = pd.DataFrame(filtered_df_by_country_category)

categories = df['category'].unique()
color_map = {}
colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#FF6D01", "#46BDC6", "#7B1FA2", "#C2185B",
          "#1A73E8", "#D93025", "#F9AB00", "#1E8E3E", "#E37400", "#00ACC1", "#6A1B9A", "#B00020"]
for i, category in enumerate(categories):
    color_map[category] = colors[i % len(colors)]

df.sort_values("due_date_score", ascending=True, inplace=True)

for period in df["due_date"].unique():
    filter_and_display_by_time_period(df, period)
