import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import math
import numpy as np
import datetime as dt
import pandas as pd
import json
from app import app
from lib import title, sidebar, us_map, stats, selector

app.layout = dbc.Container(
    [ 
        dbc.Row([
            dbc.Col([
                sidebar.sidebar
            ]),
        ]),
        dbc.Row([
              title.title
        ]),
        dbc.Row([]),
        dbc.Row([]),
        ],
    className="ds4a-app",  
)

DATA_DIR = "data"
superstore_path = os.path.join(DATA_DIR, "superstore.csv")
us_path = os.path.join(DATA_DIR, "us.json")
states_path = os.path.join(DATA_DIR, "states.json")
df = pd.read_csv(superstore_path, parse_dates=["Order Date", "Ship Date"])

with open(us_path) as geo:
    geojson = json.loads(geo.read())

with open(states_path) as f:
    states_dict = json.loads(f.read())

df["State_abbr"] = df["State"].map(states_dict)
df["Order_Month"] = pd.to_datetime(df["Order Date"].dt.to_period("M").astype(str))


@app.callback(
    Output("US_map", "figure"),
    [
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ],
)
def update_map(start_date,end_date):
    dff = df[(df['Order Date'] >= start_date) & (df['Order Date'] < end_date)] # We filter our dataset for the daterange
    dff=dff.groupby("State_abbr").sum().reset_index()
    fig_map2=px.choropleth_mapbox(dff,
        locations='State_abbr',
        color='Sales',
        geojson=geojson, 
        zoom=3, 
        mapbox_style="carto-positron", 
        center={"lat": 37.0902, "lon": -95.7129},
        color_continuous_scale="Viridis",
        opacity=0.5,
        title='US Sales'
        )
    fig_map2.update_layout(title="US State Sales",margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#F8F9F9", plot_bgcolor="#F8F9F9",)
    return fig_map2


@app.callback(
    [Output("Line", "figure"),Output("Scatter","figure")],
    [
        Input("state_dropdown", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ],
)
def make_line_plot(state_dropdown, start_date, end_date):
    ddf=df[df['State_abbr'].isin(state_dropdown)]
    ddf = ddf[(ddf['Order Date'] >= start_date) & (ddf['Order Date'] < end_date)] 
    
    ddf1=ddf.groupby(['Order_Month', 'State']).sum()
    ddf1=ddf1.reset_index()
        
    Line_fig=px.line(ddf1,x="Order_Month",y="Sales", color="State")
    Line_fig.update_layout(title='Montly Sales in selected states',paper_bgcolor="#F8F9F9")
    
    Scatter_fig=px.scatter(ddf, x="Sales", y="Profit", color="Category", hover_data=['State_abbr','Sub-Category','Order ID','Product Name'])  
    Scatter_fig.update_layout(title='Sales vs. Profit in selected states',paper_bgcolor="#F8F9F9")

    return [Line_fig, Scatter_fig]
    
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8080", debug=True)
