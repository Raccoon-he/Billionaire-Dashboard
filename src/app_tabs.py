#!/usr/bin/env python
# coding: utf-8

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pycountry
import altair as alt

# Load dataset
df = pd.read_csv('./data/Billionaires_Statistics_Updated_Countrycoded.csv')

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

# Define the layout using dbc.Container
app.layout = dbc.Container(
    [
        # Main Heading and Tabs in the same row
        dbc.Row(
            [
                # Title on the left
                dbc.Col(
                    [
                        html.H1(
                            "Billionaires Landscape",
                            style={
                                'color': '#FFD700',
                                'backgroundColor': '#000000',
                                'padding': '10px',
                                'margin': '0'
                            }
                        )
                    ],
                    style={
                        'display': 'flex',
                        'alignItems': 'center'
                    }
                ),
                # Tabs on the right
                dbc.Col(
                    [
                        dcc.Tabs(
                            id='tabs',
                            value='tab-1',
                            children=[
                                dcc.Tab(
                                    label='Overlook',
                                    value='tab-1',
                                    style={
                                        'fontSize': '12px',
                                        'borderRadius': '10px',
                                        'width': '120px',
                                        'height': '25px',
                                        'backgroundColor': '#000000',
                                        'color': '#FFD700',
                                        'padding': '1px'
                                    },
                                    selected_style={
                                        'fontSize': '12px',
                                        'borderRadius': '10px',
                                        'width': '120px',
                                        'height': '25px',
                                        'backgroundColor': '#000000',
                                        'color': '#FFD700',
                                        'padding': '1px'
                                    }
                                ),
                                dcc.Tab(
                                    label='More Info',
                                    value='tab-2',
                                    style={
                                        'fontSize': '12px',
                                        'borderRadius': '10px',
                                        'width': '120px',
                                        'height': '25px',
                                        'backgroundColor': '#000000',
                                        'color': '#FFD700',
                                        'padding': '1px'
                                    },
                                    selected_style={
                                        'fontSize': '12px',
                                        'borderRadius': '10px',
                                        'width': '120px',
                                        'height': '25px',
                                        'backgroundColor': '#000000',
                                        'color': '#FFD700',
                                        'padding': '1px'
                                    }
                                )
                            ],
                            style={
                                'height': '50px',
                                'marginTop': '10px'
                            }
                        )
                    ],
                    style={
                        'display': 'flex',
                        'justifyContent': 'flex-end',
                        'alignItems': 'center'
                    }
                )
            ],
            style={
                'backgroundColor': '#000000',
                'padding': '10px',
                'borderBottom': '2px solid #FFD700',
                'marginTop': '0',
                'textAlign': 'left'
            }
        ),
        # Tab 1 Content: Summary and Map
        html.Div(id='tab-content')
    ],
    fluid=True
)

# Tab 1 Content: Summary and Map
tab1_content = dbc.Container(
    [
        # Map and Key Statistics in the same row
        dbc.Row(
            [
                # Map Column
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                # Move the content (Graph and Text) above the header
                                html.Div(
                                    id='billionaire-count-text',
                                    style={
                                        'fontSize': 20,
                                        'textAlign': 'center',
                                        'padding': '10px'
                                    }
                                ),
                                dcc.Graph(
                                    id='choropleth-map',
                                    style={
                                        'height': '100%',
                                        'padding': '3px'
                                    }
                                ),
                                # Move the header to the bottom
                                dbc.CardHeader(
                                    "Global Billionaire Distribution",
                                    style={
                                        'backgroundColor': '#000000',
                                        'color': '#FFD700',
                                        'fontWeight': 'bold',
                                        'textAlign': 'center'
                                    }
                                )
                            ],
                            color="light"
                        )
                    ],
                    style={
                        'height': '100%'
                    }
                ),
                # Key Statistics Column
                dbc.Col(
                    [
                        # Top Row for Key Statistics
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P(
                                            "Richest Person",
                                            style={
                                                'color': '#D3D3D3',
                                                'fontWeight': 'bold',
                                                'fontSize': '14px',
                                                'textAlign': 'center'
                                            }
                                        ),
                                        html.P(
                                            f"Bernard Arnault & family ($211000B)",
                                            style={
                                                'color': '#FFD700',
                                                'fontWeight': 'bold',
                                                'fontSize': '16px',
                                                'textAlign': 'center'
                                            }
                                        )
                                    ],
                                    style={
                                        'minHeight': '100px',
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.Col(
                                    [
                                        html.P(
                                            "Youngest Billionaire",
                                            style={
                                                'color': '#D3D3D3',
                                                'fontWeight': 'bold',
                                                'fontSize': '14px',
                                                'textAlign': 'center'
                                            }
                                        ),
                                        html.P(
                                            f"Clemente Del Vecchio (18)",
                                            style={
                                                'color': '#FFD700',
                                                'fontWeight': 'bold',
                                                'fontSize': '16px',
                                                'textAlign': 'center'
                                            }
                                        )
                                    ],
                                    style={
                                        'minHeight': '100px',
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.Col(
                                    [
                                        html.P(
                                            "Oldest Billionaire",
                                            style={
                                                'color': '#D3D3D3',
                                                'fontWeight': 'bold',
                                                'fontSize': '14px',
                                                'textAlign': 'center'
                                            }
                                        ),
                                        html.P(
                                            f"George Joseph (101)",
                                            style={
                                                'color': '#FFD700',
                                                'fontWeight': 'bold',
                                                'fontSize': '16px',
                                                'textAlign': 'center'
                                            }
                                        )
                                    ],
                                    style={
                                        'minHeight': '100px',
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.Col(
                                    [
                                        html.P(
                                            "Top Industry",
                                            style={
                                                'color': '#D3D3D3',
                                                'fontWeight': 'bold',
                                                'fontSize': '14px',
                                                'textAlign': 'center'
                                            }
                                        ),
                                        html.P(
                                            f"Technology",
                                            style={
                                                'color': '#FFD700',
                                                'fontWeight': 'bold',
                                                'fontSize': '16px',
                                                'textAlign': 'center'
                                            }
                                        )
                                    ],
                                    style={
                                        'minHeight': '100px',
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.Col(
                                    [
                                        html.P(
                                            "Top Company",
                                            style={
                                                'color': '#D3D3D3',
                                                'fontWeight': 'bold',
                                                'fontSize': '14px',
                                                'textAlign': 'center'
                                            }
                                        ),
                                        html.P(
                                            f"Real estate",
                                            style={
                                                'color': '#FFD700',
                                                'fontWeight': 'bold',
                                                'fontSize': '16px',
                                                'textAlign': 'center'
                                            }
                                        )
                                    ],
                                    style={
                                        'minHeight': '100px',
                                        'textAlign': 'center'
                                    }
                                )
                            ],
                            style={
                                'backgroundColor': '#000000',
                                'padding': '10px',
                                'borderBottom': '2px solid #FFD700',
                                'marginTop': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'flex-end'
                            }
                        )
                    ],
                    style={
                        'height': '100%',
                        'display': 'flex',
                        'justifyContent': 'flex-end'
                    }
                )
            ],
            style={
                'height': '100%',
                'display': 'flex',
                'justifyContent': 'flex-end'
            }
        )
    ],
    fluid=True
)

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
        color_continuous_scale=["#D3D3D3", "#B0A080", "#FFD700"]
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

# Callback to update the line chart based on the clicked country and selected industries
@app.callback(
    Output('line-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('industry-dropdown', 'value')]
)
def update_line_chart(clickData, selected_industries):
    if clickData is None:
        filtered_df = df
    else:
        country_code = clickData['points'][0]['location']
        filtered_df = df[df['country'] == country_code]

    if selected_industries:
        filtered_df = filtered_df[filtered_df['industries'].isin(selected_industries)]
        line_data = filtered_df.groupby(['Age', 'industries'])['finalWorth'].sum().reset_index()
        fig = px.line(
            line_data,
            x='Age',
            y='finalWorth',
            color='industries'
        )
    else:
        line_data = filtered_df.groupby('Age')['finalWorth'].sum().reset_index()
        fig = px.line(
            line_data,
            x='Age',
            y='finalWorth'
        )

    fig.update_layout(
        margin=dict(l=1, r=1, t=1, b=1),
        autosize=True,
        height=200,
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        plot_bgcolor="white"
    )
    return fig

# Callback to update the pie chart
@app.callback(
    Output('pie-chart', 'srcDoc'),
    Input('choropleth-map', 'clickData')
)
def update_pie_chart(clickData):
    if clickData is None:
        filtered_df = df_pie.groupby("industries", as_index=False)["finalWorth"].sum()
        title = "Global Industry Distribution by Final Worth"
    else:
        country_code = clickData['points'][0]['location']
        filtered_df = df_pie[df_pie['country'] == country_code]
        title = f"Industry Distribution by Final Worth in {pycountry.countries.get(alpha_3=country_code).name}"

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
    return f"Global Billionaires: {global_billionaire_count}"

# Callback to update the top 10 companies bar chart
@app.callback(
    Output('top-companies-bar-chart', 'figure'),
    Input('choropleth-map', 'clickData')
)
def update_top_companies_bar_chart(clickData):
    if clickData is None:
        filtered_df = df
    else:
        country_code = clickData['points'][0]['location']
        filtered_df = df[df['country'] == country_code]

    top_companies = filtered_df.groupby('source')['finalWorth'].sum().reset_index()
    top_companies = top_companies.sort_values(by='finalWorth', ascending=False).head(10)

    top_companies = top_companies.merge(df[['source', 'industries']].drop_duplicates(), on='source', how='left')

    fig = px.bar(
        top_companies,
        x='finalWorth',
        y='source',
        color='industries',
        orientation='h',
        labels={'finalWorth': 'Wealth (B$)', 'source': 'Company'},
        title='Top 10 Companies by Wealth'
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(title='Wealth (B$)'),
        yaxis=dict(title='Company'),
        plot_bgcolor='white',
        height=400
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)