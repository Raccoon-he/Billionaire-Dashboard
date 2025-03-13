#!/usr/bin/env python
# coding: utf-8

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pycountry
import geopandas as gpd
import altair as alt
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv('../data/Billionaires_Statistics_Updated_Countrycoded.csv')

# Group by country and count billionaires
billionaires_count = df.groupby('country').size().reset_index(name='billionaire_count')

# Calculate global billionaire count
global_billionaire_count = billionaires_count['billionaire_count'].sum()

# Assume you already have a GeoDataFrame containing country geometries
geo_df = gpd.read_file('../data/ne_110m_admin_0_countries_lakes/ne_110m_admin_0_countries_lakes.shp')  # Or other formats
geo_df['centroid'] = geo_df.geometry.centroid
geo_df['longitude'] = geo_df.centroid.x
geo_df['latitude'] = geo_df.centroid.y
geo_df['area'] = geo_df.geometry.area

# Ensure the column names in geo_df match your ISO codes (assumed to be 'iso_code')
merged = geo_df.merge(billionaires_count, left_on='ISO_A3', right_on='country', how='left').fillna(0)

# Calculate average finalWorth by age and industries
df['age_group'] = (df['age'] // 10) * 10

# gender process
df['gender'] = df['gender'].replace({'M': 'Male', 'F': 'Female'})

# Extract richest person
richest_person = df.loc[df["finalWorth"].idxmax(), ["personName", "finalWorth"]]

# Extract youngest and oldest billionaire
youngest_billionaire = df.loc[df["age"].idxmin(), ["personName", "age"]]
oldest_billionaire = df.loc[df["age"].idxmax(), ["personName", "age"]]

# Extract top industry (by total finalWorth)
top_industry = df.groupby("industries")["finalWorth"].sum().idxmax()

# Extract top company (by total finalWorth) using 'source' column
top_company = df.groupby("source")["finalWorth"].sum().idxmax()

# Color for industries
industries_color = {
    "Automotive": "#FFD700",  # Gold (more vibrant than yellow)
    "Construction & Engineering": "#FF69B4",  # Deeper pink
    "Diversified": "#32CD32",  # Lime green (more vivid)
    "Energy": "#1E90FF",  # Dodger blue (enhanced visibility)
    "Fashion & Retail": "#FF8C00",  # Darker orange
    "Finance & Investments": "#BA55D3",  # Medium orchid (better contrast)
    "Food & Beverage": "#D3D3D3",  # Light gray instead of white
    "Gambling & Casinos": "#DC143C",  # Crimson (rich red)
    "Healthcare": "#00CED1",  # Dark turquoise (similar but more readable)
    "Logistics": "#FFA500",  # Darker gold/orange
    "Manufacturing": "#A9A9A9",  # Dark grayish silver
    "Media & Entertainment": "#3CB371",  # Medium sea green
    "Metals & Mining": "#A0522D", 
    "Real Estate": "#FF6347",  # Tomato (richer coral)
    "Service": "#4682B4",  # Steel blue (better contrast)
    "Sports": "#FFFF99",  # Soft yellow
    "Technology": "#FFB6C1",  # Light pink (but deeper)
    "Telecom": "#9370DB"  # Medium purple (for readability)
}


# color
bg_color = "#000000"
card_color = "#333333"
text_color = "#FFD700"

# Create Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = dbc.Container([
    # Main Heading and Tabs in the same row
    dbc.Row([
        # Title on the left
        dbc.Col([
            html.H1("Billionaires Landscape", style={'color': '#FFD700', 'backgroundColor': '#000000', 'padding': '10px', 'margin': '0'})
        ], style={'display': 'flex', 'alignItems': 'center', 'flex': '1'}),

        # Tabs on the right
        dbc.Col([
            dcc.Tabs(id='tabs', value='tab-1', children=[
                dcc.Tab(label='Overlook', value='tab-1', 
                        style={'fontSize': '12px', 'borderRadius': '10px', 'width': '120px', 'height': '25px', 'backgroundColor': '#000000', 'color': '#FFD700', 'padding': '1px'}, 
                        selected_style={'fontSize': '12px', 'borderRadius': '10px', 'width': '120px', 'height': '25px', 'backgroundColor': '#000000', 'color': '#FFD700', 'padding': '1px'}),
                dcc.Tab(label='More Info', value='tab-2', 
                        style={'fontSize': '12px', 'borderRadius': '10px', 'width': '120px', 'height': '25px', 'backgroundColor': '#000000', 'color': '#FFD700', 'padding': '1px'}, 
                        selected_style={'fontSize': '12px', 'borderRadius': '10px', 'width': '120px', 'height': '25px', 'backgroundColor': '#000000', 'color': '#FFD700', 'padding': '1px'}),
            ], style={'height': '50px', 'marginTop': '10px'})
        ], style={'display': 'flex', 'justifyContent': 'flex-end', 'alignItems': 'flex-start', 'flex': '1'})
    ], style={'backgroundColor': '#000000', 'padding': '10px', 'borderBottom': '2px solid #FFD700', 'marginTop': '0', 'textAlign': 'left', 'display': 'flex', 'justifyContent': 'space-between'}),

    # Tab 1 Content: Summary and Map
    html.Div(id='tab-content')
], fluid=True, style={'margin': '0px', 'padding': '0px', 'overflow': 'hidden', "padding": "0px", "backgroundColor": bg_color}) 


# Tab 1 Content: Summary and Map
tab1_content = dbc.Container([
    # Map and Key Statistics in the same row
    dbc.Row([
        # Map Column
        dbc.Col([
            dbc.Card([
                # Move the content (Graph and Text) above the header
                html.Div(id='billionaire-count-text', style={'color': '#FFFFFF', 'fontSize': 20, 'textAlign': 'center', 'padding': '10px'}),
                dcc.Graph(
                    id='choropleth-map',
                    style={'height': '100%', 'padding': '3px', 'overflow': 'hidden'}  # Hide overflow content
                ),
                # Move the header to the bottom
                dbc.CardHeader("Global Billionaire Distribution", style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center'}),
            ], style={'padding':'0px','width': '100%', 'height':'666px', 'overflow': 'hidden', 'backgroundColor': '#000000'})  # Ensure Card width fills parent container and hide overflow
        ], 
        style={'padding':'0px', 'flex':'5', 'flexDirection': 'column', 'justifyContent': 'flex-end', 'alignItems': 'flex-start', 'overflow': 'hidden', 'border': '2px solid yellow'}),  # Set Map column width ratio and hide overflow

        # Key Statistics Column
        dbc.Col([
            dbc.Row([
                # Richest Person
                dbc.Col([
                    html.P("Richest Person", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center', 'marginBottom':'0%'}),
                    html.P(id='richest-person', style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
                ], style={'height': '15%', 'textAlign': 'center', 'overflow': 'hidden', 'marginBottom':'5%'}),  # Height remains 20%

                # Youngest Billionaire
                dbc.Col([
                    html.P("Youngest Billionaire", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center', 'marginBottom':'0%'}),
                    html.P(id='youngest-billionaire', style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
                ], style={'height': '15%', 'textAlign': 'center', 'overflow': 'hidden', 'marginBottom':'5%'}),  # Height remains 20%

                # Oldest Billionaire
                dbc.Col([
                    html.P("Oldest Billionaire", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center', 'marginBottom':'0%'}),
                    html.P(id='oldest-billionaire', style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center', })
                ], style={'height': '15%', 'textAlign': 'center', 'overflow': 'hidden', 'marginBottom':'5%'}),  # Height remains 20%

                # Top Industry
                dbc.Col([
                    html.P("Top Industry", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center', 'marginBottom':'0%'}),
                    html.P(id='top-industry', style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
                ], style={'height': '15%', 'textAlign': 'center', 'overflow': 'hidden'}),  # Height reduced to 15%

                # Top Company
                dbc.Col([
                    html.P("Top Source", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center', 'marginBottom':'0%'}),
                    html.P(id='top-company', style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
                ], style={'height': '15%', 'textAlign': 'center', 'overflow': 'hidden'}),  # Height reduced to 15%

                # Back to Global Button
                dbc.Col([
                    dbc.Button(
                        "Back to Global", 
                        id="select-all-button", 
                        color="primary", 
                        className="mb-3", 
                        style={
                            'backgroundColor': '#FFD700', 
                            'color': '#000000',
                            'border': '0px',
                            'fontSize': '10px', 
                        }
                    )
                ],style={'height': '5%', 'textAlign': 'center', 'overflow': 'hidden'})  # Height for button
            ],style={'height':'100%','backgroundColor': '#000000', 'padding': '10px', 'borderBottom': '2px solid #FFD700', 'marginTop': '0', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-end', 'overflow': 'hidden'}),  # Hide overflow content
        ], 
        # col:metrics
        style={'flex':'1', 'height': '100%', 'flex': '1',  'overflow': 'hidden'})  # Set Statistics column width ratio and hide overflow
    ], 
    # row: map+metrics
    style={'width':'100%','height':'666px','alignItems': 'stretch', 'margin': '0px','display': 'flex', 'justifyContent': 'flex-between', 'overflow': 'hidden'})  # Ensure Row layout is reasonable and hide overflow
], fluid=True, style={'marginLeft': '0px', 'padding': '0px', 'overflow': 'hidden'})  # Ensure inner Container margin and padding are consistent and hide overflow

# Tab 2 Content: Detailed Analysis
tab2_content = dbc.Container([
    dbc.Row([
        # Filters column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filters", style={'backgroundColor': bg_color, 'color': text_color, 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}),
                dbc.CardBody([
                    html.P(
                        "Default: Global & All Industries",
                        style={'color': '#cccccc', 'marginBottom': '4px', 'marginTop': '0px', 'fontSize': '14px'}
                    ),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': cou, 'value': cou} for cou in df['countryOfCitizenship'].unique()],
                        value=[],  # Default to all countries
                        multi=True,
                        placeholder="Select countries",
                        style={'margin': '0', 'width': '100%'}
                    ),
                    # html.Br(),
                    dcc.Dropdown(
                        id='industry-dropdown',
                        options=[{'label': ind, 'value': ind} for ind in df['industries'].unique()],
                        value=[],  # Default to all industries
                        multi=True,
                        placeholder="Select industries",
                        style={'margin': '0', 'width': '100%'}
                    )
                ], style={'padding': '0'})
            ], style={"backgroundColor": bg_color, 'height': '186px', 'padding': '0', 'margin': '0'}),

            # industries color legend
            dbc.Card([
                dbc.CardHeader("Legend", style={'backgroundColor': bg_color, 'color': text_color, 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}),
                dbc.CardBody([
                    html.Div(id='legend')
                ])
            ], style={"backgroundColor": bg_color, 'height': '480px', 'padding': '0', 'margin': '0', 'width': '100%'})
        ], width=3),

        # right column
        dbc.Col([
            # line 1
            dbc.Row([
                dbc.Col([
                    # scatter plot
                    dbc.Card([
                        dbc.CardHeader("Wealth Distribution Across Different Ages", style={'backgroundColor': bg_color, 'color': text_color, 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}),
                        dcc.Graph(
                            id='scatter-chart',
                            style={'height': '100%', 'width': '100%', 'margin': '0', 'padding': '0'}
                        )
                    ], style={"backgroundColor": bg_color, 'height': '333px', 'padding': '0', 'margin': '0'})
                ],width=6),

                # stacked bar chart
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Comparison of Male and Female Counts Across Ages", style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}),
                        dcc.Graph(
                            id='stacked-bar-chart',
                            style={'height': '100%', 'width': '100%', 'margin': '0', 'padding': '0'}
                        )
                    ], style={"backgroundColor": bg_color, 'height': '333px', 'padding': '0', 'margin': '0'})
                ], width=6)
            ]),

            # line 2
            dbc.Row([
                # pie chart
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            "Industry Wealth Proportions",
                            style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}
                        ),
                        dcc.Graph(
                            id='pie-chart',
                            style={'height': '100%', 'width': '100%', 'margin': '0', 'padding': '0'}
                        )  
                    ], style={"backgroundColor": bg_color, 'height': '333px', 'padding': '0', 'margin': '0'})  
                ], width=6),

                # Top 10 Companies Bar Chart
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Top 10 Wealth Sources", style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}),
                        dcc.Graph(
                            id='top-sources-bar-chart',
                            style={'height': '100%', 'width': '100%', 'margin': '0', 'padding': '0'}
                        )
                    ], style={"backgroundColor": bg_color, 'height': '333px', 'padding': '0', 'margin': '0'})
                ], width=6)
            ])     
        ])
    ])
], fluid=True, style={"padding": "0px", "backgroundColor": bg_color})


# Callback to switch between tabs
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'tab-1':
        return tab1_content
    elif tab == 'tab-2':
        return tab2_content


def calculate_zoom_level(area):
    # Define minimum and maximum zoom values
    zoom_min = 2  # Minimum zoom value
    zoom_max = 5  # Maximum zoom value

    area_min = geo_df['area'].min()
    area_max = geo_df['area'].max()

    log_area_min = np.log(area_min + 1)  # Add 1 to avoid log(0)
    log_area_max = np.log(area_max + 1)
    log_area = np.log(area + 1)

    # Calculate zoom value
    zoom = zoom_max - (log_area - log_area_min) / (log_area_max - log_area_min) * (zoom_max - zoom_min)
    return max(zoom_min, min(zoom_max, zoom))  # Ensure zoom value is within reasonable range

# Calculate global statistics as initial values
richest_person_global = df.loc[df["finalWorth"].idxmax(), ["personName", "finalWorth"]]
youngest_billionaire_global = df.loc[df["age"].idxmin(), ["personName", "age"]]
oldest_billionaire_global = df.loc[df["age"].idxmax(), ["personName", "age"]]
top_industry_global = df.groupby("industries")["finalWorth"].sum().idxmax()
top_company_global = df.groupby("source")["finalWorth"].sum().idxmax()


# Callback to update the Key Statistics Column based on clicked country or global data
@app.callback(
    [Output('richest-person', 'children'),
     Output('youngest-billionaire', 'children'),
     Output('oldest-billionaire', 'children'),
     Output('top-industry', 'children'),
     Output('top-company', 'children')],
    [Input('choropleth-map', 'clickData'),
     Input('select-all-button', 'n_clicks')]
)
def update_key_statistics(clickData, n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If "Back to Global" button is clicked
    if trigger_id == 'select-all-button':
        # Use global data
        richest_person_global_final_worth_billion = richest_person_global['finalWorth']
        return (html.Div(f"{richest_person_global['personName']}\n(${int(richest_person_global_final_worth_billion)}M)", style={'whiteSpace': 'pre-line'}),
                html.Div(f"{youngest_billionaire_global['personName']}\n({int(youngest_billionaire_global['age'])})", style={'whiteSpace': 'pre-line'}),
                html.Div(f"{oldest_billionaire_global['personName']}\n({int(oldest_billionaire_global['age'])})", style={'whiteSpace': 'pre-line'}),
                top_industry_global,
                top_company_global)

    # If a country is clicked
    if clickData:
        try:
            # Extract country code from clickData
            customdata = clickData['points'][0].get('customdata')
            if customdata and len(customdata) > 1:
                country_code = customdata[1]
                
                # Filter data for the selected country
                country_data = df[df['country'] == country_code]
                
                # Calculate statistics for the selected country
                richest_person = country_data.loc[country_data["finalWorth"].idxmax(), ["personName", "finalWorth"]]
                youngest_billionaire = country_data.loc[country_data["age"].idxmin(), ["personName", "age"]]
                oldest_billionaire = country_data.loc[country_data["age"].idxmax(), ["personName", "age"]]
                top_industry = country_data.groupby("industries")["finalWorth"].sum().idxmax()
                top_company = country_data.groupby("source")["finalWorth"].sum().idxmax()
                
                # Convert finalWorth from million dollars to billion dollars
                richest_person_final_worth_billion = richest_person['finalWorth']
                
                # Return the calculated values with line breaks using html.Div
                return (html.Div(f"{richest_person['personName']}\n(${int(richest_person_final_worth_billion):,}M)", style={'whiteSpace': 'pre-line'}),
                        html.Div(f"{youngest_billionaire['personName']}\n(Age: {int(youngest_billionaire['age'])})", style={'whiteSpace': 'pre-line'}),
                        html.Div(f"{oldest_billionaire['personName']}\n(Age: {int(oldest_billionaire['age'])})", style={'whiteSpace': 'pre-line'}),
                        top_industry,
                        top_company)
        except Exception as e:
            print(f"Error processing clickData: {e}")
    
    # Default to global statistics if no country is selected or an error occurs
    # Convert finalWorth from million dollars to billion dollars
    richest_person_global_final_worth_billion = richest_person_global['finalWorth']
    
    return (html.Div(f"{richest_person_global['personName']}\n(${int(richest_person_global_final_worth_billion):,}M)", style={'whiteSpace': 'pre-line'}),
            html.Div(f"{youngest_billionaire_global['personName']}\n(Age: {int(youngest_billionaire_global['age'])})", style={'whiteSpace': 'pre-line'}),
            html.Div(f"{oldest_billionaire_global['personName']}\n(Age: {int(oldest_billionaire_global['age'])})", style={'whiteSpace': 'pre-line'}),
            top_industry_global,
            top_company_global)


# Callback to update the choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('select-all-button', 'n_clicks')]
)
def update_map(clickData, n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If "Back to Global" button is clicked
    if trigger_id == 'select-all-button':
        center_lat = 36
        center_lon = 5
        zoom_level = 1
    else:
        center_lat = 36
        center_lon = 5
        zoom_level = 1
        if clickData:
            try:
                customdata = clickData['points'][0].get('customdata')
                if customdata and len(customdata) > 1:
                    country_code = customdata[1]
                    country_data = geo_df[geo_df['ISO_A3'] == country_code]
                    if not country_data.empty:
                        center_lat = country_data['latitude'].values[0]
                        center_lon = country_data['longitude'].values[0]
                        area = country_data['area'].values[0]
                        zoom_level = calculate_zoom_level(area)
            except Exception as e:
                print(f"Error processing clickData: {e}")

    fig = px.choropleth_map(
        merged,
        geojson=merged.geometry,  # Geographic data
        locations=merged.index,   # Use index as location
        color="billionaire_count", # Color mapped to billionaire count
        hover_name="NAME",         # Display country name on hover
        hover_data={"billionaire_count": True, "country": False},  # Data to display on hover
        center={"lat": center_lat, "lon": center_lon},  # Map center
        map_style="open-street-map",    # Use OpenStreetMap base map
        zoom=zoom_level,                         # Initial zoom level
        color_continuous_scale=[        # Color gradient
            [0, "#D3D3D3"], [0.1, "#C0B0A0"], [0.2, "#B0A080"],
            [0.4, "#DAA520"], [0.6, "#FFD700"], [0.8, "#FFC600"],
            [1, "#FFA500"]
        ],
        range_color=[0, 100],  # Set maximum range to 200
        labels={"billionaire_count": "Billionaire Count"}
    )
    # Update layout
    fig.update_layout(
        coloraxis_colorbar=dict(
            title_font_color='white',
            tickvals=[0, 10, 20, 40, 60, 80, 100],  # Manually set tick values
            ticktext=["0", "10", "20", "40", "60", "80", "100+"],  # Manually set tick labels
            tickfont=dict(color='white')
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # Remove margins
        autosize=True,  # Auto-resize
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    return fig

# Callback to update the text component with billionaire count
@app.callback(
    Output('billionaire-count-text', 'children'),
    [Input('choropleth-map', 'clickData'),
     Input('select-all-button', 'n_clicks')]
)
def update_billionaire_count_text(clickData, n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If "Back to Global" button is clicked
    if trigger_id == 'select-all-button':
        return f"Global Billionaires Count: {global_billionaire_count}"

    # If a country is clicked
    if clickData:
        try:
            # Extract country code from customdata
            customdata = clickData['points'][0].get('customdata')
            if customdata and len(customdata) > 1:  # Ensure customdata exists and has enough elements
                country_code = customdata[1]  # Second element is the country code
                print("Extracted Country Code:", country_code)
                
                # Use pycountry to get country name
                country = pycountry.countries.get(alpha_3=country_code)
                if country:
                    country_name = country.name
                    
                    # Find the corresponding billionaire count in billionaires_count
                    billionaire_count = billionaires_count[billionaires_count['country'] == country_code]['billionaire_count'].values[0]
                    
                    # Return the result
                    return f"Selected Country: {country_name} | Billionaires Count: {billionaire_count}"
                else:
                    return f"Country not found for code: {country_code}"
            else:
                # If customdata is invalid, display global billionaire count
                return f"Global Billionaires Count: {global_billionaire_count}"
        except Exception as e:
            # Print error message
            return f"Global Billionaires Count: {global_billionaire_count}"
    
    # If no click data, display global billionaire count
    return f"Global Billionaires Count: {global_billionaire_count}"


# Tab2 - Callback to update the legend based on the selected industries
@app.callback(
    Output('legend', 'children'),
    [Input('industry-dropdown', 'value')]
)
def update_legend(selected_industries):
    legend_items = []
    for industry, color in industries_color.items():
        if selected_industries and industry not in selected_industries:
            continue
        legend_items.append(
            html.Div([
                html.Span(style={'backgroundColor': color, 'width': '20px', 'height': '10px', 'display': 'inline-block', 'margin-right': '15px', 'margin-left': '15px'}),
                html.Span(style={'color': color, 'fontSize': '16px', 'marginRight': '5px'}, children=industry)
            ])
        )
    return legend_items

# Callback to update the scatter chart based on the selected filters
@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('industry-dropdown', 'value')]
)
def update_scatter_chart(selected_countries, selected_industries):
    # Start with the full dataframe
    filtered_df = df.copy()

    # Filter by selected countries if any are selected
    if selected_countries:
        filtered_df = filtered_df[filtered_df['countryOfCitizenship'].isin(selected_countries)]

    # Filter by selected industries if any are selected
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industries'].isin(selected_industries)]

    # Prepare the data for the scatter plot
    scatter_data = filtered_df.groupby(['age', 'industries'])['finalWorth'].sum().reset_index()

    # Create the scatter plot
    fig = px.scatter(
        scatter_data,
        x='age',
        y='finalWorth',
        color='industries',
        color_discrete_map=industries_color,
        size_max=8
    )

    fig.update_layout(
        margin=dict(l=1, r=1, t=1, b=1),  # Remove internal margins
        autosize=True,  # Allow dynamic resizing
        xaxis = dict(title='Age', color='white', showgrid=True, gridcolor='#cccccc'),
        yaxis = dict(title='Total Wealth ($M)', color='white', showgrid=True, gridcolor='#cccccc'),
        plot_bgcolor=card_color,
        paper_bgcolor=card_color,
        showlegend = False,
    )

    return fig

# Callback to update the stacked bar chart based on the selected filters
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('industry-dropdown', 'value')]
)
def update_stacked_bar_chart(selected_countries, selected_industries):
    # Start with the full dataframe
    filtered_df = df.copy()

    # Filter by selected countries if any are selected
    if selected_countries:
        filtered_df = filtered_df[filtered_df['countryOfCitizenship'].isin(selected_countries)]

    # Filter by selected industries if any are selected
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industries'].isin(selected_industries)]

    # Handle the case when no data is available after filtering
    if filtered_df.empty:
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color),
            margin=dict(l=1, r=1, t=10, b=1)
        )
        return fig
    
    # Prepare the data for the stacked bar chart
    stacked_bar_data = filtered_df.groupby(['age_group', 'gender']).size().reset_index(name='count')

    # Create the stacked bar chart
    custom_colors = {
        'Male': '#87CEEB',
        'Female': 'pink'
    }

    fig = px.bar(
        stacked_bar_data,
        x='age_group',
        y='count',
        color='gender',
        color_discrete_map=custom_colors
    )

    # Update the layout
    fig.update_layout(
        margin=dict(l=1, r=1, t=1, b=1),  # Remove internal margins
        autosize=True,  # Allow dynamic resizing
        xaxis = dict(title='Age', color='white', showgrid=True, gridcolor='#cccccc'),
        yaxis = dict(title='Count', color='white', showgrid=True, gridcolor='#cccccc'),
        barmode='stack',
        plot_bgcolor=card_color,
        paper_bgcolor=card_color,
        legend=dict(  
            orientation="h",  # Horizontal orientation
            yanchor="bottom", 
            y=0.9,  
            xanchor="left",  
            x=0.01,  
            font=dict(color='white'),
            title_text="" 
        )
    )

    return fig

# Callback to update the pie chart based on the selected filters
@app.callback(
    Output('pie-chart', 'figure'),  
    [Input('country-dropdown', 'value'),
     Input('industry-dropdown', 'value')]
)
def update_pie_chart(selected_countries, selected_industries):
    # Start with the full dataframe
    filtered_df = df.copy()

    # Filter by selected countries if any are selected
    if selected_countries:
        filtered_df = filtered_df[filtered_df['countryOfCitizenship'].isin(selected_countries)]

    # Filter by selected industries if any are selected
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industries'].isin(selected_industries)]

    # Handle the case when no data is available after filtering
    if filtered_df.empty:
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor='white',
            font=dict(color=text_color),
            margin=dict(l=1, r=1, t=10, b=1)
        )
        return fig

    # Group data by industries and compute total wealth per industry
    selected_df = filtered_df.groupby("industries", as_index=False)["finalWorth"].sum()
    
    # Compute industry-wise wealth percentage
    total_wealth = selected_df["finalWorth"].sum()
    selected_df["percentage"] = (selected_df["finalWorth"] / total_wealth) * 100

    # Sort industries by wealth and keep only the Top 3 for labeling
    selected_df = selected_df.sort_values(by="finalWorth", ascending=False)
    top_3_industries = selected_df.iloc[:3]["industries"].tolist()

    # Create Plotly Pie Chart
    fig = px.pie(
        selected_df, 
        names="industries", 
        values="finalWorth", 
        color="industries",
        color_discrete_map=industries_color
    )

    # Assign custom data to pass the percentage values
    fig.update_traces(customdata=selected_df[["percentage"]].to_numpy())

    # Modify text labels to show only for the top 3 industries
    fig.update_traces(
        textinfo="none",  # Hide all labels by default
        textposition="inside",
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>Wealth: %{value:.2f}B$<br>Percentage: %{customdata[0]:.2f}%"
    )

    # Show labels only for the top 3 industries
    text_template = [
        "%{label}<br>%{percent:.1%}" if industry in top_3_industries else ""
        for industry in selected_df["industries"]
    ]

    fig.update_traces(texttemplate=text_template)

    # Remove the black border around slices
    fig.update_traces(marker=dict(line=dict(width=0))) 

    # Update layout to match dark theme
    fig.update_layout(
        margin=dict(l=1, r=1, t=10, b=1),
        autosize=True,  
        plot_bgcolor=card_color, 
        paper_bgcolor=card_color,  
        font=dict(color=text_color),
        showlegend=False
    )

    return fig


# Callback to update the top 10 sources bar chart based on the selected filters
@app.callback(
    Output('top-sources-bar-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('industry-dropdown', 'value')]
)
def update_top_sources_bar_chart(selected_countries, selected_industries):
    # Start with the full dataframe
    filtered_df = df.copy()

    # Default: Show global top 10 sources if no filters are selected
    if selected_countries:
        filtered_df = filtered_df[filtered_df['countryOfCitizenship'].isin(selected_countries)]
    
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industries'].isin(selected_industries)]
    
    # Group by source and industry, summing finalWorth
    top_sources = filtered_df.groupby(['source', 'industries'], as_index=False)['finalWorth'].sum()
    
    # Compute total wealth for each source across industries
    total_wealth_per_source = top_sources.groupby('source', as_index=False)['finalWorth'].sum()
    
    # Get the top 10 sources based on total wealth
    top_sources_list = total_wealth_per_source.sort_values(by='finalWorth', ascending=False).head(10)['source']
    
    # Filter the dataset to only include the top 10 sources
    top_sources = top_sources[top_sources['source'].isin(top_sources_list)]

    # Create the horizontal bar chart
    fig = px.bar(
        top_sources,
        x='finalWorth',
        y='source',
        color='industries',  # Assign colors based on industry
        color_discrete_map=industries_color,
        orientation='h',
        labels={'finalWorth': 'Wealth ($M)', 'source': 'Source'}
    )

    fig.update_traces(width=0.7)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(title='Wealth ($M)', color='white', showgrid=True, gridcolor='#cccccc'),
        yaxis=dict(title='Source', color='white', categoryorder='total ascending'),  # Ensure sorting by total wealth
        plot_bgcolor=card_color,
        paper_bgcolor=card_color,
        showlegend=False,  # Remove legend
        title_text=None  # Remove plot title
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
