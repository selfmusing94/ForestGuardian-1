import streamlit as st
import time
from datetime import datetime

def toggle_theme():
    """Toggle between light and dark theme"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
        # Update theme-specific CSS
        st.session_state.bg_color = "#121212"
        st.session_state.text_color = "#FFFFFF"
        st.session_state.secondary_bg_color = "#1E1E1E"
    else:
        st.session_state.theme = 'light'
        # Update theme-specific CSS
        st.session_state.bg_color = "#FFFFFF"
        st.session_state.text_color = "#262730"
        st.session_state.secondary_bg_color = "#F0F2F6"

def get_current_theme():
    """Get the current theme"""
    # Initialize theme-specific colors if not set
    if 'bg_color' not in st.session_state:
        if st.session_state.theme == 'dark':
            st.session_state.bg_color = "#121212"
            st.session_state.text_color = "#FFFFFF"
            st.session_state.secondary_bg_color = "#1E1E1E"
        else:
            st.session_state.bg_color = "#FFFFFF"
            st.session_state.text_color = "#262730"
            st.session_state.secondary_bg_color = "#F0F2F6"

    return st.session_state.theme

def apply_theme_css():
    """Apply CSS based on the current theme"""
    theme = get_current_theme()

    # Define CSS based on the current theme
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap');

        /* Animated nature theme gradients */
        @keyframes gradientFlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes colorPulse {{
            0% {{ filter: hue-rotate(0deg); }}
            50% {{ filter: hue-rotate(30deg); }}
            100% {{ filter: hue-rotate(0deg); }}
        }}

        :root {{
            --forest-gradient: linear-gradient(135deg, #2ecc71, #27ae60, #2ecc71);
            --sunset-gradient: linear-gradient(135deg, #e67e22, #d35400, #e67e22);
            --water-gradient: linear-gradient(135deg, #3498db, #2980b9, #3498db);
            --live-gradient: linear-gradient(45deg, #2ecc71, #3498db, #e67e22, #2ecc71);
        }}

        /* Live theme base styling */
        .stApp {{
            background: var(--live-gradient) !important;
            background-size: 400% 400% !important;
            animation: gradientFlow 15s ease infinite, colorPulse 10s ease infinite !important;
        }}

        /* Animated containers */
        div[data-testid="stContainer"], 
        div[data-testid="stMetricValue"],
        div[data-testid="stExpander"] {{
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}

        div[data-testid="stContainer"]:hover,
        div[data-testid="stMetricValue"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }}

        /* Base font styling with enhanced nature theme */
        .stApp, .stMarkdown, .stText {{
            font-family: 'Poppins', sans-serif !important;
            background: linear-gradient(180deg, rgba(46, 204, 113, 0.05), rgba(39, 174, 96, 0.02));
        }}

        /* Headings styling */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Roboto Slab', serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }}

        /* Metric value styling */
        div[data-testid="stMetricValue"] {{
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px;
        }}
        /* Enhanced sidebar styling with glass effect */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.15), rgba(52, 152, 219, 0.15)) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 10px 0 20px rgba(0, 0, 0, 0.2) !important;
            animation: sidebarEntrance 0.6s ease-out;
        }

        /* Enhance sidebar content */
        section[data-testid="stSidebar"] .block-container {
            background: rgba(255, 255, 255, 0.05) !important;
            padding: 2.5rem 1.5rem !important;
            border-radius: 15px !important;
            margin: 10px !important;
        }

        /* Sidebar title animation */
        section[data-testid="stSidebar"] h1 {
            background: linear-gradient(45deg, #2ecc71, #3498db) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            animation: titleGlow 3s ease-in-out infinite !important;
            font-size: 1.8em !important;
            margin-bottom: 1.5rem !important;
        }

        @keyframes sidebarEntrance {{
            from {{
                transform: translateX(-100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        /* Sidebar elements styling */
        section[data-testid="stSidebar"] .block-container {{
            padding: 2rem 1rem;
        }}

        section[data-testid="stSidebar"] h1 {{
            background: linear-gradient(45deg, #2ecc71, #3498db);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: titleGlow 3s ease-in-out infinite;
        }}

        @keyframes titleGlow {{
            0%, 100% {{ filter: brightness(100%); }}
            50% {{ filter: brightness(120%); }}
        }}

        /* Sidebar selectbox enhancement */
        section[data-testid="stSidebar"] .stSelectbox {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 5px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }}

        section[data-testid="stSidebar"] .stSelectbox:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        /* Slider styling in sidebar */
        section[data-testid="stSidebar"] .stSlider {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            transition: all 0.3s ease;
        }}

        section[data-testid="stSidebar"] .stSlider:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        /* Checkbox styling */
        section[data-testid="stSidebar"] .stCheckbox {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 10px;
            margin: 8px 0;
            transition: all 0.3s ease;
        }}

        section[data-testid="stSidebar"] .stCheckbox:hover {{
            transform: translateY(-2px);
        }}

        /* Alert sensitivity indicators */
        section[data-testid="stSidebar"] .row-widget.stMarkdown {{
            text-align: center;
            transition: all 0.3s ease;
        }}

        section[data-testid="stSidebar"] .row-widget.stMarkdown:hover {{
            transform: scale(1.05);
        }}

        /* Update notification styling */
        section[data-testid="stSidebar"] .element-container:last-child {{
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.1), rgba(52, 152, 219, 0.1));
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            border: 1px solid rgba(46, 204, 113, 0.2);
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.4); }}
            70% {{ box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }}
        }}

        /* Base app styling */
        .stApp {{
            background-color: {st.session_state.bg_color};
            color: {st.session_state.text_color} !important;
        }}

        /* Light and dark mode specific text colors for all elements */
        .stTextInput label, .stTextInput input,
        .stSelectbox label, .stSelectbox div,
        .stMultiSelect label, .stMultiSelect div,
        .stSlider label, .stSlider div,
        .stCheckbox label, .stRadio label,
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stMarkdownContainer"] a,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4,
        div[data-testid="stMarkdownContainer"] h5,
        div[data-testid="stMarkdownContainer"] h6,
        div[data-testid="stExpander"] summary span,
        div[data-testid="stExpander"] div p {{
            color: {st.session_state.text_color} !important;
        }}

        /* Ensure expander content is visible */
        details, details[open] {{
            background-color: {st.session_state.secondary_bg_color};
            color: {st.session_state.text_color} !important;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid {'rgba(255,255,255,0.1)' if theme == 'dark' else 'rgba(0,0,0,0.1)'};
        }}

        /* Ensure all text is visible */
        * {{
            color: {st.session_state.text_color} !important;
        }}

        /* Set specific elements with their appropriate colors */
        a {{
           color: {'#8AB4F8' if theme == 'dark' else '#0D6EFD'} !important;
        }}

        /* Improve data frame visibility */
        .stDataFrame div[data-testid="stTable"] {{
            background-color: {'rgba(255,255,255,0.05)' if theme == 'dark' else 'rgba(255,255,255,1)'};
            border-radius: 5px;
            padding: 2px;
        }}

        .stDataFrame div[data-testid="stTable"] table {{
            color: {st.session_state.text_color} !important;
        }}

        .stDataFrame div[data-testid="stTable"] th {{
            background-color: {'rgba(255,255,255,0.1)' if theme == 'dark' else 'rgba(240,242,246,1)'};
            color: {st.session_state.text_color} !important;
            font-weight: bold;
        }}

        .stDataFrame div[data-testid="stTable"] td {{
            background-color: {'rgba(255,255,255,0.05)' if theme == 'dark' else 'rgba(255,255,255,1)'};
            color: {st.session_state.text_color} !important;
        }}

        /* Enhanced Tabs styling */
        .stTabs [data-baseweb="tab-list"] {{
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.1), rgba(52, 152, 219, 0.1)) !important;
            border-radius: 10px;
            padding: 5px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            backdrop-filter: blur(10px);
        }}

        .stTabs [data-baseweb="tab"] {{
            color: {st.session_state.text_color} !important;
            font-weight: bold;
            transition: all 0.3s ease;
            border-radius: 8px;
            margin: 0 5px;
            padding: 8px 16px;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.2), rgba(52, 152, 219, 0.2));
            transform: translateY(-2px);
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.3), rgba(52, 152, 219, 0.3));
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        /* Map container enhancement */
        .element-container:has(iframe) {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1));
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}

        /* Plotly chart container styling */
        .stPlotlyChart {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1));
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}

        .stPlotlyChart:hover {{
            transform: translateY(-5px);
        }}

        /* Analysis section enhancement */
        div[data-testid="stContainer"] {{
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.05), rgba(52, 152, 219, 0.05));
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}

        div[data-testid="stContainer"]:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }}

        /* Metric styling */
        div[data-testid="stMetricValue"], span[data-testid="stMetricValue"] {{
            font-size: 1.5rem !important;
            font-weight: bold !important;
            color: {st.session_state.text_color} !important;
        }}

        div[data-testid="stMetricLabel"], span[data-testid="stMetricLabel"] {{
            color: {st.session_state.text_color} !important;
        }}

        div[data-testid="stMetricDelta"], span[data-testid="stMetricDelta"] {{
            font-weight: bold !important;
        }}

        /* Better contrast for elements in dark mode */
        .stSelectbox div, .stMultiSelect div {{
            background-color: {'rgba(255,255,255,0.1)' if theme == 'dark' else 'transparent'};
            border-radius: 5px;
            color: {st.session_state.text_color} !important;
        }}

        /* Improve select dropdown visibility */
        div[data-baseweb="select"] {{
            background-color: {'rgba(255,255,255,0.1)' if theme == 'dark' else 'transparent'};
            color: {st.session_state.text_color} !important;
            border-radius: 5px;
        }}

        div[data-baseweb="select"] option {{
            background-color: {'#1E1E1E' if theme == 'dark' else '#FFFFFF'};
            color: {st.session_state.text_color} !important;
        }}

        /* Improved container styling */
        div[data-testid="stContainer"] {{
            background-color: {'rgba(255,255,255,0.05)' if theme == 'dark' else 'rgba(0,0,0,0.02)'};
            padding: 10px;
            border-radius: 5px;
            border: 1px solid {'rgba(255,255,255,0.1)' if theme == 'dark' else 'rgba(0,0,0,0.05)'};
        }}

        /* Map container styling */
        .map-container {{
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }}

        /* Fix for vertical text in Folium maps and other elements */
        .leaflet-container .leaflet-control-layers,
        .leaflet-control, 
        .leaflet-popup-content,
        .leaflet-tooltip,
        .leaflet-control-layers-list,
        .folium-map span, 
        .folium-map p,
        .folium-map a,
        .folium-map div,
        .folium-control-layers, 
        .folium-control,
        .leaflet-control-zoom,
        .leaflet-bar,
        .leaflet-control-attribution,
        .folium-map button {{
            font-family: 'Arial', sans-serif !important;
            text-orientation: mixed !important;
            writing-mode: horizontal-tb !important;
            text-align: left !important;
            letter-spacing: normal !important;
            word-spacing: normal !important;
            direction: ltr !important;
            text-rendering: auto !important;
        }}

        /* Info box styling */
        div[data-testid="stAlert"] {{
            background-color: {'rgba(66, 150, 250, 0.2)' if theme == 'dark' else 'rgba(66, 150, 250, 0.1)'};
            color: {'#8AB4F8' if theme == 'dark' else '#1E5A96'} !important;
        }}

        div[data-testid="stAlert"] p {{
            color: {'#FFFFFF' if theme == 'dark' else '#1E5A96'} !important;
        }}

        /* Success message styling */
        div[data-testid="stSuccessMessage"] {{
            background-color: {'rgba(45, 200, 65, 0.2)' if theme == 'dark' else 'rgba(45, 200, 65, 0.1)'};
            color: {'#A7F3D0' if theme == 'dark' else '#047857'} !important;
        }}

        div[data-testid="stSuccessMessage"] p {{
            color: {'#FFFFFF' if theme == 'dark' else '#047857'} !important;
        }}

        /* Risk level styling with brighter colors for dark mode */
        .risk-high {{
            color: {'#FF6B6B' if theme == 'dark' else '#E53935'} !important;
            font-weight: bold;
        }}

        .risk-medium {{
            color: {'#FFD166' if theme == 'dark' else '#FB8C00'} !important;
            font-weight: bold;
        }}

        .risk-low {{
            color: {'#A7F3D0' if theme == 'dark' else '#388E3C'} !important;
            font-weight: bold;
        }}

        /* Alert box styling and animation */
        @keyframes alertPulse {{
            0% {{ transform: scale(1); background-position: 0% 50%; }}
            50% {{ transform: scale(1.02); background-position: 100% 50%; }}
            100% {{ transform: scale(1); background-position: 0% 50%; }}
        }}

        /* Alert badge styling */
        .alert-badge {{
            background: var(--live-gradient);
            background-size: 200% 200%;
            color: white !important;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 13px;
            margin-left: 8px;
            font-weight: bold;
            box-shadow: 0 2px 15px rgba(52, 152, 219, 0.3);
            animation: alertPulse 3s infinite, gradientFlow 15s ease infinite, colorPulse 10s ease infinite;
            display: inline-block;
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }}

        .alert-badge:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(255, 82, 82, 0.4);
        }}

        /* Tooltip styling */
        .tooltip {{
            position: relative;
            display: inline-block;
        }}

        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 120px;
            background-color: {'#444444' if theme == 'dark' else 'black'};
            color: white !important;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -60px;
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}

        /* Animation for icons */
        .animated-icon {{
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}

        /* Nature-themed buttons */
        .stButton > button {{
            background: var(--forest-gradient) !important;
            color: white !important;
            border: none !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3) !important;
        }}

        /* Metric containers with forest theme */
        div[data-testid="stMetricValue"] {{
            background: var(--forest-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold !important;
        }}

        /* Enhanced alerts styling */
        div[data-testid="stExpander"] {{
            border-left: 4px solid #2ecc71;
            transition: all 0.3s ease;
        }}

        /* Animated text styles */

        /* Button styling */
        button, .stButton>button {{
            background-color: {'#2E2E2E' if theme == 'dark' else '#F0F2F6'};
            color: {'#FFFFFF' if theme == 'dark' else '#262730'} !important;
            border: 1px solid {'rgba(255,255,255,0.2)' if theme == 'dark' else 'rgba(0,0,0,0.1)'};
            border-radius: 5px;
            transition: all 0.3s ease;
            text-orientation: mixed !important;
            writing-mode: horizontal-tb !important;
            text-align: center !important;
            letter-spacing: normal !important;
            word-spacing: normal !important;
            font-family: 'Arial', sans-serif !important;
        }}

        button:hover, .stButton>button:hover {{
            background-color: {'#3E3E3E' if theme == 'dark' else '#E6E9EF'};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        /* Ensure button text is always horizontal and properly displayed */
        .stButton button p,
        .stButton button span,
        .stButton button div,
        .stButton button,
        button span, 
        button p, 
        button div {{
            text-orientation: mixed !important;
            writing-mode: horizontal-tb !important;
            text-align: center !important;
            direction: ltr !important;
            display: block !important;
            font-family: 'Arial', sans-serif !important;
        }}

        /* Slider styling */
        .stSlider {{
            padding-top: 2rem;
        }}

        .stSlider div[data-baseweb="slider"] {{
            margin-top: 1rem;
        }}

        /* Footer styling */
        .st-emotion-cache-164nlkn {{
            background-color: {'#1E1E1E' if theme == 'dark' else '#F0F2F6'};
            color: {'#CCCCCC' if theme == 'dark' else '#666666'} !important;
        }}

        /* Enhanced expander styling for alerts */
        div[data-testid="stExpander"] {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.2)) !important;
            background-size: 300% 300% !important;
            border-radius: 15px !important;
            border: 2px solid rgba(46, 204, 113, 0.3) !important;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            margin: 15px 0;
            transition: all 0.3s ease !important;
            animation: alertGradient 8s ease infinite;
            backdrop-filter: blur(8px);
            padding: 20px !important;
        }}

        /* Style multiselect and slider in alert box */
        div[data-testid="stExpander"] .stMultiSelect,
        div[data-testid="stExpander"] .stSlider {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            backdrop-filter: blur(5px);
        }}

        /* Alert title styling */
        div[data-testid="stExpander"] > div:first-child {{
            font-size: 1.2em !important;
            font-weight: 600 !important;
            color: #2ecc71 !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 15px !important;
            border-bottom: 2px solid rgba(46, 204, 113, 0.2);
            padding-bottom: 15px !important;
        }}

        @keyframes alertGradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        div[data-testid="stExpander"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(46, 204, 113, 0.4) !important;
        }}

        /* Alert content styling */
        div[data-testid="stExpander"] > div {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.1) 100%);
            border-radius: 8px;
            padding: 15px !important;
            margin-top: 10px;
        }}

        /* Alert header styling */
        div[data-testid="stExpander"] > div:first-child {{
            border-bottom: 1px solid rgba(46, 204, 113, 0.2);
            padding-bottom: 10px !important;
        }}
    </style>
    """

    # Return the CSS
    return css

def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}"

def calculate_risk_color(risk_score):
    """Return a color based on risk score"""
    if risk_score < 30:
        return "green"
    elif risk_score< 70:
        return "orange"
    else:
        return "red"

def risk_level_text(risk_score):
    """Return a text description of risk level"""
    if risk_score < 30:
        return "Low Risk"
    elif risk_score < 70:
        return "Medium Risk"
    else:
        return "High Risk"

def risk_level_html(risk_score):
    """Return HTML with appropriate risk styling"""
    level = risk_level_text(risk_score)
    css_class = ""

    if risk_score < 30:
        css_class = "risk-low"
    elif risk_score < 70:
        css_class = "risk-medium"
    else:
        css_class = "risk-high"

    return f'<span class="{css_class}">{level}</span>'

def calculate_percentage_change(old_value, new_value):
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100 if new_value > 0 else 0
    return ((new_value - old_value) / old_value) * 100

def show_notification(message, icon="🔔"):
    """Display a temporary notification message"""
    notification = st.empty()
    notification.info(f"{icon} {message}")
    time.sleep(3)
    notification.empty()

def get_time_since(timestamp):
    """Return a human-readable string of time since the given timestamp"""
    now = datetime.now()
    delta = now - timestamp

    if delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.seconds >= 3600:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta.seconds >= 60:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"