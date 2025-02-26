#!/usr/bin/env python
# coding: utf-8

from dash import dash, dash_table, callback, html, dcc, Input, Output
import dash_bootstrap_components as dbc # type: ignore
import pandas as pd
import numpy as np
import altair as alt
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
import calendar
import tempfile
import zipfile

# initialize the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Billionaires Landscape")

# server
server = app.server

# load data
df = pd.read_csv("./data/Billionaires Statistics Dataset.csv")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
