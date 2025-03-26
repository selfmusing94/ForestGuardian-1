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
        .stApp {{
            background-color: {st.session_state.bg_color};
            color: {st.session_state.text_color};
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {st.session_state.secondary_bg_color};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {st.session_state.text_color};
        }}
        
        .stDataFrame {{
            background-color: {st.session_state.secondary_bg_color};
        }}
        
        div[data-testid="stMetricValue"] {{
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .map-container {{
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .risk-high {{
            color: #FF5252;
            font-weight: bold;
        }}
        
        .risk-medium {{
            color: #FFA726;
            font-weight: bold;
        }}
        
        .risk-low {{
            color: #66BB6A;
            font-weight: bold;
        }}
        
        .alert-badge {{
            background-color: #FF5252;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 6px;
        }}
        
        .tooltip {{
            position: relative;
            display: inline-block;
        }}
        
        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 120px;
            background-color: black;
            color: #fff;
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
        
        .animated-icon {{
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{
                opacity: 1;
            }}
            50% {{
                opacity: 0.5;
            }}
            100% {{
                opacity: 1;
            }}
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
    elif risk_score < 70:
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
