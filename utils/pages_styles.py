import streamlit as st

def blocks_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Fix Streamlit column responsiveness */
    [data-testid="column"] {
        width: calc(25% - 1rem) !important;
        flex: 1 1 calc(25% - 1rem) !important;
        min-width: calc(25% - 1rem) !important;
    }

    @media (max-width: 900px) {
        [data-testid="column"] {
            width: calc(50% - 1rem) !important;
            flex: 1 1 calc(50% - 1rem) !important;
            min-width: calc(50% - 1rem) !important;
        }
    }

    @media (max-width: 600px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
    
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
        width: 100%;
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
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 24px;
        padding: 0 0 8px 0;
        width: 100%;
    }

    @media screen and (max-width: 900px) {
        .cards-container {
            grid-template-columns: repeat(2, 1fr);
        }
        .event-card {
            min-height: 350px;
        }
    }

    @media screen and (max-width: 600px) {
        .cards-container {
            grid-template-columns: 1fr;
        }
        .event-card {
            min-height: 320px;
        }
        .card-image {
            height: 140px;
        }
    }

    .horizon-header {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
        margin: 8px 0 8px 0;
    }

    /* Fix stMarkdown width */
    .element-container, .stMarkdown {
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

def horizon_headers_style(period: str, data_length: int, show_view_all: bool = True):

    # TODO: Add support for checking the theme whenever streamlit update for it rolls out (track github issue)
    # will need to change color in .horizon-header h2

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
    view_all_button = f'<a href="potential_events_horizon?period={period}" class="view-all-button" target="_self">View All</a>' if show_view_all else ""
    st.markdown(
        f'<div class="horizon-header">'
        f'  <div class="horizon-header-content">'
        f'    <div class="horizon-header-left">'
        f'      <h2>'
        f'        {period} horizon'
        f'        <span class="event-count">{data_length} events</span>'
        f'      </h2>'
        f'    </div>'
        f'   {view_all_button}'
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

def event_details_style():
    st.markdown("""
        <style>
        .event-details {
            background: white;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .event-header {
            margin-bottom: 24px;
        }
        
        .event-title {
            font-size: 32px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 16px;
            line-height: 1.3;
        }
        
        .event-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 24px;
        }
        
        .meta-chip {
            background: #f5f5f5;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 14px;
            color: #666;
            position: relative;
            cursor: help;
        }
        
        .meta-chip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            padding: 8px 12px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            border-radius: 6px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1000;
            margin-top: 8px;
        }
        
        .meta-chip:hover::before {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-bottom-color: rgba(0, 0, 0, 0.8);
            margin-top: -4px;
        }
        
        .date-chip { background: #e3f2fd; color: #1976d2; }
        .country-chip { background: #e8f5e9; color: #2e7d32; }
        .category-chip { background: #fff3e0; color: #f57c00; }
        .likelihood-chip { background: #fce4ec; color: #c2185b; }
        
        .event-content {
            color: #333;
            line-height: 1.7;
            font-size: 17px;
        }
        
        .event-content h1 { font-size: 28px; margin: 32px 0 20px; }
        .event-content h2 { font-size: 24px; margin: 28px 0 16px; }
        .event-content h3 { font-size: 20px; margin: 24px 0 12px; }
        .event-content p { margin-bottom: 20px; }
        .event-content ul, .event-content ol { margin: 20px 0; padding-left: 28px; }
        .event-content li { margin-bottom: 12px; }
        .event-content a { color: #1976d2; text-decoration: none; }
        .event-content a:hover { text-decoration: underline; }
        .event-content blockquote {
            border-left: 4px solid #e0e0e0;
            margin: 24px 0;
            padding: 0 0 0 24px;
            color: #444;
            font-size: 18px;
        }
        .event-content code {
            background: #f5f5f5;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 15px;
        }
        .event-content pre {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 24px 0;
        }
        </style>
    """, unsafe_allow_html=True)
