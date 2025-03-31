import streamlit as st

def blocks_style():

    st.markdown("""
    <style>
    .event-card {
        display: flex;
        flex-direction: column;
        min-height: 380px;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 0;
        box-sizing: border-box;
    }

    .card-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .card-image {
        flex: 0 0 auto;
        height: 200px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .event-card h3, .event-card p {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


def horizon_headers_style(period: str, data_length: int):

    st.markdown(f'<div style="height:20px;"></div>', unsafe_allow_html=True)  # Adds a 20px spacer
    st.markdown(f'<h3 style="margin-bottom: 2px;">{period} horizon (total amount of events: {data_length})</h3>',
                unsafe_allow_html=True)
    st.markdown('<hr style="margin-bottom: 10px;">', unsafe_allow_html=True)

def view_all_button_style():
    # Custom CSS for button styling
    st.markdown("""
       <style>
       .stButton > button {
           color: white;
           padding: 10px 20px;
           border: none;
           border-radius: 5px;
           cursor: pointer;
           float: right;
       }
       </style>
       """, unsafe_allow_html=True)

def go_back_button_style():
    # Custom CSS for button styling
    st.markdown("""
         <style>
         .stButton > button {
             color: white;
             padding: 10px 20px;
             border: none;
             border-radius: 5px;
             cursor: pointer;
             float: left;
         }
         </style>
         """, unsafe_allow_html=True)
