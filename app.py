import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import custom modules
from utils import toggle_theme, get_current_theme
from data_processor import load_deforestation_data, load_biodiversity_data, load_alert_data
from map_visualization import create_map, create_time_lapse_map
from charts import plot_deforestation_trend, plot_biodiversity_impact, plot_risk_distribution

# Page configuration
st.set_page_config(
    page_title="Forest Guardian - Deforestation Tracking Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def main():
    # Sidebar
    with st.sidebar:
        st.image("assets/forest_logo.svg", width=80)
        st.title("Forest Guardian")
        st.subheader("Deforestation & Biodiversity Dashboard")
        
        # Theme toggle
        current_theme = get_current_theme()
        if st.button("Toggle Theme 🌓", key="theme_toggle"):
            toggle_theme()
            st.rerun()
        
        st.markdown("---")
        
        # Region filter
        regions = ["Amazon", "Congo Basin", "Southeast Asia", "Central America", "Global"]
        selected_region = st.selectbox("Select Region:", regions)
        
        # Time period filter
        st.subheader("Time Period")
        years = list(range(2015, datetime.now().year + 1))
        selected_year_range = st.select_slider(
            "Select Year Range:",
            options=years,
            value=(years[0], years[-1])
        )
        
        # Layer toggles for map
        st.subheader("Map Layers")
        show_deforestation = st.checkbox("Deforestation Heatmap", value=True)
        show_protected_areas = st.checkbox("Protected Areas", value=True)
        show_risk_zones = st.checkbox("Risk Zones", value=True)
        
        # Alert settings
        st.subheader("Alert Settings")
        alert_threshold = st.select_slider(
            "Alert Sensitivity:",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        notify_email = st.checkbox("Email Notifications", value=False)
        if notify_email:
            email = st.text_input("Email Address")
        
        notify_sms = st.checkbox("SMS Notifications", value=False)
        if notify_sms:
            phone = st.text_input("Phone Number")
            
        st.markdown("---")
        st.info("Dashboard updates every 24 hours with new satellite data.")

    # Main content
    # Load data based on filters
    deforestation_data = load_deforestation_data(selected_region, selected_year_range)
    biodiversity_data = load_biodiversity_data(selected_region, selected_year_range)
    alert_data = load_alert_data(selected_region, alert_threshold)
    
    # Header with key metrics
    st.title(f"Deforestation & Biodiversity Dashboard: {selected_region}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Forest Loss", 
            value=f"{deforestation_data['total_loss_hectares']:,.0f} ha",
            delta=f"{deforestation_data['loss_change_percent']:.1f}%"
        )
    
    with col2:
        st.metric(
            label="Species at Risk", 
            value=biodiversity_data['species_at_risk'],
            delta=biodiversity_data['species_change']
        )
    
    with col3:
        risk_score = biodiversity_data['risk_score']
        risk_level = "Low" if risk_score < 30 else "Medium" if risk_score < 70 else "High"
        risk_color = "green" if risk_score < 30 else "orange" if risk_score < 70 else "red"
        
        st.metric(
            label="Risk Score", 
            value=f"{risk_score}/100",
            delta=f"{risk_level} Risk",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Recent Alerts", 
            value=len(alert_data),
            delta=f"{alert_data['new_alerts_count']} new"
        )
    
    # Alerts section
    if len(alert_data) > 0:
        with st.expander("⚠️ Recent Deforestation Alerts", expanded=True):
            st.dataframe(
                alert_data[['date', 'location', 'severity', 'area_hectares', 'description']],
                use_container_width=True,
                hide_index=True
            )
            
            if st.button("Mark All as Read"):
                st.success("All alerts marked as read")
                time.sleep(1)
    
    # Tab-based layout for main content
    tab1, tab2, tab3 = st.tabs(["Interactive Map", "Biodiversity Impact", "Analysis & Trends"])
    
    with tab1:
        st.subheader("Deforestation Map")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Interactive map
            map_layers = {
                'deforestation': show_deforestation,
                'protected_areas': show_protected_areas,
                'risk_zones': show_risk_zones
            }
            forest_map = create_map(deforestation_data, map_layers)
            folium_map = forest_map._repr_html_()
            st.components.v1.html(folium_map, height=500)
        
        with col2:
            st.subheader("Map Legend")
            st.markdown("🔴 **High Risk Areas**")
            st.markdown("🟠 **Medium Risk Areas**")
            st.markdown("🟢 **Low Risk Areas**")
            st.markdown("🟦 **Protected Areas**")
            st.markdown("🔍 **Click on markers for details**")
            
            st.markdown("---")
            st.subheader("Risk Factors")
            risk_factors = pd.DataFrame({
                'Factor': ['Logging', 'Agriculture', 'Mining', 'Infrastructure'],
                'Contribution (%)': [35, 45, 12, 8]
            })
            st.dataframe(risk_factors, hide_index=True, use_container_width=True)
    
        st.subheader("Time-Lapse Visualization")
        year_for_timelapse = st.slider(
            "Select year to view:",
            min_value=selected_year_range[0],
            max_value=selected_year_range[1],
            value=selected_year_range[0]
        )
        
        timelapse_map = create_time_lapse_map(deforestation_data, year_for_timelapse)
        folium_timelapse = timelapse_map._repr_html_()
        st.components.v1.html(folium_timelapse, height=400)
        
    with tab2:
        st.subheader("Biodiversity Impact Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Species at Risk")
            biodiversity_fig = plot_biodiversity_impact(biodiversity_data)
            st.plotly_chart(biodiversity_fig, use_container_width=True)
            
        with col2:
            st.subheader("Risk Distribution")
            risk_fig = plot_risk_distribution(biodiversity_data)
            st.plotly_chart(risk_fig, use_container_width=True)
        
        st.subheader("Most Affected Species")
        col1, col2, col3 = st.columns(3)
        
        top_species = biodiversity_data['top_affected_species']
        
        for i, (col, species) in enumerate(zip([col1, col2, col3], top_species[:3])):
            with col:
                st.markdown(f"#### {species['name']}")
                st.markdown(f"**Status**: {species['status']}")
                st.markdown(f"**Habitat Loss**: {species['habitat_loss_percent']}%")
                st.markdown(f"**Population Decline**: {species['population_decline']}%")
                st.progress(species['risk_level'] / 100)
                
                risk_text = "Low Risk" if species['risk_level'] < 30 else "Medium Risk" if species['risk_level'] < 70 else "High Risk"
                risk_color = "green" if species['risk_level'] < 30 else "orange" if species['risk_level'] < 70 else "red"
                st.markdown(f"Risk Level: <span style='color:{risk_color}'>{risk_text}</span>", unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Deforestation Trends and Analysis")
        
        trend_fig = plot_deforestation_trend(deforestation_data)
        st.plotly_chart(trend_fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Contributing Factors")
            st.write("""
            The main drivers of deforestation in this region are:
            
            1. **Agricultural Expansion** (45%): Clearing forests for crops and livestock
            2. **Logging Activities** (35%): Both legal and illegal timber harvesting
            3. **Mining Operations** (12%): Extraction of minerals and resources
            4. **Infrastructure Development** (8%): Roads, dams, and urban expansion
            """)
            
        with col2:
            st.subheader("Conservation Status")
            
            # Protected areas information
            protected_data = deforestation_data['protected_areas']
            
            st.markdown(f"**Protected Areas**: {protected_data['total_count']} areas")
            st.markdown(f"**Total Protected Land**: {protected_data['total_area']:,.0f} hectares")
            st.markdown(f"**Protection Coverage**: {protected_data['protection_percentage']:.1f}% of region")
            
            protection_status = pd.DataFrame({
                'Status': ['Well Protected', 'At Risk', 'Critically Endangered'],
                'Percentage': [
                    protected_data['well_protected_percent'],
                    protected_data['at_risk_percent'], 
                    protected_data['critical_percent']
                ]
            })
            
            st.dataframe(protection_status, hide_index=True, use_container_width=True)
        
        st.subheader("Recommendations")
        
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        
        with rec_col1:
            st.markdown("#### Policy Actions")
            st.markdown("• Strengthen enforcement of protected areas")
            st.markdown("• Implement sustainable logging regulations")
            st.markdown("• Create economic incentives for conservation")
            
        with rec_col2:
            st.markdown("#### Community Involvement")
            st.markdown("• Support indigenous land management")
            st.markdown("• Promote eco-tourism initiatives")
            st.markdown("• Educate local communities on conservation")
            
        with rec_col3:
            st.markdown("#### Monitoring Improvements")
            st.markdown("• Increase satellite monitoring frequency")
            st.markdown("• Deploy ground sensors in high-risk areas")
            st.markdown("• Create rapid response teams for new alerts")
    
    # Footer
    st.markdown("---")
    st.caption("© 2023 Forest Guardian | Data updated daily | Sources: Global Forest Watch, IUCN Red List, NASA Earth Observations")

if __name__ == "__main__":
    main()
