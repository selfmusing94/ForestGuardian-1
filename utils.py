import streamlit as st

def toggle_theme():
    """Toggle between light and dark theme"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

def get_current_theme():
    """Get the current theme"""
    return st.session_state.theme

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

def calculate_percentage_change(old_value, new_value):
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100 if new_value > 0 else 0
    return ((new_value - old_value) / old_value) * 100
