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
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv('../data/Billionaires_Statistics_Updated_Countrycoded.csv')

# Group by country and count billionaires
billionaires_count = df.groupby('country').size().reset_index(name='billionaire_count')

# Calculate global billionaire count
global_billionaire_count = billionaires_count['billionaire_count'].sum()

# Calculate average finalWorth by age and industries
df['age_group'] = (df['age'] // 10) * 10

# gender process
df['gender'] = df['gender'].replace({'M': 'Male', 'F': 'Female'})

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

# Color for industries
industries_color = {
    "Automotive": "#FFFF00",
    "Construction & Engineering": "#FFC0CB",
    "Diversified": "#00FF00",
    "Energy": "#00FFFF",
    "Fashion & Retail": "#FFA500",
    "Finance & Investments": "#FF00FF",
    "Food & Beverage": "#FFFFFF",
    "Gambling & Casinos": "#FF0000",
    "Healthcare": "#00FFFF",
    "Logistics": "#FFD700",
    "Manufacturing": "#C0C0C0",
    "Media & Entertainment": "#00FF80",
    "Metals & Mining": "#B2FFFC",
    "Real Estate": "#FF7F50",
    "Service": "#87CEEB",
    "Sports": "#FFFF33",
    "Technology":"#FFDAB9",
    "Telecom": "#E6E6FA"
}

# color
bg_color = "#000000"
card_color = "#333333"
text_color = "#FFD700"

# Create Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout using dbc.Container
app.layout = dbc.Container([
    # Main Heading and Tabs in the same row
    dbc.Row([
        # Title on the left
        dbc.Col([
            html.H1("Billionaires Landscape", style={'color': '#FFD700', 'backgroundColor': '#000000', 'padding': '10px', 'margin': '0'})
        ], style={'display': 'flex', 'alignItems': 'center'}),

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
        ], style={'display': 'flex', 'justifyContent': 'flex-end', 'alignItems': 'center'})
    ], style={'backgroundColor': '#000000', 'padding': '10px', 'borderBottom': '2px solid #FFD700', 'marginTop': '0'}),

    # Tab Content
    html.Div(id='tab-content')
], fluid=True, style={"padding": "0px", "backgroundColor": bg_color})

# Tab 1 Content: Summary and Map
tab1_content = dbc.Container([
    # Top Row for Key Statistics
    dbc.Row([
        dbc.Col([
            html.P("Richest Person", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center'}),
            html.P(f"{richest_person['personName']} (${richest_person['finalWorth']}B)", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ]),

        dbc.Col([
            html.P("Youngest Billionaire", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center'}),
            html.P(f"{youngest_billionaire['personName']} ({round(youngest_billionaire['age'])})", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ]),

        dbc.Col([
            html.P("Oldest Billionaire", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center'}),
            html.P(f"{oldest_billionaire['personName']} ({round(oldest_billionaire['age'])})", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ]),

        dbc.Col([
            html.P("Top Industry", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center'}),
            html.P(f"{top_industry}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ]),

        dbc.Col([
            html.P("Top Company", style={'color': '#D3D3D3', 'fontWeight': 'bold', 'fontSize': '14px', 'textAlign': 'center'}),
            html.P(f"{top_company}", 
                   style={'color': '#FFD700', 'fontWeight': 'bold', 'fontSize': '16px', 'textAlign': 'center'})
        ]),
    ], justify="center", style={'backgroundColor': '#000000', 'padding': '10px', 'borderBottom': '2px solid #FFD700', 'marginTop': '0'}), 

    # Map
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
        ])
    ])
], fluid=True, style={"padding": "0px", "backgroundColor": bg_color})

# Tab 2 Content: Detailed Analysis
tab2_content = dbc.Container([
    dbc.Row([
        # Filters column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filters", style={'backgroundColor': bg_color, 'color': text_color, 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': cou, 'value': cou} for cou in df['countryOfCitizenship'].unique()],
                        value=[],  # Default to all countries
                        multi=True,
                        placeholder="Select countries",
                        style={'margin': '0', 'width': '100%'}
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id='industry-dropdown',
                        options=[{'label': ind, 'value': ind} for ind in df['industries'].unique()],
                        value=[],  # Default to all industries
                        multi=True,
                        placeholder="Select industries",
                        style={'margin': '0', 'width': '100%'}
                    ),
                    html.P(
                        "Default: Global & All Industries",
                        style={'color': '#cccccc', 'marginTop': '8px'}
                    )
                ])
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
                dbc.Col(
                    # scatter plot
                    dbc.Card([
                        dbc.CardHeader("Wealth Distribution Across Different Ages", style={'backgroundColor': bg_color, 'color': text_color, 'fontWeight': 'bold', 'textAlign': 'center', 'padding': '0'}),
                        dcc.Graph(
                            id='scatter-chart',
                            style={'height': '100%', 'width': '100%', 'margin': '0', 'padding': '0'}
                        )
                    ], style={"backgroundColor": bg_color, 'height': '333px', 'padding': '0', 'margin': '0'})
                , width=6),

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
                            "Industry Proportions by Wealth",
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
                        dbc.CardHeader("Top 10 Sources by Wealth", style={'backgroundColor': '#000000', 'color': '#FFD700', 'fontWeight': 'bold', 'textAlign': 'center'}),
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

# Callback to update the legend based on the selected industries
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
        yaxis = dict(title='Total Wealth (B)', color='white', showgrid=True, gridcolor='#cccccc'),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
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

    # Prepare the data for the stacked bar chart
    stacked_bar_data = filtered_df.groupby(['age_group', 'gender']).size().unstack(fill_value=0).reset_index()

    # Create the stacked bar chart
    fig = px.bar(
        stacked_bar_data,
        x='age_group',
        y=['Male', 'Female'],
        color_discrete_sequence=['#87CEEB', 'pink'],
    )

    # Update the layout
    fig.update_layout(
        margin=dict(l=1, r=1, t=1, b=1),  # Remove internal margins
        autosize=True,  # Allow dynamic resizing
        xaxis = dict(title='Age', color='white', showgrid=True, gridcolor='#cccccc'),
        yaxis = dict(title='Count', color='white', showgrid=True, gridcolor='#cccccc'),
        barmode='stack',
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
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
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
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
        color_discrete_map=industries_color,  
        hover_data=["finalWorth", "percentage"]
    )

    # Remove the title and legend
    fig.update_layout(title_text=None, showlegend=False)

    # Modify text labels to show only for the top 3 industries
    fig.update_traces(
        textinfo="none",  # Hide all labels by default
        textposition="inside",
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>Wealth: %{value:.2f}B$<br>Percentage: %{customdata[1]:.2f}%"
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
        plot_bgcolor=bg_color, 
        paper_bgcolor=bg_color,  
        font=dict(color=text_color),
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
        labels={'finalWorth': 'Wealth (B$)', 'source': 'Source'}
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(title='Wealth (B$)', color='white', showgrid=True, gridcolor='#cccccc'),
        yaxis=dict(title='Source', color='white', categoryorder='total ascending'),  # Ensure sorting by total wealth
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        height=400,
        showlegend=False,  # Remove legend
        title_text=None  # Remove plot title
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

# Callback to update the top 10 companies bar chart
@app.callback(
    Output('top-companies-bar-chart', 'figure'),
    Input('choropleth-map', 'clickData')
)
def update_top_companies_bar_chart(clickData):
    # Determine the dataframe to use based on clickData
    if clickData is None:
        # Default to global data
        filtered_df = df
    else:
        # Extract the country code from the click data
        country_code = clickData['points'][0]['location']
        # Filter the dataframe to include only the selected country
        filtered_df = df[df['country'] == country_code]

    # Group by company and sum their finalWorth
    top_companies = filtered_df.groupby('source')['finalWorth'].sum().reset_index()
    # Sort by finalWorth and get the top 10
    top_companies = top_companies.sort_values(by='finalWorth', ascending=False).head(10)

    # Merge with the original dataframe to get the industry information
    top_companies = top_companies.merge(df[['source', 'industries']].drop_duplicates(), on='source', how='left')

    # Create the bar chart
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
