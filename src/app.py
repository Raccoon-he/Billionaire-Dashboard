import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pycountry
import altair as alt


# Load dataset
df = pd.read_csv('../data/Billionaires_Statistics_Updated_Countrycoded.csv')

# Group by country and count billionaires
billionaires_count = df.groupby('country').size().reset_index(name='billionaire_count')

# Calculate global billionaire count
global_billionaire_count = billionaires_count['billionaire_count'].sum()

# Calculate average finalWorth by age and industries
df['Age'] = (df['age'] // 10) * 10

# Prepare data for the Altair pie chart
df_pie = df.groupby(["country", "industries"], as_index=False)["finalWorth"].sum()
df_pie["total_wealth"] = df_pie.groupby("country")["finalWorth"].transform("sum")
df_pie["percentage"] = (df_pie["finalWorth"] / df_pie["total_wealth"]) * 100

# Extract richest person
richest_person = df.loc[df["finalWorth"].idxmax(), ["personName", "finalWorth"]]

# Extract youngest and oldest billionaire
youngest_billionaire = df.loc[df["age"].idxmin(), ["personName", "age"]]
oldest_billionaire = df.loc[df["age"].idxmax(), ["personName", "age"]]

# Extract top industry (by total finalWorth)
top_industry = df.groupby("industries")["finalWorth"].sum().idxmax()

# Extract top company (by total finalWorth) using 'source' column
top_company = df.groupby("source")["finalWorth"].sum().idxmax()


# Create Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Function to create Altair Pie Chart
def create_pie_chart(selected_df, title):
    # Compute total wealth to calculate industry percentage
    total_wealth = selected_df["finalWorth"].sum()
    selected_df = selected_df.assign(percentage=(selected_df["finalWorth"] / total_wealth) * 100)

    # Sort industries by finalWorth (optional, makes visualization clearer)
    selected_df = selected_df.sort_values(by="finalWorth", ascending=False)

    # Create Altair Pie Chart
    chart = (
        alt.Chart(selected_df)
        .mark_arc()
        .encode(
            theta="finalWorth:Q",
            color=alt.Color("industries:N", legend=alt.Legend(title="Industries")),  # Industry colors
            tooltip=[
                alt.Tooltip("industries:N", title="Industry"),
                alt.Tooltip("finalWorth:Q", format=".2f", title="Final Worth (B$)"),
                alt.Tooltip("percentage:Q", format=".2f", title="Percentage (%)") 
            ],
        )
        .properties(title=title)
    )
    
    return chart.to_html()  

 
# Define the layout using dbc.Container
app.layout = dbc.Container([
    # Main Heading
    html.H1("Billionaires Landscape", style={'textAlign': 'center', 'color': '#FFD700', 'backgroundColor': '#000000', 'padding': '20px'}),

    html.Br(),

    # Top Row for Key Statistics
    dbc.Row([
        dbc.Col([
            html.P("Richest Person:", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '12px', 'textAlign': 'center'}),
            html.P(f"{richest_person['personName']}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'}),
            html.P(f"${richest_person['finalWorth']}B", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ], width=2),

        dbc.Col([
            html.P("Youngest Billionaire:", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '12px', 'textAlign': 'center'}),
            html.P(f"{youngest_billionaire['personName']}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'}),
            html.P(f"Age {youngest_billionaire['age']}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ], width=2),

        dbc.Col([
            html.P("Oldest Billionaire:", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '12px', 'textAlign': 'center'}),
            html.P(f"{oldest_billionaire['personName']}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'}),
            html.P(f"Age {oldest_billionaire['age']}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ], width=2),

        dbc.Col([
            html.P("Top Industry:", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '12px', 'textAlign': 'center'}),
            html.P(f"{top_industry}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ], width=2),

        dbc.Col([
            html.P("Top Company:", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '12px', 'textAlign': 'center'}),
            html.P(f"{top_company}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ], width=2),
    ], justify="center", style={'backgroundColor': '#000000', 'padding': '10px', 'borderBottom': '2px solid #FFD700'}),  # ✅ Connected Full Row

    html.Br(),

    # ✅ Main Dashboard Content
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Global Billionaire Distribution", style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center'}),
                dcc.Graph(
                    id='choropleth-map',
                    style={'height': '100%', 'padding': '3px'}
                ),
                html.Div(id='billionaire-count-text', style={'fontSize': 20, 'textAlign': 'center', 'padding': '10px'})
            ], color="light")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Final Worth by Age", style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center'}),
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
        ], width=4),
    ]),

    html.Br(),

    # ✅ Pie Chart Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    "Top 5 Industries by Final Worth",
                    style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center'}
                ),
                html.Iframe(
                    id='pie-chart',
                    style={'border-width': '0', 'width': '100%', 'height': '400px'}  
                )
            ], color="light", style={'border': '2px solid #FFD700'})  
        ], width=4),
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
        color_continuous_scale=[
            "#D3D3D3", "#B0A080", "#FFD700"
        ]
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


# Callback to update the pie chart 
@app.callback(
    Output('pie-chart', 'srcDoc'),  # Output the updated pie chart HTML
    Input('choropleth-map', 'clickData')  # Clicked country from the map
)
def update_pie_chart(clickData):
    # Determine the dataset to use based on clickData
    if clickData is None:
        # Default to global data (All industries globally)
        filtered_df = df_pie.groupby("industries", as_index=False)["finalWorth"].sum()
        title = "Global Industry Distribution by Final Worth"
    else:
        # Extract the country code from the click data
        country_code = clickData['points'][0]['location']
        # Filter the dataset to include only the selected country
        filtered_df = df_pie[df_pie['country'] == country_code]
        title = f"Industry Distribution by Final Worth in {pycountry.countries.get(alpha_3=country_code).name}"

    # No need to filter for top 5; show all industries
    return create_pie_chart(filtered_df, title)


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