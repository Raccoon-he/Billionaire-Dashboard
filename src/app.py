#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pycountry
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from geopy.geocoders import Nominatim

# Load dataset
df = pd.read_csv('./Billionaires_Statistics_Updated_Countrycoded.csv')

# Group by country and count billionaires
billionaires_count = df.groupby('country').size().reset_index(name='billionaire_count')

# Calculate global billionaire count
global_billionaire_count = billionaires_count['billionaire_count'].sum()

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Cache for country latitudes and longitudes
country_lat_lon_cache = {}

# Function to get latitude and longitude
def get_country_lat_lon(country_name):
    if country_name in country_lat_lon_cache:
        return country_lat_lon_cache[country_name]
    
    try:
        location = geolocator.geocode(country_name)
        if location:
            lat, lon = location.latitude, location.longitude
            country_lat_lon_cache[country_name] = (lat, lon)
            return lat, lon
    except Exception as e:
        print(f"Error fetching lat/lon for {country_name}: {e}")
    return None, None

# Create Dash app
app = dash.Dash(__name__)

# Define map module
map_module = html.Div([
    html.Div(id='billionaire-count-text', style={'fontSize': 25, 'fontWeight': 'bold', 'marginBottom': '1px'}),
    dcc.Graph(
        id='choropleth-map',
        style={'height': '100%', 
               'width': '100%',
               'border': '1px solid white',}
    )
], style={
    'position': 'relative',
    'top': '3px',
    'left': '1px',   
    'width': '60%',
    'height': '50%',
    'zIndex': '1000',
    'backgroundColor': 'white',
    'padding': '0px',
    'border': '1px solid white',
    'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)', 
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'flex-start', 
    'alignItems': 'baseline',
    'overflow': 'hidden'
})

# add other modules here like map_module

# Define layout
app.layout = html.Div([
    map_module,  # left-top is map
    # other modules
])

# Update map callback
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('choropleth-map', 'clickData'))
def update_map(clickData):
    # Define custom color scale (light blue to gold)
    custom_colorscale = [
        [0, 'rgb(173, 216, 230)'],  # Light blue
        [0.5, 'rgb(255, 215, 0)'],  # Gold
        [1, 'rgb(255, 140, 0)']     # Darker gold
    ]

    # Create choropleth map
    fig = px.choropleth(
        billionaires_count,
        locations="country",
        color="billionaire_count",
        hover_name="country",
        hover_data={"billionaire_count": True, "country": False},
        locationmode='ISO-3',
        color_continuous_scale=custom_colorscale  # Apply custom color scale
    )

    # Customize map appearance
    fig.update_geos(
        landcolor="LightGrey",      # Land color
        oceancolor="LightBlue",     # Ocean color
        showcountries=True,          # Show country borders
        countrycolor="White",
        showcoastlines=True,
        coastlinecolor="White",  # Coastline color
        showframe=False,
        lakecolor="#69ADE0",
        rivercolor="#69ADE0",
        bgcolor='#EDF7FE'
    )

    # Customize color bar
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Billionaires",  # Color bar title
            title_font=dict(size=10),
            x=10,                # Position (x-axis)
            y=8,                # Position (y-axis)
            len=0.5,               # Length
            thickness=15,         # Thickness of the color bar
            xanchor='left',      # Anchor point for x position
            yanchor='bottom' 
        ),
        margin=dict(l=0, r=3, t=20, b=40),
        dragmode=False
    )

    # Zoom to selected country
    if clickData:
        country_code = clickData['points'][0]['location']
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            if country:
                country_name = country.name
                lat, lon = get_country_lat_lon(country_name)
                if lat and lon:
                    # Set map center and scope to the selected country
                    fig.update_geos(
                        center=dict(lat=lat, lon=lon),
                        projection_scale=5  # Zoom level (higher value = more zoom)
                    )
        except Exception as e:
            print(f"Error processing country code {country_code}: {e}")

    return fig

# Update text callback
@app.callback(
    Output('billionaire-count-text', 'children'),
    Input('choropleth-map', 'clickData'))
def update_billionaire_count_text(clickData):
    if clickData:
        country_code = clickData['points'][0]['location']
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            if country:
                country_name = country.name
                billionaire_count = billionaires_count[billionaires_count['country'] == country_code]['billionaire_count'].values[0]
                return "Selected Country: {} | Billionaires: {}".format(country_name, billionaire_count)
        except Exception as e:
            print(f"Error processing country code {country_code}: {e}")
    # Default to global billionaire count
    return "Global Billionaires: {}".format(global_billionaire_count)

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
