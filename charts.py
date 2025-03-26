import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st

def plot_deforestation_trend(deforestation_data):
    """
    Create a line chart showing deforestation trends over time
    
    Parameters:
    deforestation_data: Dictionary with deforestation data
    
    Returns:
    Plotly figure object
    """
    # Extract yearly data
    df = deforestation_data['raw_data']
    yearly_data = df.groupby('year')['deforestation_hectares'].sum().reset_index()
    
    # Create line chart
    fig = px.line(
        yearly_data, 
        x='year', 
        y='deforestation_hectares',
        title=f"Annual Deforestation Trend in {deforestation_data['region']}",
        labels={
            'year': 'Year',
            'deforestation_hectares': 'Deforested Area (hectares)'
        }
    )
    
    # Customize layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Deforested Area (hectares)",
        hovermode="x unified",
        height=400
    )
    
    # Add data points
    fig.add_trace(
        go.Scatter(
            x=yearly_data['year'],
            y=yearly_data['deforestation_hectares'],
            mode='markers',
            name='Annual Data'
        )
    )
    
    return fig

def plot_biodiversity_impact(biodiversity_data):
    """
    Create a bar chart showing species impact by category
    
    Parameters:
    biodiversity_data: Dictionary with biodiversity data
    
    Returns:
    Plotly figure object
    """
    # Extract species distribution data
    species_dist = biodiversity_data['species_distribution']
    
    # Create DataFrame for plotting
    df = pd.DataFrame(species_dist)
    
    # Calculate percentage at risk
    df['percent_at_risk'] = (df['at_risk'] / df['count']) * 100
    
    # Create stacked bar chart
    fig = go.Figure()
    
    # Add bars for species at risk
    fig.add_trace(
        go.Bar(
            x=df['category'],
            y=df['at_risk'],
            name='At Risk',
            marker_color='red'
        )
    )
    
    # Add bars for species not at risk
    fig.add_trace(
        go.Bar(
            x=df['category'],
            y=df['count'] - df['at_risk'],
            name='Not at Risk',
            marker_color='green'
        )
    )
    
    # Customize layout
    fig.update_layout(
        title="Biodiversity Impact by Species Category",
        xaxis_title="Species Category",
        yaxis_title="Number of Species",
        barmode='stack',
        hovermode="x unified",
        height=400
    )
    
    return fig

def plot_risk_distribution(biodiversity_data):
    """
    Create a pie chart showing risk distribution
    
    Parameters:
    biodiversity_data: Dictionary with biodiversity data
    
    Returns:
    Plotly figure object
    """
    # Extract risk distribution data
    risk_dist = biodiversity_data['risk_distribution']
    
    # Create DataFrame for plotting
    df = pd.DataFrame(risk_dist)
    
    # Colors for each risk level
    colors = {
        'Low Risk': 'green',
        'Medium Risk': 'orange',
        'High Risk': 'red'
    }
    
    color_list = [colors.get(level, 'gray') for level in df['level']]
    
    # Create pie chart
    fig = px.pie(
        df,
        values='percentage',
        names='level',
        title="Species Risk Distribution",
        color_discrete_sequence=color_list
    )
    
    # Customize layout
    fig.update_layout(
        height=400
    )
    
    # Update trace properties
    fig.update_traces(
        textinfo='percent+label',
        hole=0.3
    )
    
    return fig
