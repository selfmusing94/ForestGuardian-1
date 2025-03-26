import folium
from folium.plugins import HeatMap, MarkerCluster, TimeSliderChoropleth
import pandas as pd
import numpy as np
from branca.colormap import LinearColormap

def create_map(deforestation_data, layers):
    """
    Create an interactive map with deforestation hotspots and layers
    
    Parameters:
    deforestation_data: Dictionary with deforestation data
    layers: Dictionary with layer toggle states
    
    Returns:
    Folium map object
    """
    # Get region center for map initialization
    region_centers = {
        "Amazon": [-5.0, -60.0],
        "Congo Basin": [0.0, 20.0],
        "Southeast Asia": [5.0, 110.0],
        "Central America": [15.0, -85.0],
        "Global": [0.0, 0.0]
    }
    
    region = deforestation_data['region']
    center = region_centers.get(region, [0.0, 0.0])
    zoom_start = 4 if region != "Global" else 2
    
    # Create base map
    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="cartodbpositron"
    )
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add deforestation heatmap if enabled
    if layers.get('deforestation', True):
        # Extract hotspot data
        hotspots = deforestation_data['hotspots']
        heat_data = [[spot['lat'], spot['lon'], spot['area_hectares']] for spot in hotspots]
        
        # Create heatmap layer
        HeatMap(
            heat_data,
            radius=15,
            gradient={0.4: 'blue', 0.65: 'yellow', 1: 'red'},
            name="Deforestation Heatmap",
            show=True
        ).add_to(m)
    
    # Add risk zones if enabled
    if layers.get('risk_zones', True):
        # Create marker cluster for risk zones
        marker_cluster = MarkerCluster(name="Risk Zones", show=True)
        
        for spot in deforestation_data['hotspots']:
            # Determine icon color based on risk score
            risk_score = spot['risk_score']
            
            if risk_score > 70:
                icon_color = 'red'
                risk_level = 'High'
            elif risk_score > 30:
                icon_color = 'orange'
                risk_level = 'Medium'
            else:
                icon_color = 'green'
                risk_level = 'Low'
            
            # Create popup content
            popup_html = f"""
            <div style="width:200px;">
                <h4>Deforestation Risk Zone</h4>
                <p><b>Risk Level:</b> {risk_level} ({risk_score}/100)</p>
                <p><b>Area Affected:</b> {spot['area_hectares']:.1f} hectares</p>
                <p><b>First Detected:</b> {spot['first_detected'].strftime('%d %b %Y')}</p>
                <p><b>Severity:</b> {spot['severity']} (1-3 scale)</p>
            </div>
            """
            
            # Add marker to cluster
            folium.Marker(
                location=[spot['lat'], spot['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=icon_color, icon='warning', prefix='fa')
            ).add_to(marker_cluster)
        
        marker_cluster.add_to(m)
    
    # Add protected areas if enabled
    if layers.get('protected_areas', True):
        # In a real application, this would use actual GeoJSON data for protected areas
        # Here we'll create some random circular areas as an example
        
        # Create a feature group for protected areas
        protected_group = folium.FeatureGroup(name="Protected Areas", show=True)
        
        # Number of protected areas to show
        num_areas = min(20, deforestation_data['protected_areas']['total_count'])
        
        # Region center
        center_lat, center_lon = center
        
        for i in range(num_areas):
            # Generate random position not too far from center
            lat = center_lat + np.random.uniform(-5, 5)
            lon = center_lon + np.random.uniform(-5, 5)
            
            # Area size (radius in meters)
            radius = np.random.uniform(10000, 50000)
            
            # Status based on overall protection rates
            status_odds = [
                deforestation_data['protected_areas']['well_protected_percent'],
                deforestation_data['protected_areas']['at_risk_percent'],
                deforestation_data['protected_areas']['critical_percent']
            ]
            status_odds = [o/sum(status_odds) for o in status_odds]  # Normalize
            
            status = np.random.choice(
                ['Well Protected', 'At Risk', 'Critical'],
                p=status_odds
            )
            
            # Color based on status
            color = {
                'Well Protected': 'green',
                'At Risk': 'orange',
                'Critical': 'red'
            }.get(status, 'blue')
            
            # Create circle and popup
            folium.Circle(
                location=[lat, lon],
                radius=radius,
                color=color,
                fill=True,
                fill_opacity=0.2,
                popup=f"Protected Area {i+1}<br>Status: {status}<br>Size: {radius/1000:.1f} km²"
            ).add_to(protected_group)
        
        protected_group.add_to(m)
    
    return m

def create_time_lapse_map(deforestation_data, selected_year):
    """
    Create a map showing the deforestation state for a specific year
    
    Parameters:
    deforestation_data: Dictionary with deforestation data
    selected_year: Year to display
    
    Returns:
    Folium map object
    """
    # Get region center for map initialization
    region_centers = {
        "Amazon": [-5.0, -60.0],
        "Congo Basin": [0.0, 20.0],
        "Southeast Asia": [5.0, 110.0],
        "Central America": [15.0, -85.0],
        "Global": [0.0, 0.0]
    }
    
    region = deforestation_data['region']
    center = region_centers.get(region, [0.0, 0.0])
    zoom_start = 4 if region != "Global" else 2
    
    # Create base map
    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="cartodbpositron"
    )
    
    # Filter hotspots to only show those detected up to the selected year
    filtered_hotspots = [
        spot for spot in deforestation_data['hotspots'] 
        if spot['first_detected'].year <= selected_year
    ]
    
    # Create severity-based markers
    for severity in [1, 2, 3]:
        # Filter by severity
        severity_hotspots = [spot for spot in filtered_hotspots if spot['severity'] == severity]
        
        # Skip if no hotspots of this severity
        if not severity_hotspots:
            continue
        
        # Determine group name and color
        severity_name = {1: "Low", 2: "Medium", 3: "High"}.get(severity, "Unknown")
        color = {1: "green", 2: "orange", 3: "red"}.get(severity, "blue")
        
        # Create feature group
        group = folium.FeatureGroup(name=f"{severity_name} Severity", show=True)
        
        # Add markers
        for spot in severity_hotspots:
            # Create popup content
            popup_html = f"""
            <div style="width:200px;">
                <h4>Deforested Area</h4>
                <p><b>Year Detected:</b> {spot['first_detected'].year}</p>
                <p><b>Area Affected:</b> {spot['area_hectares']:.1f} hectares</p>
                <p><b>Severity:</b> {severity_name}</p>
            </div>
            """
            
            # Add circle marker
            folium.CircleMarker(
                location=[spot['lat'], spot['lon']],
                radius=np.sqrt(spot['area_hectares']) / 5,  # Size proportional to area
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(group)
        
        group.add_to(m)
    
    # Add the year as a title
    title_html = f'''
        <h3 align="center" style="font-size:16px">
            <b>Deforestation Status in {selected_year}</b>
        </h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    return m
