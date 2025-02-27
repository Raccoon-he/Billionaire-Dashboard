import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pycountry

# Load dataset
df = pd.read_csv('./data/Billionaires_Statistics_Updated_Countrycoded.csv')

# Group by country and count billionaires
billionaires_count = df.groupby('country').size().reset_index(name='billionaire_count')

# Calculate global billionaire count
global_billionaire_count = billionaires_count['billionaire_count'].sum()

# Calculate average finalWorth by age and industries
df['Age'] = (df['age'] // 10) * 10

# Create Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout using dbc.Container
app.layout = dbc.Container([
    html.H1("Billionaires Landscape", style={'textAlign': 'center', 'color': '#68A58C', 'marginBottom': '20px'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Global Billionaire Distribution", style={'backgroundColor': '#68A58C', 'fontWeight': 'bold', 'textAlign': 'center'}),
                dcc.Graph(
                    id='choropleth-map',
                    style={'height': '100%', 'padding': '3px'}
                ),
                html.Div(id='billionaire-count-text', style={'fontSize': 20, 'textAlign': 'center', 'padding': '10px'})
            ], color="light")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Final Worth by Age", style={'backgroundColor': '#68A58C', 'fontWeight': 'bold', 'textAlign': 'center'}),
                dcc.Dropdown(
                    id='industry-dropdown',
                    options=[{'label': ind, 'value': ind} for ind in df['industries'].unique()],
                    value=[],  # Default value
                    multi=True
                ),
                dcc.Graph(
                    id='line-chart',
                    style={'height': '100%', 'padding': '3px'}
                )
            ], color="light", style={'height': '50vh'})
        ], width=6),
    ]),
], fluid=True)

# Callback to update the choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('choropleth-map', 'clickData')
)
def update_map(clickData):
    fig = px.choropleth(
        billionaires_count,
        locations="country",
        color="billionaire_count",
        hover_name="country",
        hover_data={"billionaire_count": True, "country": False},
        locationmode='ISO-3',
        color_continuous_scale=px.colors.sequential.Greens
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

# Callback to update the line chart based on the clicked country and selected industries
# Callback to update the line chart based on the clicked country and selected industries
@app.callback(
    Output('line-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('industry-dropdown', 'value')]
)
def update_line_chart(clickData, selected_industries):
    # Determine the dataframe to use based on clickData
    if clickData is None:
        # Default to global data
        filtered_df = df
        title = "Global Sum of Final Worth by Age"
    else:
        # Extract the country code from the click data
        country_code = clickData['points'][0]['location']
        # Filter the dataframe to include only the selected country
        filtered_df = df[df['country'] == country_code]
        title = f"Sum of Final Worth by Age for {pycountry.countries.get(alpha_3=country_code).name}"

    # If industries are selected, further filter the dataframe
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industries'].isin(selected_industries)]
        # Group the filtered data by Age and industries, and calculate the sum of finalWorth
        line_data = filtered_df.groupby(['Age', 'industries'])['finalWorth'].sum().reset_index()
        # Create the line chart with multiple lines for each industry
        fig = px.line(
            line_data,
            x='Age',
            y='finalWorth',
            color='industries',
            title=title
        )
    else:
        # Default view: sum of finalWorth by Age
        line_data = filtered_df.groupby('Age')['finalWorth'].sum().reset_index()
        fig = px.line(
            line_data,
            x='Age',
            y='finalWorth',
            title=title
        )

    return fig

# Callback to update the text component with billionaire count
@app.callback(
    Output('billionaire-count-text', 'children'),
    Input('choropleth-map', 'clickData')
)
def update_billionaire_count_text(clickData):
    if clickData:
        country_code = clickData['points'][0]['location']
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            if country:
                country_name = country.name
                billionaire_count = billionaires_count[billionaires_count['country'] == country_code]['billionaire_count'].values[0]
                return f"Selected Country: {country_name} | Billionaires: {billionaire_count}"
        except Exception as e:
            print(f"Error processing country code {country_code}: {e}")
    # Default to global billionaire count
    return f"Global Billionaires: {global_billionaire_count}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)