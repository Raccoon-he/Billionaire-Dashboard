import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pycountry
import geopandas as gpd

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
df['Age'] = (df['age'] // 10) * 10

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
], fluid=True, style={'margin': '0px', 'padding': '0px', 'overflow': 'hidden'})  # Hide overflow content


# Tab 1 Content: Summary and Map
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
            ], style={'padding':'0px','width': '100%', 'height':'100%', 'overflow': 'hidden', 'backgroundColor': '#000000'})  # Ensure Card width fills parent container and hide overflow
        ], 
        style={'padding':'0px', 'flex':'5', 'flexDirection': 'column', 'justifyContent': 'flex-end', 'alignItems': 'flex-start', 'overflow': 'hidden', 'border': '2px solid #FFD700'}),  # Set Map column width ratio and hide overflow

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
                    html.P("Top Company", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center', 'marginBottom':'0%'}),
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
    style={'width':'100%','height':'560px','alignItems': 'stretch', 'margin': '0px','display': 'flex', 'justifyContent': 'flex-between', 'overflow': 'hidden'})  # Ensure Row layout is reasonable and hide overflow
], fluid=True, style={'marginLeft': '0px', 'padding': '0px', 'overflow': 'hidden'})  # Ensure inner Container margin and padding are consistent and hide overflow

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
        richest_person_global_final_worth_billion = richest_person_global['finalWorth'] / 1_000
        return (html.Div(f"{richest_person_global['personName']}\n(${int(richest_person_global_final_worth_billion)}B)", style={'whiteSpace': 'pre-line'}),
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
                richest_person_final_worth_billion = richest_person['finalWorth'] / 1_000
                
                # Return the calculated values with line breaks using html.Div
                return (html.Div(f"{richest_person['personName']}\n(${int(richest_person_final_worth_billion)}B)", style={'whiteSpace': 'pre-line'}),
                        html.Div(f"{youngest_billionaire['personName']}\n({int(youngest_billionaire['age'])})", style={'whiteSpace': 'pre-line'}),
                        html.Div(f"{oldest_billionaire['personName']}\n({int(oldest_billionaire['age'])})", style={'whiteSpace': 'pre-line'}),
                        top_industry,
                        top_company)
        except Exception as e:
            print(f"Error processing clickData: {e}")
    
    # Default to global statistics if no country is selected or an error occurs
    # Convert finalWorth from million dollars to billion dollars
    richest_person_global_final_worth_billion = richest_person_global['finalWorth'] / 1_000
    
    return (html.Div(f"{richest_person_global['personName']}\n(${int(richest_person_global_final_worth_billion)}B)", style={'whiteSpace': 'pre-line'}),
            html.Div(f"{youngest_billionaire_global['personName']}\n({int(youngest_billionaire_global['age'])})", style={'whiteSpace': 'pre-line'}),
            html.Div(f"{oldest_billionaire_global['personName']}\n({int(oldest_billionaire_global['age'])})", style={'whiteSpace': 'pre-line'}),
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
