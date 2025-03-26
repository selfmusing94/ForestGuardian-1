import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_deforestation_data(region, year_range):
    """
    Load and process deforestation data based on region and year range.
    In a real application, this would fetch data from an API or database.
    """
    # Create synthetic data for demonstration
    years = list(range(year_range[0], year_range[1] + 1))
    
    # Base data with regional variations
    base_loss_rates = {
        "Amazon": 2000000,
        "Congo Basin": 1500000,
        "Southeast Asia": 1800000,
        "Central America": 900000,
        "Global": 5000000
    }
    
    # Generate yearly data with some variance and a generally increasing trend
    yearly_data = []
    base_loss = base_loss_rates.get(region, 1000000)
    
    for i, year in enumerate(years):
        # Add some yearly variation with an increasing trend
        yearly_loss = base_loss * (1 + (i * 0.05)) * np.random.uniform(0.9, 1.1)
        
        # Add seasonal patterns
        monthly_data = []
        for month in range(1, 13):
            # More deforestation during dry seasons (adjust based on region)
            seasonal_factor = 1.0
            if region == "Amazon" and month in [6, 7, 8, 9]:  # Dry season
                seasonal_factor = 1.3
            elif region == "Southeast Asia" and month in [1, 2, 3]:
                seasonal_factor = 1.3
            
            monthly_loss = yearly_loss / 12 * seasonal_factor * np.random.uniform(0.8, 1.2)
            
            monthly_data.append({
                'year': year,
                'month': month,
                'deforestation_hectares': monthly_loss,
                'region': region
            })
        
        yearly_data.extend(monthly_data)
    
    df = pd.DataFrame(yearly_data)
    
    # Calculate total loss and percentage change
    total_loss_hectares = df['deforestation_hectares'].sum()
    
    # Calculate percentage change from first to last year
    first_year_loss = df[df['year'] == years[0]]['deforestation_hectares'].sum()
    last_year_loss = df[df['year'] == years[-1]]['deforestation_hectares'].sum()
    loss_change_percent = ((last_year_loss - first_year_loss) / first_year_loss) * 100
    
    # Generate hotspot data for map visualization
    num_hotspots = 50
    hotspots = []
    
    # Region-specific coordinates (approximate centers)
    region_coords = {
        "Amazon": (-5.0, -60.0, 12.0, 8.0),  # lat, lon, lat_spread, lon_spread
        "Congo Basin": (0.0, 20.0, 10.0, 10.0),
        "Southeast Asia": (5.0, 110.0, 15.0, 15.0),
        "Central America": (15.0, -85.0, 5.0, 10.0),
        "Global": (0.0, 0.0, 60.0, 180.0)
    }
    
    center_lat, center_lon, lat_spread, lon_spread = region_coords.get(region, (0.0, 0.0, 60.0, 180.0))
    
    for i in range(num_hotspots):
        # Generate random coordinates within the region
        lat = center_lat + np.random.uniform(-lat_spread, lat_spread)
        lon = center_lon + np.random.uniform(-lon_spread, lon_spread)
        
        # Generate severity (higher numbers = worse deforestation)
        severity = np.random.choice([1, 2, 3], p=[0.3, 0.4, 0.3])
        
        # Area affected
        area = np.random.uniform(50, 2000) * severity
        
        # First detection date
        first_detected = datetime(
            np.random.choice(years),
            np.random.randint(1, 13),
            np.random.randint(1, 28)
        )
        
        hotspots.append({
            'lat': lat,
            'lon': lon,
            'severity': severity,
            'area_hectares': area,
            'first_detected': first_detected,
            'risk_score': np.random.randint(1, 101)
        })
    
    # Generate protected areas data
    protected_areas = {
        'total_count': np.random.randint(20, 100),
        'total_area': np.random.uniform(500000, 5000000),
        'protection_percentage': np.random.uniform(10, 30),
        'well_protected_percent': np.random.uniform(30, 60),
        'at_risk_percent': np.random.uniform(20, 40),
        'critical_percent': np.random.uniform(10, 30)
    }
    
    # Combine all data into a single structured dictionary
    result = {
        'raw_data': df,
        'total_loss_hectares': total_loss_hectares,
        'loss_change_percent': loss_change_percent,
        'hotspots': hotspots,
        'protected_areas': protected_areas,
        'region': region,
        'year_range': year_range
    }
    
    return result

def load_biodiversity_data(region, year_range):
    """
    Load and process biodiversity impact data based on region and year range.
    In a real application, this would fetch data from an API or database.
    """
    # Regional variations for species data
    region_species_data = {
        "Amazon": {
            'total_species': 40000,
            'mammals': 430,
            'birds': 1300,
            'amphibians': 1000,
            'plants': 30000,
            'endemic_percent': 30,
        },
        "Congo Basin": {
            'total_species': 20000,
            'mammals': 400,
            'birds': 1000,
            'amphibians': 400,
            'plants': 15000,
            'endemic_percent': 20,
        },
        "Southeast Asia": {
            'total_species': 25000,
            'mammals': 350,
            'birds': 1200,
            'amphibians': 600,
            'plants': 18000,
            'endemic_percent': 25,
        },
        "Central America": {
            'total_species': 18000,
            'mammals': 250,
            'birds': 900,
            'amphibians': 500,
            'plants': 12000,
            'endemic_percent': 15,
        },
        "Global": {
            'total_species': 100000,
            'mammals': 1000,
            'birds': 5000,
            'amphibians': 2000,
            'plants': 80000,
            'endemic_percent': 10,
        }
    }
    
    base_data = region_species_data.get(region, region_species_data["Global"])
    
    # Calculate species at risk based on region and deforestation rates
    species_at_risk = int(base_data['total_species'] * np.random.uniform(0.05, 0.2))
    species_change = int(species_at_risk * np.random.uniform(-0.1, 0.2))
    
    # Calculate risk score (0-100)
    risk_score = int(np.random.uniform(20, 80))
    
    # Species distribution data
    species_distribution = [
        {'category': 'Mammals', 'count': base_data['mammals'], 'at_risk': int(base_data['mammals'] * np.random.uniform(0.1, 0.3))},
        {'category': 'Birds', 'count': base_data['birds'], 'at_risk': int(base_data['birds'] * np.random.uniform(0.05, 0.2))},
        {'category': 'Amphibians', 'count': base_data['amphibians'], 'at_risk': int(base_data['amphibians'] * np.random.uniform(0.1, 0.4))},
        {'category': 'Plants', 'count': base_data['plants'], 'at_risk': int(base_data['plants'] * np.random.uniform(0.05, 0.15))},
    ]
    
    # Risk distribution by severity
    risk_distribution = [
        {'level': 'Low Risk', 'percentage': np.random.uniform(25, 45)},
        {'level': 'Medium Risk', 'percentage': np.random.uniform(25, 45)},
        {'level': 'High Risk', 'percentage': np.random.uniform(15, 35)},
    ]
    # Normalize to 100%
    total = sum(item['percentage'] for item in risk_distribution)
    for item in risk_distribution:
        item['percentage'] = (item['percentage'] / total) * 100
    
    # Top affected species
    status_options = ['Critically Endangered', 'Endangered', 'Vulnerable']
    
    top_affected_species = []
    
    # Region-specific species
    region_species_names = {
        "Amazon": ['Jaguar', 'Uakari Monkey', 'Poison Dart Frog', 'Harpy Eagle', 'Giant Otter'],
        "Congo Basin": ['Mountain Gorilla', 'Forest Elephant', 'Okapi', 'Bonobo', 'Congo Peacock'],
        "Southeast Asia": ['Orangutan', 'Sumatran Tiger', 'Asian Elephant', 'Sunda Pangolin', 'Bornean Clouded Leopard'],
        "Central America": ['Resplendent Quetzal', 'Spider Monkey', 'Baird\'s Tapir', 'Scarlet Macaw', 'Golden Toad'],
        "Global": ['Tiger', 'Rhinoceros', 'Orangutan', 'Mountain Gorilla', 'Polar Bear']
    }
    
    species_names = region_species_names.get(region, region_species_names["Global"])
    
    for name in species_names:
        top_affected_species.append({
            'name': name,
            'status': np.random.choice(status_options),
            'habitat_loss_percent': np.random.randint(30, 85),
            'population_decline': np.random.randint(30, 90),
            'risk_level': np.random.randint(40, 95)
        })
    
    # Combine all data into a structured dictionary
    result = {
        'species_at_risk': species_at_risk,
        'species_change': species_change,
        'risk_score': risk_score,
        'species_distribution': species_distribution,
        'risk_distribution': risk_distribution,
        'top_affected_species': top_affected_species,
        'region': region,
        'year_range': year_range
    }
    
    return result

def load_alert_data(region, alert_threshold):
    """
    Load recent deforestation alerts based on region and threshold.
    In a real application, this would fetch data from an API or database.
    """
    # Number of alerts varies by threshold
    threshold_multiplier = {
        "Low": 1.5,
        "Medium": 1.0,
        "High": 0.5
    }
    
    # Base number of alerts by region
    base_alerts = {
        "Amazon": 15,
        "Congo Basin": 12,
        "Southeast Asia": 18,
        "Central America": 8,
        "Global": 30
    }
    
    num_alerts = int(base_alerts.get(region, 10) * threshold_multiplier.get(alert_threshold, 1.0))
    
    # Generate alert data
    alerts = []
    now = datetime.now()
    
    for i in range(num_alerts):
        # Generate a date within the last 30 days
        days_ago = np.random.randint(0, 30)
        alert_date = now - timedelta(days=days_ago)
        
        # Regional coordinates
        region_coords = {
            "Amazon": (-5.0, -60.0, 12.0, 8.0),  # lat, lon, lat_spread, lon_spread
            "Congo Basin": (0.0, 20.0, 10.0, 10.0),
            "Southeast Asia": (5.0, 110.0, 15.0, 15.0),
            "Central America": (15.0, -85.0, 5.0, 10.0),
            "Global": (0.0, 0.0, 60.0, 180.0)
        }
        
        center_lat, center_lon, lat_spread, lon_spread = region_coords.get(region, (0.0, 0.0, 60.0, 180.0))
        
        # Generate random coordinates within the region
        lat = center_lat + np.random.uniform(-lat_spread, lat_spread)
        lon = center_lon + np.random.uniform(-lon_spread, lon_spread)
        
        # Location name
        location = f"{lat:.2f}°, {lon:.2f}°"
        
        # Severity (higher numbers = worse deforestation)
        severity_options = ["Low", "Medium", "High"]
        severity_probs = [0.3, 0.4, 0.3]
        severity = np.random.choice(severity_options, p=severity_probs)
        
        # Area affected
        area_multiplier = 1 if severity == "Low" else 3 if severity == "Medium" else 10
        area_hectares = np.random.uniform(10, 100) * area_multiplier
        
        # Description based on severity
        descriptions = {
            "Low": [
                "Small-scale clearing detected",
                "Minor forest disturbance observed",
                "Limited logging activity detected"
            ],
            "Medium": [
                "Moderate clearing for agriculture",
                "Significant logging operations detected",
                "Road construction causing forest fragmentation"
            ],
            "High": [
                "Large-scale forest clearing for palm oil",
                "Massive deforestation for cattle ranching",
                "Critical habitat destruction by mining operations"
            ]
        }
        
        description = np.random.choice(descriptions.get(severity, ["Forest disturbance detected"]))
        
        alerts.append({
            'date': alert_date,
            'location': location,
            'severity': severity,
            'area_hectares': area_hectares,
            'description': description,
            'lat': lat,
            'lon': lon,
            'is_new': days_ago < 5  # New alerts are less than 5 days old
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(alerts)
    
    # Sort by date (most recent first)
    df = df.sort_values('date', ascending=False).reset_index(drop=True)
    
    # Count new alerts
    new_alerts_count = df['is_new'].sum()
    
    # Add the count to the DataFrame
    df['new_alerts_count'] = new_alerts_count
    
    return df
