import streamlit as st

def blocks_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    .event-card {
        display: flex;
        flex-direction: column;
        min-height: 380px;
        background: white;
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 0;
        box-sizing: border-box;
        transition: all 0.2s ease-in-out;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }

    .event-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
    }

    .card-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 16px;
    }

    .card-image {
        flex: 0 0 auto;
        height: 180px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 12px;
        overflow: hidden;
        background: #f8f9fa;
        margin-bottom: 16px;
    }

    .card-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .event-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
        line-height: 1.4;
        margin: 0 0 12px 0;
    }

    .event-reasoning {
        font-size: 14px;
        color: #4a4a4a;
        line-height: 1.6;
        margin: 0;
    }

    .event-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 16px;
    }

    .meta-chip {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        background: #f0f2f5;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
        color: #4a4a4a;
    }

    .likelihood-chip {
        background: #e3f2fd;
        color: #1976d2;
    }

    .category-chip {
        background: #f3e5f5;
        color: #7b1fa2;
    }

    .country-chip {
        background: #e8f5e9;
        color: #2e7d32;
    }

    .cards-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 24px;
        padding: 0 0 8px 0;
    }

    .horizon-header {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
        margin: 8px 0 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def horizon_headers_style(period: str, data_length: int):
    st.markdown("""
        <style>
        .horizon-header {
            font-family: 'Inter', sans-serif;
            color: #1a1a1a;
            margin: 8px 0 8px 0;
        }
        .horizon-header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .horizon-header-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .horizon-header h2 {
            font-size: 24px;
            font-weight: 600;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .horizon-header .event-count {
            font-size: 14px;
            color: #666;
            background: #f0f2f5;
            padding: 4px 12px;
            border-radius: 16px;
            font-weight: 500;
        }
        .view-all-button {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            background: #e3f2fd;
            color: #1976d2;
            border-radius: 16px;
            font-size: 14px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s ease-in-out;
        }
        .view-all-button:hover {
            background: #bbdefb;
            transform: translateY(-1px);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="horizon-header">'
        f'  <div class="horizon-header-content">'
        f'    <div class="horizon-header-left">'
        f'      <h2>'
        f'        {period} horizon'
        f'        <span class="event-count">{data_length} events</span>'
        f'      </h2>'
        f'    </div>'
        f'    <a href="potential_events_horizon?period={period}" class="view-all-button" target="_self">View All</a>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True
    )

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
